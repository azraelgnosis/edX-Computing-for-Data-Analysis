from collections import defaultdict

latin_text = """
Sed ut perspiciatis, unde omnis iste natus error sit
voluptatem accusantium doloremque laudantium, totam
rem aperiam eaque ipsa, quae ab illo inventore
veritatis et quasi architecto beatae vitae dicta
sunt, explicabo. Nemo enim ipsam voluptatem, quia
voluptas sit, aspernatur aut odit aut fugit, sed
quia consequuntur magni dolores eos, qui ratione
voluptatem sequi nesciunt, neque porro quisquam est,
qui dolorem ipsum, quia dolor sit amet consectetur
adipisci[ng] velit, sed quia non numquam [do] eius
modi tempora inci[di]dunt, ut labore et dolore
magnam aliquam quaerat voluptatem. Ut enim ad minima
veniam, quis nostrum exercitationem ullam corporis
suscipit laboriosam, nisi ut aliquid ex ea commodi
consequatur? Quis autem vel eum iure reprehenderit,
qui in ea voluptate velit esse, quam nihil molestiae
consequatur, vel illum, qui dolorem eum fugiat, quo
voluptas nulla pariatur?
At vero eos et accusamus et iusto odio dignissimos
ducimus, qui blanditiis praesentium voluptatum
deleniti atque corrupti, quos dolores et quas
molestias excepturi sint, obcaecati cupiditate non
provident, similique sunt in culpa, qui officia
deserunt mollitia animi, id est laborum et dolorum
fuga. Et harum quidem rerum facilis est et expedita
distinctio. Nam libero tempore, cum soluta nobis est
eligendi optio, cumque nihil impedit, quo minus id,
quod maxime placeat, facere possimus, omnis voluptas
assumenda est, omnis dolor repellendus. Temporibus
autem quibusdam et aut officiis debitis aut rerum
necessitatibus saepe eveniet, ut et voluptates
repudiandae sint et molestiae non recusandae. Itaque
earum rerum hic tenetur a sapiente delectus, ut aut
reiciendis voluptatibus maiores alias consequatur
aut perferendis doloribus asperiores repellat.
"""

################
# Exercise 1
""" Complete the following function, normalize_string(s). The input s is a string (str object). The function
should return a new string with (a) all characters converted to lowercase and (b) all non-alphabetic, non-whitespace characters removed."""
################

def normalize_string(s):
    assert type (s) is str

    s = s.lower()

    replacements = {
        ",": "",
        ".": "",
        "[": "",
        "]": "",
        "?": "",
        "'": "",
        ":": "",
        "-": "",
        ";": "",
        "\n": " ",
        "\t": " "
    }

    new_str = ""

    '''     for i in s:
        if not (i.isspace() or i.isalpha()):
            continue
        else:
            new_str = "".join([new_str, i]) '''

    '''for i in s:
        if i.isspace() or i.isalpha():
            new_str = "".join([new_str, i])'''

    new_str = "".join([replacements.get(c, c) for c in s])

    return new_str

# `normalize_string_test`: Test cell
norm_latin_text = normalize_string(latin_text)
assert type(norm_latin_text) is str
assert len(norm_latin_text) == 1693 # originally said 1694 but I'm not sure
assert all([c.isalpha() or c.isspace() for c in norm_latin_text])
assert norm_latin_text == norm_latin_text.lower()

###############################################################

################
# Exercise 2
# Implement the following function, get_normalized_words(s). It takes as input a string s (i.e., a strobject). It should return a list of the words in s,
################

def get_normalized_words(s):
    assert type (s) is str

    s = normalize_string(s)
    #s = " ".join(s.split())
    #s = " ".join(s.splitlines(False))
    s = s.split()

    return s

################
# `get_normalized_words_test`: Test cell
norm_latin_words = get_normalized_words(norm_latin_text)

assert len(norm_latin_words) == 250
for i, w in [(20, 'illo'), (73, 'eius'),(144, 'deleniti'), (248, 'asperiores')]:
    assert norm_latin_words[i] == w

###############################################################

################
# Exercise 3
'''Implement a function, make_itemsets(words). The input, words, is a list of strings. Your function should convert
the characters of each string into an itemset and then return the list of all itemsets. These output itemsets should appear in the same order as their
corresponding words in the input.'''
################

def make_itemsets(words):
    assert type(words) is list

    itemset = []

    for index, word in enumerate(words):
        itemset.append(set())
        for letter in word:
            if letter not in itemset[index]:
                itemset[index].add(letter)

    
    return itemset


