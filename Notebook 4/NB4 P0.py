def is_valid_strdigit(c, base=2):
    if type (c) is not str: return False # Reject non-string digits
    if (type (base) is not int) or (base < 2) or (base > 36): return False # Reject non-integer bases outside 2-36
    if base < 2 or base > 36: return False # Reject bases outside 2-36
    if len (c) != 1: return False # Reject anything that is not a single character
    if '0' <= c <= str (min (base-1, 9)): return True # Numerical digits for bases up to 10
    if base > 10 and 0 <= ord (c) - ord ('a') < base-10: return True # Letter digits for bases > 10
    return False # Reject everything else

def valid_strdigits(base=2):
    POSSIBLE_DIGITS = '0123456789abcdefghijklmnopqrstuvwxyz'
    return [c for c in POSSIBLE_DIGITS if is_valid_strdigit(c, base)]

def print_valid_strdigits(base=2):
    valid_list = valid_strdigits(base)
    if not valid_list:
        msg = '(none)'
    else:
        msg = ', '.join([c for c in valid_list])
    print('The valid base ' + str(base) + ' digits: ' + msg)

# Quick demo:
print_valid_strdigits(6)
print_valid_strdigits(16)
print_valid_strdigits(23)

################################################################


################################
# Exercise 0
'''Write a function, eval_strint(s, base). It takes a string of digits s in the base given by base. It returns its value as an integer.
That is, this function implements the mathematical object, , which would convert a string to its numerical value, assuming its digits are given in
base.'''
################################

def eval_strint(s, base=2):
    assert type(s) is str
    assert 2 <= base <= 36

    return int(s, base)

################################
# Test: `eval_strint_test0` (1 point)
def check_eval_strint(s, v, base=2):
    v_s = eval_strint(s, base)
    msg = "'{}' -> {}".format (s, v_s)
    print(msg)
    assert v_s == v, "Results do not match expected solution."

# Test 0: From the videos
check_eval_strint('16180339887', 16180339887, base=10)
# Test: `eval_strint_test1` (1 point)
check_eval_strint('100111010', 314, base=2)
# Test: `eval_strint_test2` (1 point)
check_eval_strint('a205b064', 2718281828, base=16)


################################################################


################################
# Exercise 1
'''Suppose a string of digits s in base base contains up to one fractional point. Complete the function, eval_strfrac(s, base), so that it
returns its corresponding floating-point value. Your function should always return a value of type float, even if the input happens to correspond to an exact
integer.'''
################################

def is_valid_strfrac(s, base=2):
    return all([is_valid_strdigit(c, base) for c in s if c != '.']) \
        and (len([c for c in s if c == '.']) <= 1)

def eval_strfrac(s, base=2):
    assert is_valid_strfrac(s, base), "'{}' contains invalid digits for a base-{} number.".format(s, base)
    #s = str(float(s)) # removes trailing/preceding zeroes
    places = len(s) - s.find(".")-1 # find number of decimal places
    if places == len(s): places = 0 # checks if there is no decimal point
    s = s.replace(".", "") # removes decimal point; equivalent to multiplying by number of decimal places
    s = int(s, base) # converts to base 10
    s = s / pow(base, places)
    return s


################################
# Test 0: `eval_strfrac_test0` (1 point)
def check_eval_strfrac(s, v_true, base=2, tol=1e-7):
    v_you = eval_strfrac(s, base)
    assert type(v_you) is float, "Your function did not return a `float` as instructed."
    delta_v = v_you - v_true
    msg = "[{}]_{{{}}} ~= {}: You computed {}, which differs by {}.".format(s, base, v_true,
    v_you, delta_v)

    print(msg)
    assert abs(delta_v) <= tol, "Difference exceeds expected tolerance."

# Test cases from the video
check_eval_strfrac('3.14', 3.14, base=10)
check_eval_strfrac('100.101', 4.625, base=2)
check_eval_strfrac('11.0010001111', 3.1396484375, base=2)

# A hex test case
check_eval_strfrac('f.a', 15.625, base=16)

# Test 1: `eval_strfrac_test1` (1 point)
# Test 2: `eval_strfrac_test2` (2 point)

