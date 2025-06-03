count = 0

def quote_split(my_string):
    temp = my_string.replace('\\"', ' QUOTATION MARK ')
    ary = [x.replace(' QUOTATION MARK ', '\\"') for x in temp.split('"')]
    return ary

def debuggable(line_count, line):
    return line_count == 2332

with open("source_code.adv") as file:
    for (line_count, line) in enumerate (file, 1):
        if 'print' not in line:
            continue
        if '{(' not in line:
            continue
        x = quote_split(line)
        unquoted = ' '.join(x[0::2])
        if "<\"" in line:
            continue
        if ' ? ' in unquoted and ' : ' in unquoted[1:]:
            continue
        if 'item()' in unquoted:
            continue
        if 'collection_get' in unquoted:
            continue
        if 'collection_count' in unquoted:
            continue
        count += 1
        print(count, line_count, line.strip())
