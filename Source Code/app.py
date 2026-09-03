"""
Property Dispute Judgment Interpretation System
================================================
Flask backend — serves the premium SPA and runs the NLP pipeline via a JSON API.

Run:
    python app.py
Open:
    http://localhost:5000
"""

from __future__ import annotations

import io
import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, Optional

from flask import Flask, jsonify, render_template, request

# ── project root on sys.path ────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── NLP modules ─────────────────────────────────────────────────────────────
from modules.preprocessing import preprocess, describe_tag
from modules.feature_grammar import parse_with_feature_grammar
from modules.pcfg_parser import parse_with_pcfg
from modules.wsd import disambiguate, get_target_terms
from modules.interpretation import interpret

# ── Flask app ────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024   # 20 MB

SAMPLE_PATH = PROJECT_ROOT / "data" / "sample_judgment.txt"
SAMPLE_FALLBACK = (
    "Karthik claimed ownership of the disputed property. "
    "The plaintiff stated that he purchased the land through a registered sale deed. "
    "The defendant disputed the claim and argued that the property belonged to his family."
)


# ============================================================================
#  Serialisers — convert dataclasses to plain JSON-serialisable dicts
# ============================================================================

def _serialise_m1(m1) -> Dict:
    return {
        "original_text": m1.original_text,
        "sentences": m1.sentences,
        "sentence_analyses": [
            {
                "index": sa.index,
                "original": sa.original,
                "tokens": sa.tokens,
                "pos_tags": [
                    {
                        "word": w,
                        "tag": t,
                        "description": describe_tag(t),
                    }
                    for w, t in sa.pos_tags
                ],
            }
            for sa in m1.sentence_analyses
        ],
    }


def _serialise_m2(m2_list) -> list:
    out = []
    for fg in m2_list:
        constituents = []
        for c in fg.constituents:
            constituents.append({
                "role": c.role,
                "words": c.words,
                "head": c.head,
                "feature_structure": dict(c.feature_structure.items()),
                "pos_tags": [{"word": w, "tag": t} for w, t in c.pos_tags],
            })
        out.append({
            "sentence": fg.sentence,
            "parse_success": fg.parse_success,
            "parse_note": fg.parse_note,
            "constituents": constituents,
            "unification_checks": fg.unification_checks,
        })
    return out


def _tree_to_dict(tree) -> Dict:
    """Recursively convert an NLTK Tree to a nested dict for rendering."""
    if isinstance(tree, str):
        return {"label": tree, "children": []}
    return {
        "label": str(tree.label()),
        "children": [_tree_to_dict(child) for child in tree],
    }


def _tree_pprint(tree) -> str:
    buf = io.StringIO()
    try:
        tree.pretty_print(stream=buf)
    except Exception:
        return str(tree)
    return buf.getvalue()


def _serialise_m3(m3_list) -> list:
    out = []
    for pc in m3_list:
        candidates = []
        for cand in pc.candidates[:5]:
            candidates.append({
                "rank": cand.rank,
                "probability": cand.probability,
                "tree_str": str(cand.tree),
                "tree_pprint": _tree_pprint(cand.tree),
                "tree_dict": _tree_to_dict(cand.tree),
                "is_selected": (cand.rank == 1),
            })
        out.append({
            "sentence": pc.sentence,
            "parse_success": pc.parse_success,
            "parse_note": pc.parse_note,
            "terminal_sequence": pc.terminal_sequence,
            "terminal_mapping": [
                {"word": w, "tag": t, "terminal": term}
                for w, t, term in pc.terminal_mapping
            ],
            "candidates": candidates,
            "selected_probability": pc.selected.probability if pc.selected else None,
            "grammar_rules_used": pc.grammar_rules_used,
        })
    return out


def _serialise_m4(m4) -> Dict:
    sentence_results = []
    for sr in m4.sentence_results:
        wsd_results = []
        for wr in sr.wsd_results:
            candidates = []
            for c in wr.candidates:
                candidates.append({
                    "sense_id": c.sense_id,
                    "label": c.label,
                    "definition": c.definition,
                    "keywords": c.keywords,
                    "overlap_count": c.overlap_count,
                    "overlap_words": c.overlap_words,
                    "score": c.score,
                    "is_selected": (
                        wr.selected_sense is not None
                        and c.sense_id == wr.selected_sense.sense_id
                    ),
                })
            wsd_results.append({
                "term": wr.term,
                "normalised_term": wr.normalised_term,
                "sentence": wr.sentence,
                "context_window": wr.context_window,
                "candidates": candidates,
                "selected_sense": {
                    "sense_id": wr.selected_sense.sense_id,
                    "label": wr.selected_sense.label,
                    "definition": wr.selected_sense.definition,
                    "overlap_words": wr.selected_sense.overlap_words,
                    "score": wr.selected_sense.score,
                } if wr.selected_sense else None,
                "determined": wr.determined,
                "method_note": wr.method_note,
            })
        sentence_results.append({
            "sentence_index": sr.sentence_index,
            "sentence": sr.sentence,
            "wsd_results": wsd_results,
        })
    return {"sentence_results": sentence_results}


