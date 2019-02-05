text = "sgtEEEr2020.0"

# Strings have methods for checking "global" string properties
print("1.", text.isalpha())

# These can also be applied per character
print("2.", [c.isalpha() for c in text])

# Here are a bunch of additional useful methods
print("BELOW: (global) -> (per character)")
print(text.isdigit(), "-->", [c.isdigit() for c in text])
print(text.isspace(), "-->", [c.isspace() for c in text])
print(text.islower(), "-->", [c.islower() for c in text])
print(text.isupper(), "-->", [c.isupper() for c in text])

################################
# Exercise 0
'''
Create a new function that checks whether a given input string is a properly formatted social security number, i.e., has the pattern, XXX-XX-XXXX, including the separator dashes, where each X is a digit. It should return True if so or False otherwise.
'''
################################

def is_ssn(s):
    a = s.split("-")
    if len(a) is not 3: return False # checks if there are three parts separated by a hyphen
    if len(a[0]) is not 3 or len(a[1]) is not 2 or len(a[2]) is not 4: return False # checks that each part has the current number of characters
    
    # checks that each character in each part is a digit
    for i in a:
        for j in i:
            if not j.isdigit(): return False

    return True

################################
# Test cell: `is_snn_test`
assert is_ssn('832-38-1847')
assert not is_ssn('832 -38 -  1847')
assert not is_ssn('832-bc-3847')
assert not is_ssn('832381847')
assert not is_ssn('8323-8-1847')
assert not is_ssn('abc-de-ghij')
print("\n(Passed!)")

################################################################

import re

pattern = 'fox'
pattern_matcher = re.compile(pattern)

input = 'The quick brown fox jumps over the lazy dog'
matches = pattern_matcher.search(input)
print(matches)

print(matches.group())
print(matches.start())
print(matches.end())
print(matches.span())

matches_2 = re.search ('jump', input)
assert matches_2 is not None
print ("Found", matches_2.group (), "@", matches_2.span ())

# Make the expression more readable with a re.VERBOSE pattern
re_names2 = re.compile ('''^              # Beginning of string
                           ([a-zA-Z]+)    # First name
                           \s+            # At least one space
                           ([a-zA-Z]+\s)? # Optional middle name
                           ([a-zA-Z]+)    # Last name
                           $              # End of string
                        ''',
                        re.VERBOSE)
print (re_names2.match ('Rich Vuduc').groups ())
print (re_names2.match ('Rich S Vuduc').groups ())
print (re_names2.match ('Rich Salamander Vuduc').groups ())

# Named groups
re_names3 = re.compile ('''^
                           (?P<first>[a-zA-Z]+)
                           \s
                           (?P<middle>[a-zA-Z]+\s)?
                           \s*
                           (?P<last>[a-zA-Z]+)
                           $
                        ''',
                        re.VERBOSE)
print (re_names3.match ('Rich Vuduc').group ('first'))
print (re_names3.match ('Rich S Vuduc').group ('middle'))
print (re_names3.match ('Rich Salamander Vuduc').group ('last'))


################################
# Exercise 1
'''
Write a function parse_email that, given an email address s, returns a tuple, (user-id, domain) corresponding to the user name and domain name.

For instance, given `richie@cc.gatech.eduit should return(richie, cc.gatech.edu)`.

Your function should parse the email only if it exactly matches the email specification. For example, if there are leading or trailing spaces, the function should not match those. See the test cases for examples.

If the input is not a valid email address, the function should raise a ValueError.
'''
################################

def parse_email (s):
    """Parses a string as an email address, returning an (id, domain) pair."""
    
    if re.match("^[A-z][A-z0-9._-]*@[A-z0-9._-]*[A-z]$", s) is not None:
        return tuple(s.split("@"))
    else:
        raise ValueError

################################
# Test cell: `parse_email_test`

def pass_case(u, d):
    s = u + '@' + d
    msg = "Testing valid email: '{}'".format(s)
    print(msg)
    assert parse_email(s) == (u, d), msg
    
pass_case('richie', 'cc.gatech.edu')
pass_case('bertha_hugely', 'sampson.edu')
pass_case('JKRowling', 'Huge-Books.org')

def fail_case(s):
    msg = "Testing invalid email: '{}'".format(s)
    print(msg)
    try:
        parse_email(s)
    except ValueError:
        print("==> Correctly throws an exception!")
    else:
        raise AssertionError("Should have, but did not, throw an exception!")
        
fail_case('x @hpcgarage.org')
fail_case('   quiggy.smith38x@gmail.com')
fail_case('richie@cc.gatech.edu  ')
fail_case('4test@gmail.com')
fail_case('richie@cc.gatech.edu7')

print("Passed")


################################################################


################################
# Exercise 2
'''
Write a function to parse US phone numbers written in the canonical "(404) 555-1212" format, i.e., a three-digit area code enclosed 
in parentheses followed by a seven-digit local number in three-hyphen-four digit format. It should also ignore all leading and trailing spaces, 
as well as any spaces that appear between the area code and local numbers. However, it should not accept any spaces in the 
area code (e.g., in '(404)') nor should it in the seven-digit local number.

It should return a triple of strings, (area_code, first_three, last_four).

If the input is not a valid phone number, it should raise a ValueError.
'''
################################

