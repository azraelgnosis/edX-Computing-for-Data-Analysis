#########################
# Exercise 0
#########################

#########################
# Exercise 1 (x_float_test: 1 point). 
# Create a variable named x_float whose numerical value is one (1) and whose type is floating-point.
#########################

def is_number(x):
    from numbers import Number
    return isinstance(x, Number)

def random_letter():
    from random import choice
    return choice('abcdefghjiklmnopqrstuvwxyz')

def random_string(n, fun=random_letter):
    return ''.join(str(fun()) for _ in range(n))

##################################################

#########################
# Exercise 3    
#########################
def strcat_list(L):
        assert type(L) is list
        
        return list(reversed(L))

#########################
# `strcat_list_test`: Test cell
n = 3
nL = 6
L = [random_string(n) for _ in range(nL)]
Lc = strcat_list(L)
print('L == {}'.format(L))
print('strcat_list(L) == \'{}\''.format(Lc))
assert all([Lc[i*n:(i+1)*n] == L[nL-i-1] for i, x in zip(range(nL), L)])
print("\n(Passed!)")
###########################################################################

"""
def floor_fraction(a, b):
    assert is_number(a) and a >= 0
    assert is_number(b) and b >= 0

    return a // b

#####################
from random import random
a = random()
b = random()
c = floor_fraction(a, b)

print(a)
print(b)
print(c)

print('floor_fraction({}, {} == floor({}) == {}'.format(a, b, a/b, c))
assert a
assert b
print("\n(Passed)")

#################

def ceiling_fraction(a, b):
    assert is_number(a) and a>= 0
    assert is_number(b) and b > 0

    quotient = a / b
    rem = quotient % 1
    Sum = quotient + (1 - rem)
    return int(Sum)

from random import random
a = random()
b = random()
c = ceiling_fraction(a, b)
print('ceiling_fraction({}, {}) == ceiling({}) == {}'.format(a, b, a/b, c))
assert b*(c-1) <= a <= b*c
assert type(c) is int
print("\n(Passed)!")

#########################
# Exercise 6    
#########################
def report_exam_avg(a, b, c):
        assert is_number(a) and is_number(b) and is_number(c)
        avg = (a+b+c)/3
        return "Your average score: {}".format("{:.1f}".format(avg))
#########################


#########################
# `report_exam_avg_test`: Test cell
from random import random
msg = report_exam_avg(100, 95, 80)
print(msg)
assert msg == "Your average score: 91.7"

print("Checking some additional randomly generated cases:")
for i in range(10):
    ex1 = random() * 100 
    ex2 = random() * 100
    ex3 = random() * 100
    msg = report_exam_avg(ex1, ex2, ex3)
    ex_rounded_avg = float(msg.split()[-1])
    abs_err = abs(ex_rounded_avg*3 - (ex1 + ex2 + ex3)) / 3
    print("{}, {}, {} -> '{}' [{}]".format(ex1, ex2, ex3, msg, abs_err))
    assert abs_err <= 0.05

print("\n(Passed!)")
#########################

#########################        
# Output
#########################
##Your average score: 91.7
##Checking some additional randomly generated cases:
##70.38315323374754, 6.453338032208422, 54.231756021639164 -> 'Your average score: 43.7' [0.010584237468303096]
##15.464835996617577, 16.120602423728027, 26.023082211851147 -> 'Your average score: 19.2' [0.0028402107322520465]
##9.901790898595486, 70.26756196921778, 33.572225069562435 -> 'Your average score: 37.9' [0.01385931245857345]
##94.64455303078306, 72.88146278834857, 19.049810686309797 -> 'Your average score: 62.2' [0.008057831519532025]
##27.138223079746727, 78.71422828182666, 46.48946052269325 -> 'Your average score: 50.8' [0.019362705244446943]
##43.08656840630013, 91.8346813214635, 91.56170665696737 -> 'Your average score: 75.5' [0.005681205089662929]
##38.519724163861746, 12.152895606485636, 51.89226237649742 -> 'Your average score: 34.2' [0.011705951051733146]
##33.95949597702986, 27.465709033522945, 60.45767391732184 -> 'Your average score: 40.6' [0.027626309291543787]
##43.06599130879437, 71.45381759943221, 39.933660345538335 -> 'Your average score: 51.5' [0.01551024874502597]
##89.8855134338091, 18.4319696400158, 84.27749984735532 -> 'Your average score: 64.2' [0.0016723596066109774]
##
(Passed!)
"""

#########################
#Exercise 7
#########################
def count_word_lengths(s):
    assert all([x.isalpha() or x == ' ' for x in s])
    assert type(s) is str


##    s += ' '
##    lengths = []
##    i = 0
##    for c in s:        
##        if c.isalpha():
##            i += 1
##        else:
##            if i != 0: lengths.append(i)
##            i = 0

    arr = s.split(' ')
    lengths = []
    for word in arr:
        if word != '':
           lengths.append(len(word))

    return lengths
            

#########################
# `count_word_Lengths_test`: Test cell

# Test 1: Example
qbf_str = 'the quick brown fox jumped over the lazy dog'
qbf_lens = count_word_lengths(qbf_str)
print("Test 1: count_word_lengths('{}') ==".format(qbf_str, qbf_lens))
print(qbf_lens)
assert  qbf_lens == [3, 5, 5, 3, 6, 4, 3, 4, 3]

# Test 2: Random strings
from random import choice # 3.5.2 does not have `choices()` (available in 3.6+)
#return ''.join([choice('abcdefghijklmnopqrstuvwxyz') for _ in range(n)])

def random_letter_or_space(pr_space=0.15):
    from random import choice, random
    is_space = (random() <= pr_space)
    if is_space:
        return ' '
    return random_letter()

S_LEN = 40
W_SPACE = 1 / 6
rand_str = random_string(S_LEN, fun=random_letter_or_space)
rand_lens = count_word_lengths(rand_str)
print("Test 2: count_word_lengths('{}') == '{}'".format(rand_str, rand_lens))
c = 0
while c < len(rand_str) and rand_str[c] == ' ':
    c += 1
for k in rand_lens:
    print(" => '{}'".format (rand_str[c:c+k]))
    assert (c+k) == len(rand_str) or rand_str[c+k] == ' '
    c += k
    while c < len(rand_str) and rand_str[c] == ' ':
        c += 1
        
# Test 3: Empty string
print("Test 3: Empty strings...")
assert count_word_lengths('') == []
assert count_word_lengths(' ') == []
print("\n(Passed!)")
#########################