# `make_itemsets_test`: Test cell
norm_latin_itemsets = make_itemsets(norm_latin_words)

# Lists should have the same size
assert len(norm_latin_itemsets) == len(norm_latin_words)

# Test a random sample
from random import sample
for i in sample(range(len(norm_latin_words)), 5):
    print('[{}]'.format(i), norm_latin_words[i], "-->", norm_latin_itemsets[i])
    assert set(norm_latin_words[i]) == norm_latin_itemsets[i]

###############################################################

################
# Exercise 4
'''Start by implementing a function that enumerates all item-pairs within an itemset and updates, in-place, a
table that tracks the counts of those item-pairs.
The signature of this function is:

def update_pair_counts(pair_counts, itemset):
    ... 

where pair_counts is the table to update and itemset is the itemset from which you need to enumerate item-pairs. You may assume pair_counts is a
default dictionary. Each key is a pair of items (a, b), and each value is the count. You may assume all items in itemset'''
################

def update_pair_counts(pair_counts, itemset):
    """
    Updates a dictionary of pair counts for
    all pairs of items in a given itemset.
    """
    assert type (pair_counts) is defaultdict

    for i in itemset:
        for j in itemset:
            if i is not j:
                pair_counts[(i, j)] += 1
                #pair_counts[(j, i)] += 1 


################
# `update_pair_counts_test`: Test cell
itemset_1 = set("error")
itemset_2 = set("dolor")
pair_counts = defaultdict(int)

update_pair_counts(pair_counts, itemset_1)
assert len(pair_counts) == 6
update_pair_counts(pair_counts, itemset_2)
assert len(pair_counts) == 16

print('"{}" + "{}"\n==> {}'.format (itemset_1, itemset_2, pair_counts))
for a, b in pair_counts:
    assert (b, a) in pair_counts
    assert pair_counts[(a, b)] == pair_counts[(b, a)]


###############################################################

################
# Exercise 5
'''Implement a procedure that, given an itemset, updates a table to track counts of each item.
As with the previous exercise, you may assume all items in the given itemset (itemset) are distinct, i.e., that you may treat it as you would any set-like
collection. You may also assume the table (item_counts) is a default dictionary.'''
################

def update_item_counts(item_counts, itemset):
    for i in itemset:
        item_counts[i] += 1

# `update_item_counts_test`: Test cell
itemset_1 = set("error")
itemset_2 = set("dolor")
item_counts = defaultdict(int)
update_item_counts(item_counts, itemset_1)
assert len(item_counts) == 3
update_item_counts(item_counts, itemset_2)
assert len(item_counts) == 5
assert item_counts['d'] == 1
assert item_counts['e'] == 1
assert item_counts['l'] == 1
assert item_counts['o'] == 2
assert item_counts['r'] == 2


###############################################################

################
# Exercise 6
'''Given tables of item-pair counts and individual item counts, as well as a confidence threshold, return the
rules that meet the threshold. The returned rules should be in the form of a dictionary whose key is the tuple, (a, b), corresponding to the rule a=>b,
and whose value is the confidence of the rule, conf(a=>b).
You may assume that if (a,b) is in the table of item-pair counts, then both a and b are in the table of individual item counts.'''
################

def filter_rules_by_conf(pair_counts, item_counts, threshold):
    rules = {} # (item_a, item_b) -> conf (item_a => item_b)

    for i in pair_counts:
        conf = pair_counts[i] / item_counts[i[0]]
        if conf >= threshold:
            rules[i] = conf

    return rules

# `filter_rules_by_conf_test`: Test cell
pair_counts = {('man', 'woman'): 5,
    ('bird', 'bee'): 3,
    ('red fish', 'blue fish'): 7}
item_counts = {'man': 7,
    'bird': 9,
    'red fish': 11}
rules = filter_rules_by_conf (pair_counts, item_counts, 0.5)
print("Found these rules:", rules)
assert ('man', 'woman') in rules
assert ('bird', 'bee') not in rules
assert ('red fish', 'blue fish') in rules

def gen_rule_str(a, b, val=None, val_fmt='{:.3f}', sep=" = "):
    text = "{} => {}".format(a, b)
    if val:
        text = "conf(" + text + ")"
        text += sep + val_fmt.format(val)
    return text

