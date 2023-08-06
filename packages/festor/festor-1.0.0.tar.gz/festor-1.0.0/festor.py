##This is the festor.py module, and it provides one function called print_lol() which prints lists that may or may 
##not include nested lists
def print_lol(the_list):
##This function takes a positional argument called "the_list", which is any Python list.  
# Each data item is printed the screen on its own line
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

movies = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Micheal Palin", "John Cleese",
"Terry Gilliam", "Eric Idle", "Terry Jones"]]]

print_lol(movies)
