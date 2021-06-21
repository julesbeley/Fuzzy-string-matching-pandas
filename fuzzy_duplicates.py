from Levenshtein import ratio
import pandas as pd


def fuzzy_match(
    df, 
    key, 
    strings, 
    threshold
):
    
    dictionary = dict(zip(df[key], df[strings]))
    unique_keys = [df[key][0]]
    duplicates = {key:[] for key in dictionary}

    for key in dictionary:
        results = []

        for unique_key in unique_keys:
            to_test = dictionary[key], dictionary[unique_key]
            results.append(ratio(*to_test))

        results = dict(zip(unique_keys, results))  
        original = [key for key, value in results.items() if value >= threshold]

        if len(original) == 0:
            unique_keys.append(key)

        else:
            true_original = original[0]
            
            if len(original) > 1:
                for other_original in original[1:]:
                    unique_keys.remove(other_original)
                    duplicates[true_original].append(other_original)
                    duplicates[true_original].extend(duplicates[other_original])
                    duplicates[other_original] = []
                    
    return unique_keys, duplicates


def drop_fuzzy_duplicates(
    df, 
    key, 
    string, 
    threshold
):

    unique_keys, duplicates = fuzzy_match(df, key, string, threshold)
    return df[df['key'].isin(unique_keys)]


def fuzzy_duplicated(
    df, 
    key, 
    string, 
    threshold
):
    
    unique_keys, duplicates = fuzzy_match(df, key, string, threshold)
    return ~df['key'].isin(unique_keys)



# create test dataset

import pandas as pd
import string
import random

text = 'In approximate string matching,  the objective is to find matches for short strings \
in many longer texts,  in situations where a small number of differences is to be expected. \
The short strings could come from a dictionary,  for instance. Here,  one of the strings is\
typically short,  while the other is arbitrarily long. This has a wide range of applications, \
for instance,  spell checkers,  correction systems for optical character recognition,  and \
software to assist natural language translation based on translation memory.The Levenshtein\
distance can also be computed between two longer strings,  but the cost to compute it,  which\
is roughly proportional to the product of the two string lengths,  makes this impractical. \
Thus,  when used to aid in fuzzy string searching in applications such as record linkage,  \
the compared strings are usually short to help improve speed of comparisons.[citation needed]\
In linguistics,  the Levenshtein distance is used as a metric to quantify the linguistic distance, \
or how different two languages are from one another.[3] It is related to mutual intelligibility, \
the higher the linguistic distance,  the lower the mutual intelligibility,  and the lower the \
linguistic distance,  the higher the mutual intelligibility.'

translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
text = set(text.translate(translator).split())

unique_strings = []

for i in range(100):
    length = random.randint(1, 3)
    unique_strings.append(' '.join(random.sample(text, length)))

all_letters = list('abcdefghijklmnopqrstuvwxyz')
new_strings = []

for string in random.choices(unique_strings, k=300):
    n_changes = random.randint(0, 3)
    new_string = list(string)
    if len(new_string) > 1:
        for change in range(n_changes):
            to_change_index = random.randint(1, len(new_string)-1)
            replace_by = random.sample(all_letters, 1)[0]
            new_string[to_change_index] = replace_by
    new_strings.append(''.join(new_string))
    
all_strings = unique_strings + new_strings
random.shuffle(all_strings)
        
test_df = pd.DataFrame(all_strings, columns=['strings'])
test_df['key'] = test_df.index

test_df = test_df[['key', 'strings']]