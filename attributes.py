<attribute>
<name>
random words (standard)
</name>
<function>
def toniR_randomWords(phrase):
    import pattern.en
    import random
    words = phrase.split()
    nouns = [pattern.en.lemma(x) for x in words if x in pattern.en.wordnet.NOUNS]
    verbs = [pattern.en.lemma(x) for x in words if x in pattern.en.wordnet.VERBS]
    adverbs = [pattern.en.lemma(x) for x in words if x in pattern.en.wordnet.ADVERBS]
    adjectives = [pattern.en.lemma(x) for x in words if x in pattern.en.wordnet.ADJECTIVES]
    allWords = list(set(nouns+verbs+adverbs+adjectives))
    return len(allWords)/float(len(words))
    </function>
</attribute>
<attribute>
<name>
basic words (standard)
</name>
<function>
def toniR_basicWords(phrase):
    import pattern.en
    import random
    words = phrase.split()
    basicWords = [pattern.en.lemma(x) for x in words if x in pattern.en.wordlist.BASIC]
    return len(basicWords)/float(len(words))
    </function>
</attribute>
<attribute>
<name>
academic words (standard)
</name>
<function>
def toniR_academicWords(phrase):
    import pattern.en
    import random
    words = phrase.split()
    academicWords = [pattern.en.lemma(x) for x in words if x in pattern.en.wordlist.ACADEMIC]
    return len(academicWords)/float(len(words))
    </function>
</attribute>
