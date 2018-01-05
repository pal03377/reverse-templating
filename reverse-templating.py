# https://github.com/pal03377/reverse-templating
# reverse-templating.py
# reverse-templating is licensed under MIT.
# https://github.com/pal03377/reverse-templating/blob/master/LICENSE
# author: Paul Schwind
# 2018-01-05
# Reverse templating is a lib to reverse simple templates with {mustache} placeholder notation.
# The main function is get_placeholders_in(template, text, case_sensitive=True), which returns 
# a list of dictionaries that contain all placeholders and all possible values for them so that 
# the template matches at least a part of the text.
# Examples:
# get_placeholders_in("This is a {whatIsThis}.", "This is a test.")
# => [{'whatIsThis': 'test'}]
# get_placeholders_in("What a {adjective} {whatIsThis}!", "What a great tool!")
# => [{'adjective': 'great', 'whatIsThis': 'tool'}]
# get_placeholders_in("What a {adjective} {whatIsThis}!", "WHAT a great tool!") # case sensitive by default => WHAT does not match
# => []
# get_placeholders_in("What a {adjective} {whatIsThis}!", "WHAT a great tool!", case_sensitive=False)
# => [{'adjective': 'great', 'whatIsThis': 'tool'}]
# get_placeholders_in("Here is a {thing} for you: {smiley}", "Here is a smiley for you: :-)") # You'll get multiple possibilities as the lib doesn't know how long the smiley should be.
# => [{'thing': 'smiley', 'smiley': ':'}, {'thing': 'smiley', 'smiley': ':-'}, {'thing': 'smiley', 'smiley': ':-)'}]
# get_dict_with_longest_values(get_placeholders_in(
#     "Here is a {thing} for you: {smiley}", "Here is a smiley for you: :-)"))
# => {'thing': 'smiley', 'smiley': ':-)'}


import re, itertools


def get_all_occurrence_ends(sub, a_str):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start + len(sub)
        start += 1


def is_ascending_sequence(seq):
    """2 same values next to each other not allowed"""
    if seq == []:
        return True
    for index in range(1, len(seq)):
        if seq[index] <= seq[index-1]:
            return False
    return True


def placeholder_find_helper(template, text, case_sensitive=True):
    """
    helper function of get_placeholders_in
    returns list of list of potential placeholders in text
    takes template as a list of strings, between the strings are the placeholders"""
    text_to_search_in = text
    template_to_search_in = template
    if not case_sensitive:
        text_to_search_in = text_to_search_in.lower()
        template_to_search_in = [part.lower() for part in template_to_search_in]
    # get all occurrences of all template text parts
    part_occ = [get_all_occurrence_ends(
        part, text_to_search_in) for part in template_to_search_in]
    # get all combinations with an element from the first
    # part_occ sublist, than with an element from the next one and
    # so on
    combi_occ = itertools.product(*part_occ)
    # filter those out with an ascending number sequence
    # => placeholder indices must be in order
    combi_occ = filter(is_ascending_sequence, combi_occ)
    # trick for later
    template.append("")
    # now make the indices ~great~ text again
    to_return = []
    for placeholder_indices in combi_occ:
        to_return.append([])
        template_index = 0
        if placeholder_indices[0] > 0:
            # text before the 1st placeholder in template, not needed
            # remove it
            template_index = 1
        for p_i_index in range(len(placeholder_indices)):
            placeholder_index = placeholder_indices[p_i_index]
            if p_i_index+1 >= len(placeholder_indices):
                next_placeholder_index = -1
            else:
                next_placeholder_index = placeholder_indices[p_i_index+1]
            # start is placeholder_index,
            # end is next_placeholder_index-len(template[template_index])
            to_return[-1].append(
                text[placeholder_index:(
                    next_placeholder_index-len(template[template_index]))]
            )
            template_index += 1
    return to_return


def get_placeholders_in(template, text, case_sensitive=True):
    """takes a template and a text onto which the template (partly) possibly matches
    and returns a dict of placeholder names and their values
    Placeholders in templates are marked with "{}", e.g. This is {adjective}!
    where {adjective} could be anything (e.g. cool)
    returns a dict with the values being the placeholder names (here: "adjective")
    and the keys the text parts (here: "cool").
    case_sensitive=False ignores the case for the search, but still returns cased values. """
    # seperate the text from the placeholders in template
    seperated = [split_up.split("}") for split_up in template.split("{")]
    # flatten it
    seperated = [a for b in seperated for a in b]
    # now, every second element in seperated is text and the others
    # (with an odd index) are placeholders
    # extract them
    template_text = seperated[::2]
    template_placeholders = seperated[1::2]
    # great, now let's get potential canidates for the placeholders
    potential_placeholders = placeholder_find_helper(
        template_text, text, case_sensitive)
    to_return = []
    for placeholders in potential_placeholders:
        # match the placeholder names onto the potential placeholders
        matched_placeholders = dict(zip(template_placeholders, placeholders))
        # format the text with it
        to_return.append(
            matched_placeholders
        )
    return to_return


def get_values_lengthes(dictionary):
    """returns the sum of the lengthes of values of a dictionary"""
    return sum(map(lambda value: len(value), dictionary.values()))


def sort_by_values_length(dictionaries):
    """looks at the sum of the lengthes of the values of dicts in a list and returns them sorted"""
    return sorted(dictionaries, key=get_values_lengthes)


def get_dict_with_longest_values(dictionaries):
    """returns the dict of a dict list with the longest values (in sum)"""
    return sort_by_values_length(dictionaries)[-1]


def get_dict_with_shortest_values(dictionaries):
    """returns the dict of a dict list with the shortest values (in sum)"""
    return sort_by_values_length(dictionaries)[0]


def apply_vars_to_template(placeholder_vars, template):
    """takes a return value of placeholder_replace and produces strings out of it with the help of the template"""
    to_return = []
    for placeholders in placeholder_vars:
        # match the placeholder names onto the potential placeholders
        matched_placeholders = dict(zip(placeholders0, placeholders))
        # format the text with it
        to_return.append(
            template1.format(**matched_placeholders)
        )
    return to_return


if __name__ == "__main__":
    print(get_placeholders_in("This is a {whatIsThis}.", "This is a test."))
    print(get_placeholders_in("What a {adjective} {whatIsThis}!", "What a great tool!"))
    print(get_placeholders_in("What a {adjective} {whatIsThis}!", "WHAT a great tool!")) # case sensitive by default => WHAT does not match
    print(get_placeholders_in("What a {adjective} {whatIsThis}!", "WHAT a great tool!", case_sensitive=False))
    print(get_placeholders_in("Here is a {thing} for you: {smiley}", "Here is a smiley for you: :-)")) # You'll get multiple possibilities as the lib doesn't know how long the smiley should be.
    print(get_dict_with_longest_values(get_placeholders_in(
        "Here is a {thing} for you: {smiley}", "Here is a smiley for you: :-)")))
