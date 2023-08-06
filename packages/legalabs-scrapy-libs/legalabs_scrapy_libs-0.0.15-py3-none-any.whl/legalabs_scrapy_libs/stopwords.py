stopwords_set = set('''
da das do dos de
na nas no nos
para pra pro em
pelo pela à às
a o e é ao aos até
que se
um uma
'''.split())

def is_stopword(word):
    if type(word) != str:
        raise Exception('Input must be str')

    return word.strip().lower() in stopwords_set
