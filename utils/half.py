matches = []
ignorables = [ 'take crackers', 'go west' ]

with open("walkthrough.txt") as file:
    for (line_count, line) in enumerate (file, 1):
        if not line.startswith('>'):
            continue
        if not '(1)' in line:
            continue
        a = line.lower().strip().split(' ')
        b = ' '.join(a[1:3])
        if b not in ignorables:
            matches.append(a[1:3])

with open("source_code.adv") as file:
    for (line_count, line) in enumerate (file, 1):
        if "_;" not in line and "_\"" not in line:
            continue
        for m in matches:
            if m[0] in line and m[1] in line and " _" in line and "_ " in line:
                matches.remove(m)
                break

if len(matches) == 0:
    print("Everything matched up! Hooray!")
else:
    for m in matches:
        print("Still need something for", ' '.join(m))