def _serialise_final(final) -> Dict:
    sentence_interps = []
    for si in final.sentence_interpretations:
        wsd = []
        for wr in si.disambiguated_terms:
            if wr.determined and wr.selected_sense:
                wsd.append({
                    "term": wr.term,
                    "label": wr.selected_sense.label,
                    "overlap_words": wr.selected_sense.overlap_words,
                })
        sentence_interps.append({
            "sentence_index": si.sentence_index,
            "original_sentence": si.original_sentence,
            "subject": si.subject,
            "verb": si.verb,
            "obj": si.obj,
            "pp": si.pp,
            "syntactic_pattern": si.syntactic_pattern,
            "pcfg_parse_probability": si.pcfg_parse_probability,
            "pcfg_parse_note": si.pcfg_parse_note,
            "interpretation_text": si.interpretation_text,
            "disambiguated_terms": wsd,
        })
    return {
        "parties": final.parties,
        "legal_actions": final.legal_actions,
        "property_references": final.property_references,
        "legal_terms_found": final.legal_terms_found,
        "important_sentences": final.important_sentences,
        "sentence_interpretations": sentence_interps,
        "summary_text": final.summary_text,
        "disclaimer": final.disclaimer,
    }


# ============================================================================
#  Routes
# ============================================================================

@app.route("/")
def index():
    sample = SAMPLE_FALLBACK
    try:
        sample = SAMPLE_PATH.read_text(encoding="utf-8").strip()
    except Exception:
        pass
    monitored_terms = []
    try:
        monitored_terms = get_target_terms()
    except Exception:
        pass
    return render_template("index.html", sample=sample, monitored_terms=monitored_terms)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """Run the full NLP pipeline and return JSON results."""
    data = request.get_json(silent=True) or {}
    text: str = (data.get("text") or "").strip()

    if not text:
        return jsonify({"success": False, "error": "No text provided."}), 400
    if len(text) < 5:
        return jsonify({"success": False, "error": "Input text is too short."}), 400

    response: Dict[str, Any] = {"success": True}

    # ── Module 1 ─────────────────────────────────────────────────────────────
    try:
        m1 = preprocess(text)
        response["m1"] = _serialise_m1(m1)
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 422
    except Exception as e:
        return jsonify({"success": False, "error": f"Module 1 error: {e}"}), 500

    # ── Module 2 ─────────────────────────────────────────────────────────────
    try:
        m2 = parse_with_feature_grammar(m1)
        response["m2"] = _serialise_m2(m2)
    except Exception as e:
        response["m2"] = []
        response["m2_error"] = str(e)

    # ── Module 3 ─────────────────────────────────────────────────────────────
    try:
        m3 = parse_with_pcfg(m1)
        response["m3"] = _serialise_m3(m3)
    except Exception as e:
        response["m3"] = []
        response["m3_error"] = str(e)

    # ── Module 4 ─────────────────────────────────────────────────────────────
    try:
        m4 = disambiguate(m1)
        response["m4"] = _serialise_m4(m4)
    except Exception as e:
        response["m4"] = None
        response["m4_error"] = str(e)

    # ── Final interpretation ─────────────────────────────────────────────────
    try:
        if m1 and not response.get("m2_error") and not response.get("m3_error") and not response.get("m4_error"):
            final = interpret(m1, m2, m3, m4)
            response["final"] = _serialise_final(final)
    except Exception as e:
        response["final_error"] = str(e)

    return jsonify(response)


@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    """Extract text from an uploaded PDF file."""
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded."}), 400
    f = request.files["file"]
    if not f.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "error": "Only PDF files are accepted."}), 400
    try:
        import fitz
        data = f.read()
        doc = fitz.open(stream=data, filetype="pdf")
        pages = [page.get_text() for page in doc]
        doc.close()
        text = "\n".join(pages).strip()
        if not text:
            return jsonify({
                "success": False,
                "error": "Unable to extract readable text from this PDF. Please use a PDF with selectable text.",
            }), 422
        return jsonify({"success": True, "text": text, "pages": len(pages)})
    except ImportError:
        return jsonify({"success": False, "error": "PyMuPDF is not installed. Run: pip install pymupdf"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"PDF extraction failed: {e}"}), 500


# ============================================================================
#  Entry point
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*58)
    print("  Property Dispute Judgment Interpretation System")
    print("  Open: http://localhost:5000")
    print("="*58 + "\n")
    app.run(debug=False, host="0.0.0.0", port=5000)
