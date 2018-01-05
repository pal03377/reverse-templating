# reverse-templating (Python)

## Explaination

Reverse templating is a lib to reverse simple templates with {mustache} placeholder notation.

The main function is `get_placeholders_in(template, text, case_sensitive=True)`, which returns 
a list of dictionaries that contain all placeholders and all possible values for them so that 
the template matches at least a part of the text.

## Examples

```
get_placeholders_in("This is a {whatIsThis}.", "This is a test.")
=> [{'whatIsThis': 'test'}]
```
```
get_placeholders_in("What a {adjective} {whatIsThis}!", "What a great tool!")
=> [{'adjective': 'great', 'whatIsThis': 'tool'}]
```
```
get_placeholders_in("What a {adjective} {whatIsThis}!", "WHAT a great tool!") # case sensitive by default => WHAT does not match
=> []
```
```
get_placeholders_in("What a {adjective} {whatIsThis}!", "WHAT a great tool!", case_sensitive=False)
=> [{'adjective': 'great', 'whatIsThis': 'tool'}]
```
```
get_placeholders_in("Here is a {thing} for you: {smiley}", "Here is a smiley for you: :-)") # You'll get multiple possibilities as the lib doesn't know how long the smiley should be.
=> [{'thing': 'smiley', 'smiley': ':'}, {'thing': 'smiley', 'smiley': ':-'}, {'thing': 'smiley', 'smiley': ':-)'}]
```
```
get_dict_with_longest_values(get_placeholders_in(
    "Here is a {thing} for you: {smiley}", "Here is a smiley for you: :-)"))
=> {'thing': 'smiley', 'smiley': ':-)'}
```
