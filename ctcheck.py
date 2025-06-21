# ctcheck.py : checks colored text stuff

import regex as re

with open("source_code.adv") as file:
    for (line_count, line) in enumerate (file, 1):
        if '"' not in line:
            continue
        ary = line.strip().split("\"")[1::2]
        if not ary:
            continue
        quo = ' '.join(ary)
        f = re.findall(r"<[^<>]*?[<>]", quo, overlapped = True)
        if not f:
            continue
        for i in f:
            if '>' not in i:
                continue
            if '<#' in i:
                continue
            if re.search("<[0-9a-fA-F]>", i): # Adventuron default colorings e.g. <TEXT<6>>
                continue
            print("Possible errant <>", i, line_count)