def print_rules(rules):
    if type(rules) is dict or type(rules) is defaultdict:
        from operator import itemgetter
        ordered_rules = sorted(rules.items(), key=itemgetter(1), reverse=True)
    else: # Assume rules is iterable
        ordered_rules = [((a, b), None) for a, b in rules]
    for (a, b), conf_ab in ordered_rules:
        print(gen_rule_str(a, b, conf_ab))

        
###############################################################


################
# Exercise 7
'''Using the building blocks you implemented above, complete a function find_assoc_rules so that it
implements the basic association rule mining algorithm and returns a dictionary of rules.
In particular, your implementation may assume the following:
1. As indicated in its signature, below, the function takes two inputs: receipts and threshold.
2. The input, receipts, is a collection of itemsets: for every receipt r in receipts, r may be treated as a collection of unique items.
3. The input threshold is the minimum desired confidence value. That is, the function should only return rules whose confidence is at least threshold.
The returned dictionary, rules, should be keyed by tuples corresponding to the rule ; each value should the the confidence
of the rule.'''
################

def find_assoc_rules(receipts, threshold):
    # get items sets
    item_sets = make_itemsets(receipts)

    # gets pair counts
    pair_count = defaultdict(int)
    for i in item_sets:
        update_pair_counts(pair_count, i)

    # gets item counts
    item_count = defaultdict(int)
    for i in receipts:
        update_item_counts(item_count, i)

    # filter rules
    return filter_rules_by_conf(pair_count, item_count, threshold)

################
# `find_assoc_rules_test`: Test cell
receipts = [set('abbc'), set('ac'), set('a')]
rules = find_assoc_rules(receipts, 0.6)
print("Original receipts as itemsets:", receipts)
print("Resulting rules:")
print_rules(rules)
assert ('a', 'b') not in rules
assert ('b', 'a') in rules
assert ('a', 'c') in rules
assert ('c', 'a') in rules
assert ('b', 'c') in rules
assert ('c', 'b') not in rules


###############################################################


################
# Exercise 8
'''For the Latin string, latin_text, use your find_assoc_rules() function to compute the rules whose confidence is
at least 0.75. Store your result in a variable named latin_rules.'''
################


latin_rules = find_assoc_rules(norm_latin_itemsets, 0.75)

# `latin_rules_test`: Test cell
assert len(latin_rules) == 10, "latin_rules length = {}".format(len(latin_rules))
assert all([0.75 <= v <= 1.0 for v in latin_rules.values()])
#for ab in ['xe', 'qu', 'hi', 'xi', 'vt', 're', 've', 'fi', 'gi', 'bi']:
#    assert (ab[0], ab[1]) in latin_rules

english_text = """
But I must explain to you how all this mistaken idea of denouncing of a pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammeled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.
"""

###############################################################


################
# Exercise 9
'''Write a function that, given two dictionaries, finds the intersection of their keys.
'''
################
def intersect_keys(d1, d2):
    assert type(d1) is dict or type(d1) is defaultdict
    assert type(d2) is dict or type(d2) is defaultdict

    intersection = [] #defaultdict(int)
    for i in d1:
        if i in d2:
            intersection.append(i)

    return intersection

# `intersect_keys_test`: Test cell
from random import sample

key_space = {'ape', 'baboon', 'bonobo', 'chimp', 'gorilla', 'monkey', 'orangutan'}
val_space = range(100)

for trial in range(10): # Try 10 random tests
    d1 = {k: v for k, v in zip(sample(key_space, 4), sample(val_space, 4))}
    d2 = {k: v for k, v in zip(sample(key_space, 3), sample(val_space, 3))}
    k_common = intersect_keys(d1, d2)
    for k in key_space:
        is_common = (k in k_common) and (k in d1) and (k in d2)
        is_not_common = (k not in k_common) and ((k not in d1) or (k not in d2))
        assert is_common or is_not_common


###############################################################


################
# Exercise 10
'''Let's consider any rules with a confidence of at least 0.75 to be a "high-confidence rule."
Write some code that finds all high-confidence rules appearing in both the Latin text and the English text. Store your result in a list
named common_high_conf_rules whose elements are (a, b)(a,b) pairs corresponding to the rules a ⇒ b a⇒b.
'''
################

norm_english_words = get_normalized_words(english_text)
english_rules = find_assoc_rules(norm_english_words, 0.75)
common_high_conf_rules = intersect_keys(latin_rules, english_rules)
print("High-confidence rules common to _lorem ipsum_ in Latin and English:")

################
# `common_high_conf_rules_test`: Test cell
assert len(common_high_conf_rules) == 2
assert ('x', 'e') in common_high_conf_rules
assert ('q', 'u') in common_high_conf_rules


