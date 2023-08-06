#!/usr/bin/env python
# coding: utf-8

# # Split alphanumeric
#
# This module takes a string of letters and numbers and return a list of paired values that can by mapped to a dictionary.

# In[1]:


import re

from money2float import money


# In[3]:


def append_count(terms):
    seen_dict = {}
    return_list = []
    for term in terms:
        if seen_dict.get(term, 0) > 0:
            seen_dict[term] += 1
            term = f"{term}{seen_dict[term]}"
        else:
            seen_dict[term] = 1
        return_list.append(term)
    return return_list


# In[5]:


def build_fee_group_list(fee_group, substitute_characters=[]):
    extended_characters = [(" ", ""), (",", ""), ("$", ""), ("CR", "-")]
    substitute_characters.extend(extended_characters)
    for item in substitute_characters:
        fee_group = fee_group.replace(*item)
    letters_regex = re.compile("[A-Z]")
    numbers_regex = re.compile("[0-9\.\-]+")
    letters = letters_regex.findall(fee_group)
    numbers = numbers_regex.findall(fee_group)
    letters = append_count(letters)
    return list(zip(letters, numbers))


# In[7]:


def map_fee_group_to_fields(fee_group_list, fee_mapping):
    fees_dict = {}
    for item in fee_group_list:
        print(item)
        mapped_name = fee_mapping.get(item[0], None)
        print(mapped_name)
        if mapped_name:
            fees_dict[mapped_name] = item[1]  # + fees_dict[mapped_name]
    return fees_dict


# In[ ]:
