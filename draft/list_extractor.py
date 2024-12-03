"""
Модуль для извлечения массива из текста.
"""
import ast
import re

def extract_list(s):
    match = re.search(r"\[.*?\]", s)
    if match:
        list_str = match.group(0)
        try:
            result_list = ast.literal_eval(list_str)
            if isinstance(result_list, list):
                return result_list
        except Exception as e:
            return e
    return s

# Examples
s1 = "dkjvnjkd ['coder'] djvnsfn"
s2 = "random text with [1, 2, 3, 4] in it"
s3 = "no list here"

print(extract_list(s1))  # Output: ['coder']
print(extract_list(s2))  # Output: [1, 2, 3, 4]
print(extract_list(s3))  # Output: None