###############################################################


""" def on_vocareum():
    import os
    return os.path.exists('.voc')

def download(file, local_dir="", url_base=None, checksum=None):
    import os, requests, hashlib, io
    local_file = "{}{}".format(local_dir, file)
    if not os.path.exists(local_file):
        if url_base is None:
            url_base = "https://cse6040.gatech.edu/datasets/"
        url = "{}{}".format(url_base, file)
        print("Downloading: {} ...".format(url))
        r = requests.get(url)
        with open(local_file, 'wb') as f:
            f.write(r.content)
    if checksum is not None:
        with io.open(local_file, 'rb') as f:
            body = f.read()
            body_checksum = hashlib.md5(body).hexdigest()
            assert body_checksum == checksum, \
            "Downloaded file '{}' has incorrect checksum: '{}' instead of '{}'".format(local_file,
            body_checksum,
            checksum)

    print("'{}' is ready!".format(file)) 

if on_vocareum():
    DATA_PATH = "../resource/asnlib/publicdata/"
else:
    DATA_PATH = ""
datasets = {'groceries.csv': '0a3d21c692be5c8ce55c93e59543dcbe'}
for filename, checksum in datasets.items():
    download(filename, local_dir=DATA_PATH, checksum=checksum)
with open('{}{}'.format(DATA_PATH, 'groceries.csv')) as fp:
    groceries_file = fp.read()"""

with open('Notebook 2/groceries.csv') as fp:
    groceries_file = fp.read()

################
# Exercise 11
'''
Your final task in this notebook is to mine this dataset for pairwise association rules. In particular, your
code should produce (no pun intended!) a final dictionary, basket_rules, that meet these conditions (read carefully!):
1. The keys are pairs , where and are item names (as strings).
2. The values are the corresponding confidence scores, .
3. Only include rules where item occurs at least MIN_COUNT times and is at least THRESHOLD.
Pay particular attention to Condition 3: not only do you have to filter by a confidence threshold, but you must exclude rules where the item does
not appear "often enough." There is a code cell below that defines values of MIN_COUNT and THRESHOLD, but your code should work even if we decide to
change those values later on.
Aside: Why would an analyst want to enforce Condition 3?
Your solution can use the groceries_file string variable defined above as its starting point. And since it's in the same notebook, you may, of course, reuse
any of the code you've written above as needed. Lastly, if you feel you need additional code cells, you can create them after the code cell marked for your
solution but before the code marked, ### TEST CODE ###.
'''
################

# Confidence threshold
THRESHOLD = 0.5
MIN_COUNT = 10 # MIN_COUNT = 6 results in 17 entries in basket_rules, MIN_COUNT = 5 results in 20 entries in basket_rules
# Only consider rules for items appearing at least `MIN_COUNT` times.

baskets = groceries_file.split("\n") # create list of baskets with items as a string
for index, basket in enumerate(baskets): # create list of baskets with items as a sublist
    baskets[index] = basket.split(",")

# Create item list
basket_item_list = []
for index, basket in enumerate(baskets):
    basket_item_list.append(set())
    for item in basket:
        basket_item_list[index].add(item)

# Create item pairs
basket_item_pairs = defaultdict(int)
for basket in baskets:
    for item1 in basket:
        for item2 in basket:
            if item1 is not item2:
                basket_item_pairs[(item1, item2)] += 1

# Create item counts
basket_item_counts = defaultdict(int)
for basket in basket_item_list:
    for item in basket:
        basket_item_counts[item] +=1

# Create pairwise association rules
basket_rules = {}
for pair in basket_item_pairs:
    conf = basket_item_pairs[pair] / basket_item_counts[pair[0]]
    if conf >= THRESHOLD and basket_item_counts[pair[0]] >= MIN_COUNT:
        basket_rules[pair] = conf

### `basket_rules_test`: TEST CODE ###
print("Found {} rules whose confidence exceeds {}.".format(len(basket_rules), THRESHOLD))
print("Here they are:\n")
print_rules(basket_rules)
assert len(basket_rules) == 19, "basket_rules length is {}".format(len(basket_rules))
assert all([THRESHOLD <= v < 1.0 for v in basket_rules.values()])
ans_keys = [("pudding powder", "whole milk"), ("tidbits", "rolls/buns"), ("cocoa drinks", "whole milk"), ("cream", "sausage")]
for k in ans_keys:
    assert k in basket_rules