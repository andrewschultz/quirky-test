# this was used to track file name changes and sync variable name changes
# it makes sure references to graphics don't point to something null
# while the compiler catches update_graphics null references, it doesn't catch dynamic_graphics, 

import os
import glob
from collections import defaultdict

need_one = defaultdict(bool)
got_one = defaultdict(bool)

good_prefixes = [ 'r_', 'o_', 's_', 't_', 'ts_' ]

def good_name(x):
	for g in good_prefixes:
		if x.startswith(g):
			return True
	return False

with open("c:/users/andrew/documents/github/quirky-test/source_code.adv") as file:
	for (line_count, line) in enumerate (file, 1):
		if "base64_png" in line:
			a = [x.strip() for x in line.split(':')]
			if a[0] in need_one:
				print("Duplicate base64_png definition {} line {}.".format(a, line_count))
			need_one[a[0]] = True
			continue
		if 'overlay' in line and line.strip().startswith(':'):
			a = [x.strip() for x in line.split('"')]
			got_one[a[1]] = True
		if 'location' in line and 'graphic' in line:
			a = [x.strip() for x in line.split('"')]
			got_one[a[-2]] = True
		if 'dynamic_graphic' in line or 'update_graphic' in line:
			a = [x.strip() for x in line.split('"')]
			for g in a[1::2]:
				if g in got_one:
					print("Duplicate base64_png call {} line {}.".format(g, line_count))
				got_one[g] = True
			continue

ng = set(need_one) - set(got_one)
if ng:
	print("Still need call for", len(ng), ng)
else:
	print("Don't need any base64 calls!")

gn = set(got_one) - set(need_one)
if gn:
	print("Still need definition for", len(gn), gn)
else:
	print("Don't need any base64 definitions!")

allgraf = sorted(set(need_one) | set(got_one))
badgraf = [x for x in allgraf if not good_name(x)]

if not len(badgraf):
	print("All graphics named well!")
else:
	print("Rename", len(badgraf), ', '.join(badgraf))

os.chdir('c:/users/andrew/documents/github/quirky-test/graphics')
u = glob.glob("*.png")

ag2 = [x.replace('_', '-') + '.png' for x in allgraf]

ng = set(ag2) - set(u)
if (ng):
	print("Graphics without files", ng)
else:
	print("All graphics have files!")

gn = set(u) - set(ag2)
if (gn):
	print("Files without graphics", gn)
else:
	print("All files have graphics!")
