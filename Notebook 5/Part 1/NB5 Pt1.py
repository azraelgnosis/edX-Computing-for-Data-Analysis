import requests
import os
import hashlib

if os.path.exists('.voc'):
    data_url = 'https://cse6040.gatech.edu/datasets/yelp-example/yelp.htm'
else:
    data_url = 'https://github.com/cse6040/labs-fa17/raw/master/datasets/yelp.htm'

if not os.path.exists('yelp.htm'):
    print("Downloading: {} ...".format(data_url))
    r = requests.get(data_url)
    with open('yelp.htm', 'w', encoding=r.encoding) as f:
        f.write(r.text)

with open('yelp.htm', 'r', encoding='utf-8') as f:
    yelp_html = f.read().encode(encoding='utf-8')
    checksum = hashlib.md5(yelp_html).hexdigest()
    assert checksum == "4a74a0ee9cefee773e76a22a52d45a8e", "Downloaded file has incorrect checksum!"
    
print("'yelp.htm' is ready!")

with open('yelp.htm', 'r', encoding='utf-8') as yelp_file:
    yelp_html = yelp_file.read()
    
# Print first few hundred characters of this string:
print("*** type(yelp_html) == {} ***".format(type(yelp_html)))
n = 1000
print("*** Contents (first {} characters) ***\n{} ...".format(n, yelp_html[:]))

################################
# Exercise
'''
Write some Python code to create a variable named rankings, which is a list of dictionaries set up as follows:

rankings[i] is a dictionary corresponding to the restaurant whose rank is i+1. For example, from the screenshot above, rankings[0] should be a dictionary with information about Gus's World Famous Fried Chicken.
Each dictionary, rankings[i], should have these keys:
rankings[i]['name']: The name of the restaurant, a string.
rankings[i]['stars']: The star rating, as a string, e.g., '4.5', '4.0'
rankings[i]['numrevs']: The number of reviews, as an integer.
rankings[i]['price']: The price range, as dollar signs, e.g., '$', '$$', '$$$', or '$$$$'.
Of course, since the current topic is regular expressions, you might try to apply them (possibly combined with other string manipulation methods) find the particular patterns that yield the desired information.
'''
################################

import re

rankings = []

f = open("yelp.htm", 'r', encoding='utf-8')
rank = 1

# skips past first two spondered ads
line = f.readline()
while "class=\"regular-search-result\"" not in line:
    line = f.readline()

while rank < 11:
    if str(rank)+".  " in line:
        rankings.append({"name": re.match(".*<span>(.*)</span>.*", line).group(1)})
    if "star rating" in line:
        rankings[rank-1]["stars"] = re.match(".*(\d\.\d).*", line).group(1)
        f.readline()
    if "reviews" in line:
        rankings[rank-1]["numrevs"] = int(re.match("\s*(\d+)\s.*", line).group(1))
    if "$" in line:
        rankings[rank-1]["price"] = re.match(".*>(\$+)<.*", line).group(1)
        rank+=1
    line = f.readline()

################################
# Test cell: `rankings_test`

assert type(rankings) is list, "`rankings` must be a list"
assert all([type(r) is dict for r in rankings]), "All `rankings[i]` must be dictionaries"

print("=== Rankings ===")
for i, r in enumerate(rankings):
    print("{}. {} ({}): {} stars based on {} reviews".format(i+1,
                                                             r['name'],
                                                             r['price'],
                                                             r['stars'],
                                                             r['numrevs']))

assert rankings[0] == {'numrevs': 549, 'name': 'Gus’s World Famous Fried Chicken', 'stars': '4.0', 'price': '$$'}
assert rankings[1] == {'numrevs': 1777, 'name': 'South City Kitchen - Midtown', 'stars': '4.5', 'price': '$$'}
assert rankings[2] == {'numrevs': 2241, 'name': 'Mary Mac’s Tea Room', 'stars': '4.0', 'price': '$$'}
assert rankings[3] == {'numrevs': 481, 'name': 'Busy Bee Cafe', 'stars': '4.0', 'price': '$$'}
assert rankings[4] == {'numrevs': 108, 'name': 'Richards’ Southern Fried', 'stars': '4.0', 'price': '$$'}
assert rankings[5] == {'numrevs': 93, 'name': 'Greens &amp; Gravy', 'stars': '3.5', 'price': '$$'}
assert rankings[6] == {'numrevs': 350, 'name': 'Colonnade Restaurant', 'stars': '4.0', 'price': '$$'}
assert rankings[7] == {'numrevs': 248, 'name': 'South City Kitchen Buckhead', 'stars': '4.5', 'price': '$$'}
assert rankings[8] == {'numrevs': 1558, 'name': 'Poor Calvin’s', 'stars': '4.5', 'price': '$$'}
assert rankings[9] == {'numrevs': 67, 'name': 'Rock’s Chicken &amp; Fries', 'stars': '4.0', 'price': '$'}

print("\n(Passed!)")