def check_random_strfrac():
    from random import randint
    b = randint(2, 36) # base
    d = randint(0, 5) # leading digits
    r = randint(0, 5) # trailing digits
    v_true = 0.0
    s = ''
    possible_digits = valid_strdigits(b)
    for i in range(-r, d+1):
        v_i = randint(0, b-1)
        s_i = possible_digits[v_i]

        v_true += v_i * (b**i)
        s = s_i + s
        if i == -1:
            s = '.' + s
    check_eval_strfrac(s, v_true, base=b)

for _ in range(10):
    check_random_strfrac()


################################################################


def print_fp_hex(v):
    assert type(v) is float
    print("v = {} ==> v.hex() == '{}'".format(v, v.hex()))

print_fp_hex(0.0)
print_fp_hex(1.0)
print_fp_hex(16.0625)

################################
# Exercise 2
'''Write a function, fp_bin(v), that determines the IEEE-754 tuple representation of any double-precision floating-point value, v. That is,
given the variable v such that type(v) is float, it should return a tuple with three components, (s_sign, s_bin, v_exp) such that
s_sign is a string representing the sign bit, encoded as either a '+' or '-' character;
s_signif is the significand, which should be a string of 54 bits having the form, x.xxx...x, where there are (at most) 53 x bits (0 or 1 values);
v_exp is the value of the exponent and should be an integer.
'''
################################

def int_to_bin(n):
    digits = ""

    digits += str(n%2)
    n = n//2
    while n > 0:
        digits += str(n%2)
        n = n//2

    return digits[::-1]

hex_dict = {}
for i in range(10):
    hex_dict[str(i)] = int_to_bin(i).zfill(4)
for i in range(6):
    hex_dict[chr(97+i)] = int_to_bin(10+i).zfill(4)

def fp_bin(v, signif_bits=None):
    assert type(v) is float

    s_sign = "-" if str(v)[0] == "-" else "+"
    v_hex = v.hex()
    v_exp = int(v_hex[v_hex.find("p")+1:])

    s_signif = "1." if v != 0 else "0."
    for i in v_hex[v_hex.find(".")+1:v_hex.find("p")]:
        s_signif += hex_dict[i]
    s_signif = s_signif.ljust(54, "0")
    if signif_bits != None: s_signif = s_signif[:signif_bits+1]
    #s_signif = "{0:03s}".format(s_signif)

    return (s_sign, s_signif, v_exp)

################################
# Test: `fp_bin_test0` (2 points)
def check_fp_bin(v, x_true):
    x_you = fp_bin(v)
    print("""{} [{}] ==
        {}
        vs. you: {}
        """.format(v, v.hex(), x_true, x_you))
    assert x_you == x_true, "Results do not match!"

check_fp_bin(0.0, ('+', '0.0000000000000000000000000000000000000000000000000000', 0))
check_fp_bin(-0.1, ('-', '1.1001100110011001100110011001100110011001100110011010', -4))
check_fp_bin(1.0 + (2**(-52)), ('+', '1.0000000000000000000000000000000000000000000000000001', 0))

# Test: `fp_bin_test1` (2 points)
check_fp_bin(-1280.03125, ('-', '1.0100000000000010000000000000000000000000000000000000', 10))
check_fp_bin(6.2831853072, ('+', '1.1001001000011111101101010100010001001000011011100000', 2))
check_fp_bin(-0.7614972118393695, ('-', '1.1000010111100010111101100110100110110000110010000000', -1))

################################
# Exercise 3
'''
Suppose you are given a floating-point value in a base given by base and in the form of the tuple, (sign, significand, exponent),
where
sign is either the character '+' if the value is positive and '-' otherwise;
significand is a string representation in base-base;
exponent is an integer representing the exponent value.

Complete the function,
    def eval_fp(sign, significand, exponent, base):
        ...
so that it converts the tuple into a numerical value (of type float) and returns it.
'''
################################

def whole_to_int(n, base):
    num = 0
    for index, i in enumerate(n[::-1]):
        num += int(i)*pow(base, index)

    return num

def frac_to_int(f, base):
    n = 0
    for index, i in enumerate(f):
        n += int(i) * pow(base, -1*index-1)

    return n

