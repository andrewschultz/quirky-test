This is a collection of utilities that helped me do code inspections or make sure there were no stray variables or calls to null strings.

Adventuron is forgiving of code such as "{non_existent_string}", which is nice to compile, but not so nice when blank text appears. So collected here are some useful utilities.

GENERAL CHECKS
* b64.py: checks base 64 graphics and makes sure 1) each graphic is referred to elsewhere and 2) any call to a graphic doesn't go to a null graphic

GAME SPECIFIC CHECKS
* half.py: compares walkthrough.txt to the code. Currently it looks for point-scoring lines and makes sure we have code that defects half-right. For instance, for Turkey Quest, it makes sure we have "turkey _" and "_ quest".