# Week 0 Part 1.py

##################################################
import sys
print(sys.version)
#3.6.4 (v3.6.4:d48eceb, Dec 19 2017, 06:04:45) [MSC v.1900 32 bit (Intel)]
##################################################



#########################
## Download:
#!curl -O https://cse6040.gayech.edu/datasets/message_in_a_bottle.txt.zip

## Confirm (from shell):
#!echo && echo "=== Files in the current directory (from a shell command) ==="

# Confirm (from Python):
import os
print("\n=== Files in the current directory (from Python) ===\n{}".format(os.listdir('.')))
##################################################


##################################################
# Exercise 0
uncompressed_name = 'message_in_a_bottle.txt'
compressed_extension = '.zip'

filename = uncompressed_name + compressed_extension
##################################################



##################################################
# Test cell: `filename_test`

print("`filename`: '{}'".format(filename))
from zipfile import ZipFile
with ZipFile(filename, 'r') as input_zip:
    with input_zip.open(filename[:-4], 'r') as input_file:
        message = input_file.readline().decode('utf-8')
print("\n=== BEGIN MESSAGE ===\n{}=== END MESSAGE ===".format(message))
##################################################

# output
#=== Files in the current directory (from Python) ===
#['Homework1', 'Homework1.zip', 'message_in_a_bottle.txt.zip', 'part0.py', 'Week 0 part 1.pdf', 'Week 0 Part 1.py']
#`filename`: 'message_in_a_bottle.txt.zip'
#
#=== BEGIN MESSAGE ===
#some message
#=== END MESSAGE ===