def eval_fp(sign, significand, exponent, base=2):
    assert sign in ['+', '-'], "Sign bit must be '+' or '-', not '{}'.".format(sign)
    assert is_valid_strfrac(significand, base), "Invalid significand for base-{}: '{}'".format(base, significand)
    assert type(exponent) is int

    sign = -1 if sign == "-" else 1

    whole_num = "1"+significand[2:2+exponent] if exponent >= 0 else "0"
    whole_num = whole_to_int(whole_num, base)
    frac_num = significand[exponent+2:] if exponent >= 0 else (-1*exponent-1)*"0" + "1" + significand[2:]
    frac_num = frac_to_int(frac_num, base)

    result = sign*(whole_num + frac_num)
    return result

################################
# Test: `eval_fp_test0` (1 point)
def check_eval_fp(sign, significand, exponent, v_true, base=2, tol=1e-7):
    v_you = eval_fp(sign, significand, exponent, base)
    delta_v = v_you - v_true
    msg = "('{}', ['{}']_{{{}}}, {}) ~= {}: You computed {}, which differs by {}.".format(sign, significand, base, exponent, v_true, 0, 0)
    print(msg)
    assert abs(delta_v) <= tol, "Difference exceeds expected tolerance."

# Test 0: From the videos
check_eval_fp('+', '1.25000', -1, 0.125, base=10)

# Test: `eval_fp_test1` -- Random floating-point binary values (1 point)
def gen_rand_fp_bin():
    from random import random, randint
    v_sign = 1.0 if (random() < 0.5) else -1.0
    v_mag = random() * (10**randint(-5, 5))
    v = v_sign * v_mag
    s_sign, s_bin, s_exp = fp_bin(v)
    return v, s_sign, s_bin, s_exp

for _ in range(5):
    (v_true, sign, significand, exponent) = gen_rand_fp_bin()
    check_eval_fp(sign, significand, exponent, v_true, base=2)

################################
# Exercise 4
'''
Suppose you are given two binary floating-point values, u and v, in the tuple form given above. That is, u == (u_sign, u_signif,
u_exp) and v == (v_sign, v_signif, v_exp), where the base for both u and v is two (2). Complete the function add_fp_bin(u, v, signif_bits), so
that it returns the sum of these two values with the resulting significand truncated to signif_bits digits.
'''
################################

def add_fp_bin(u, v, signif_bits):
    u_sign, u_signif, u_exp = u
    v_sign, v_signif, v_exp = v

    # You may assume normalized inputs at the given precision, `signif_bits`.
    assert u_signif[:2] == '1.' and len(u_signif) == (signif_bits+1)
    assert v_signif[:2] == '1.' and len(v_signif) == (signif_bits+1)

    alpha = eval_fp(u_sign, u_signif, u_exp)
    beta = eval_fp(v_sign, v_signif, v_exp)
    Sum = alpha + beta
    Bin = fp_bin(Sum, signif_bits)
    return Bin

# Test: `add_fp_bin_test`
def check_add_fp_bin(u, v, signif_bits, w_true):
    w_you = add_fp_bin(u, v, signif_bits)
    msg = "{} + {} == {}: You produced {}.".format(u, v, w_true, w_you)
    print(msg)
    assert w_you == w_true, "w_you: {} != w_true {} Results do not match.".format(w_you, w_true)

u = ('+', '1.010010', 0)
v = ('-', '1.000000', -2)
w_true = ('+', '1.000010', 0)
check_add_fp_bin(u, v, 7, w_true)

u = ('+', '1.00000', 0)
v = ('+', '1.00000', -5)
w_true = ('+', '1.00001', 0)
check_add_fp_bin(u, v, 6, w_true)

u = ('+', '1.00000', 0)
v = ('-', '1.00000', -5)
w_true = ('+', '1.11110', -1)
check_add_fp_bin(u, v, 6, w_true)

u = ('+', '1.00000', 0)
v = ('+', '1.00000', -6)
w_true = ('+', '1.00000', 0)
check_add_fp_bin(u, v, 6, w_true)

u = ('+', '1.00000', 0)
v = ('-', '1.00000', -6)
w_true = ('+', '1.11111', -1)
check_add_fp_bin(u, v, 6, w_true)