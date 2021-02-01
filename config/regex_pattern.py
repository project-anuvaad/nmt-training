'''
Various regex patterns used to support translation
'''

patterns = {
    "p1" : { "regex":r'(\d+,)\s(\d+)', "description":"remove space between number separated by ," },
    "p2" : { "regex":r'(\d+.)\s(\d+)', "description":"remove space between number separated by ." },
    "p3" : { "regex":r'\d+', "description":"indentify numbers in a string" },
    "p10": { "regex":r'^(\(|\[|\{)(\d+|\d+.|\d+.\d+)(\)|\]|\})$', "description":\
        "regex for handling different types of number prefix ie in first token only,brackets variations"},
    "p11": { "regex":r'^(\d+|\d+.|\d+.\d+)$', "description":\
        "regex for handling different types of number prefix ie in first token only, no brackets variations"},
    "p12": { "regex":r'\d+,\d+,\d+,\d+,\d+|\d+,\d+,\d+,\d+|\d+,\d+,\d+|\d+,\d+|\d+', "description":\
        "indentify all numbers in a string including thousand separated numbers" },
    "p13": { "regex":r'http[s]?\s*:\s*/\s*/\s*(?:\s*[a-zA-Z]|[0-9]\s*|[$-_@.&+]|\s*[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]\s*))+',"description":\
        "identify url" },
    "p14": { "regex":r'[a-zA-Z0-9०-९_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9]+',"description":\
        "identify email id" }
}




hindi_numbers = ['०', '१', '२', '३','४','५','६','७','८','९','१०','११','१२','१३','१४','१५','१६','१७','१८','१९','२०','२१','२२','२३','२४','२५',\
                 '२६','२७','२८','२९','३०','३१','३२','३३','३४','३५','३६','३७','३८','३९','४०','४१','४२','४३','४४','४५','४६','४७','४८','४९','५०']