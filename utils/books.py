# books.py: a utility designed to verify the bookshelf books in Quirky Test are different enough
# What does it do?
# 1. keeps track of words any 2 books have in common
# 2. keeps track of the same words within a set of 17 books and notes any duplicates
# 3. notes any similar 2-word sequence
# 4. notes if some books are rearrangements of others (sort of like 3, but with additional rigor) e.g. "Simon My Son" and "My Son Simon" are flagged
#
# Some exceptions here include the same word on 1 line, like the final "big" title Burt Had Hurt Bad, Dirt Had Hurt Dad
#
# There is no ignored words list, but there could be, for 'a'
#
# There is also reference to an auxiliary file.
#

import sys
import os
import re

from collections import defaultdict
import mytools as mt

aux_file = "c:/users/andrew/documents/github/quirky-test/utils/books-from.txt"
source_file = "c:/users/andrew/documents/github/quirky-test/source_code.adv"

flaggables = sys.argv[1:]

def title_to_array(my_string):
    return [x for x in re.split("[^a-zA-Z']+", my_string) if x]

def array_to_title(my_array):
    return ' '.join(my_array).title()

def check_auxiliary_file(aux_file):
    if not os.path.exists(aux_file):
        print("Can't find", aux_file)
        return
    with open(aux_file) as file:
        for (line_count, line) in enumerate (file, 1):
            if not re.search("[0-9]", line):
                continue
            l2 = mt.zap_comment(line.lower())
            l2 = re.sub("[^a-zA-Z0-9 ]", "", l2)
            word_array = [x for x in l2.split(' ') if re.search('[a-zA-Z]', x)]
            sorted_array = '/'.join(sorted(word_array))
            final_title = array_to_title(word_array)
            if final_title in book_set:
                mt.warn("Duplicate title in {}: {} line {}".format(aux_file, final_title, line_count))
            elif final_title in book_set_aux:
                mt.warn("AUXILIARY Duplicate title {} line {}".format(final_title, line_count))
            elif sorted_array in books_sorted:
                mt.warn("Reshuffled duplicate {}/{} line {} = {}".format(sorted_array, books_sorted[sorted_array], line_count, final_title))
            word_flags = set(word_array) & set(flaggables)
            if word_flags:
                mt.okay("FLAGGED to-read keyword(s) {} / {} line {}".format(word_flags, final_title, line_count))
            book_set_aux.add(final_title)
            books_sorted[sorted_array].append(final_title)

book_count = 0
books = defaultdict(list)
books_sorted = defaultdict(list)

pair_lines = defaultdict(int)

book_set = set()
book_set_aux = set()

this_shelf_dict = defaultdict(int)

with open(source_file) as file:
    for (line_count, line) in enumerate (file, 1):
        if line.rstrip().startswith('      }'):
            this_shelf_dict.clear()
        if "book_is" not in line and 'final book' not in line: continue
        if "print" not in line: continue
        if re.search("[\?!\.]<#ff0>>\.", line.lower()):
            ary = line.split('"')
            mt.warn("BAD BOOK PUNCTUATION LINE {} {}".format(line_count, ary[1]))
        ary_init = line.lower().split('<')
        book_count += 1
        word_array = title_to_array(ary_init[1])
        sorted_array = '/'.join(sorted(word_array))
        final_title = array_to_title(word_array)
        word_flags = set(word_array) & set(flaggables)
        for w in word_array:
            if w in this_shelf_dict and this_shelf_dict[w] != line_count:
                mt.warn("TRIVIAL WARNING: {} is repeated in bookshelf at line {}, originally {}.".format(w, line_count, this_shelf_dict[w]))
            else:
                this_shelf_dict[w] = line_count
        if word_flags:
            mt.okay("FLAGGED source keyword(s) {} / {} line {}".format(word_flags, final_title, line_count))
        if final_title in book_set:
            mt.fail("Duplicate book internal to source", final_title)
        else:
            book_set.add(final_title)
            for w in word_array:
                books[w].append(final_title)
            if sorted_array in books_sorted:
                mt.warn("Reshuffled duplicate {}/{} line {} = {}".format(sorted_array, books_sorted[sorted_array], line_count, final_title))
            else:
                for x in range(0, len(word_array)):
                    temp_string = "{} {}".format(word_array[x], word_array[(x+1) % len(word_array)])
                    if temp_string in pair_lines:
                        mt.warn("Duplicate word pair: {} lines {}/{}".format(temp_string, pair_lines[temp_string], line_count))
                    else:
                        pair_lines[temp_string] = line_count
            books_sorted[sorted_array].append(final_title)

print(book_count, "total books in source")

for b in sorted(books, key=lambda x:(len(books[x]), x)):
    if len(books[b]) > 1:
        print("({}): {:7} = {}".format(len(books[b]), b, ' / '.join([u.title() for u in books[b]])))

check_auxiliary_file(aux_file)