""" def parse_phone1 (s):
    if re.match("( *)?\(\d{3}\)( *)?\d{3}-\d{4}( *)?", s) is not None:
        area_code = s.split(")")[0][-3:]
        num = s.split("-")
        first_three = num[0][-3:]
        last_four = num[1][:4]
        return (area_code, first_three, last_four)
    else:
        raise ValueError """

def parse_phone1 (s):
    re_num = re.compile(" *\((?P<area_code>\d{3})\) *(?P<first_three>\d{3})-(?P<last_four>\d{4}) *")
    num = re_num.match(s)
    if num: 
        return(num.group("area_code"), num.group("first_three"), num.group("last_four"))
    else:
        raise ValueError

# Test cell: `parse_phone1_test`

def rand_spaces(m=5):
    from random import randint
    return ' ' * randint(0, m)

def asm_phone(a, l, r):
    return rand_spaces() + '(' + a + ')' + rand_spaces() + l + '-' + r + rand_spaces()

def gen_digits(k):
    from random import choice # 3.5 compatible; 3.6 has `choices()`
    DIGITS = '0123456789'
    return ''.join([choice(DIGITS) for _ in range(k)])

def pass_phone(p=None, a=None, l=None, r=None):
    if p is None:
        a = gen_digits(3)
        l = gen_digits(3)
        r = gen_digits(4)
        p = asm_phone(a, l, r)
    else:
        assert a is not None and l is not None and r is not None, "Need to supply sample solution."
    msg = "Should pass: '{}'".format(p)
    print(msg)
    p_you = parse_phone1(p)
    assert p_you == (a, l, r), "Got {} instead of ('{}', '{}', '{}')".format(p_you, a, l, r)
    
def fail_phone(s):
    msg = "Should fail: '{}'".format(s)
    print(msg)
    try:
        p_you = parse_phone1(s)
    except ValueError:
        print("==> Correctly throws an exception.")
    else:
        raise AssertionError("Failed to throw a `ValueError` exception!")


# Cases that should definitely pass:
pass_phone('(404) 121-2121', '404', '121', '2121')
pass_phone('(404)121-2121', '404', '121', '2121')
for _ in range(5):
    pass_phone()
    
fail_phone("404-121-2121")
fail_phone('(404)555 -1212')
fail_phone(" ( 404)121-2121")
fail_phone("(abc) def-ghij")

print("Pass")


################################################################


################################
# Exercise 3
'''
Implement an enhanced phone number parser that can handle any of these patterns.
    (404) 555-1212
    (404) 5551212
    404-555-1212
    404-5551212
    404555-1212
    4045551212
As before, it should not be sensitive to leading or trailing spaces. Also, for the patterns in which the area code is enclosed in parentheses, it should not be sensitive to the number of spaces separating the area code from the remainder of the number.
'''
################################

def parse_phone2 (s):
    re_num = re.compile("^ *(\((?P<area_code1>\d{3})\)[ ]*|(?P<area_code2>\d{3}))[-]*(?P<first_three>\d{3})[-]*(?P<last_four>\d{4}) *")
    num = re_num.match(s)

    if num is not None:
        return (num.group("area_code1") or num.group("area_code2"), num.group("first_three"), num.group("last_four"))
    else:
        raise ValueError

################################
# Test cell: `parse_phone2_test`

def asm_phone2(a, l, r):
    from random import random
    x = random()
    if x < 0.33:
        a2 = '(' + a + ')' + rand_spaces()
    elif x < 0.67:
        a2 = a + '-'
    else:
        a2 = a
    y = random()
    if y < 0.5:
        l2 = l + '-'
    else:
        l2 = l
    return rand_spaces() + a2 + l2 + r + rand_spaces()

def pass_phone2(p=None, a=None, l=None, r=None):
    if p is None:
        a = gen_digits(3)
        l = gen_digits(3)
        r = gen_digits(4)
        p = asm_phone2(a, l, r)
    else:
        assert a is not None and l is not None and r is not None, "Need to supply sample solution."
    msg = "Should pass: '{}'".format(p)
    print(msg)
    p_you = parse_phone2(p)
    assert p_you == (a, l, r), "Got {} instead of ('{}', '{}', '{}')".format(p_you, a, l, r)
    
pass_phone2("  (404)   555-1212  ", '404', '555', '1212')
pass_phone2("(404)555-1212  ", '404', '555', '1212')
pass_phone2("  404-555-1212 ", '404', '555', '1212')
pass_phone2("  404-5551212 ", '404', '555', '1212')
pass_phone2(" 4045551212", '404', '555', '1212')
    
for _ in range(5):
    pass_phone2()
    
    
def fail_phone2(s):
    msg = "Should fail: '{}'".format(s)
    print(msg)
    try:
        parse_phone2 (s)
    except ValueError:
        print ("==> Function correctly raised an exception.")
    else:
        raise AssertionError ("Function did *not* raise an exception as expected!")
        
failure_cases = ['+1 (404) 555-3355',
                 '404.555.3355',
                 '404 555-3355',
                 '404 555 3355',
                 '(404-555-1212'
                ]
for s in failure_cases:
    fail_phone2(s)
    
print("\n(Pass)")