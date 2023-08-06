"""This is the standard way to make a recurion to print multiple lists in
some separate lists"""

movies = [
    "동주", 2016, "극한직업", 2019,
    ["류승룡",
     ["이하늬", "김인석", "박정민"]]]

"""Below is an example of recursion function that calls lists
no matter how many lists the top list has uner itself"""

def print_lol(the_list):
	for each in the_list:
		if isinstance(each, list):
			print_lol(each)
		else: print(each)
