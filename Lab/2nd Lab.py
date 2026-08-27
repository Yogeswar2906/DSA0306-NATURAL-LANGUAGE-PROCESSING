string = "aab"

state = 0

for ch in string:
    if state == 0:
        if ch == 'a':
            state = 1
        else:
            state = 0
    elif state == 1:
        if ch == 'a':
            state = 1
        elif ch == 'b':
            state = 2
        else:
            state = 0
    elif state == 2:
        if ch == 'a':
            state = 1
        else:
            state = 0

print("Input String :", string)

if state == 2:
    print("Accepted")
else:
    print("Rejected")