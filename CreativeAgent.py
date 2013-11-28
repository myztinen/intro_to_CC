import agent
import random
import time
from agent import Feedback
import pattern.en

class CreativeAgent(agent.Agent):


    def __init__(self, name):
        self.mood = 0.6
        agent.Agent.__init__(self, name)
        	
    def lifeCycle(self):
        r = random.random()
        if r < 0.33:
            self.generateSentence()
        if r > 0.33 and r < 0.66:
            unratedwords = self.getUnscoredWords()
            if len(unratedwords) > 0:
                self.score(unratedwords[0])
        elif r > 0.66:
            feedback = self.getAllFeedback()
            self.adapt(feedback)
        time.sleep(1)

    def score(self, word):
        if self.mood > 0.8:
            funcId = "toniR_randomWords"
            funcName = "random words"
        elif self.mood > 0.25 and self.mood < 0.75:
            funcId = "toniR_basicWords"
            funcName = "basic words"
        else:
            funcId = "toniR_academicWords"
            funcName = "academic words"
        score = self.callFunction(funcId, word.word)
        if score>0.75:
            level = "high"
        elif score<0.25:
            level = "low"
        else:
            level = "varying"
        framing = "I find the attribute "+funcName+" to be as "+level
        self.sendFeedback(word.word_id, score, framing, wordtext=word.word)

    def generateSentence(self):

        if self.mood > 0.75:
            self.generateBASICSentence()
        elif self.mood>0.25 and self.mood < 0.75:
            self.generateACADEMICSentence()
        else:
            self.generateRandomSentence()

    def adapt(self, feedback):
        for f in feedback:
            if self.mood > f.score:
                self.mood = self.mood - abs(self.mood-f.score)/10
                if f.score == 0.0:
                    self.mood = self.mood - 0.1
            else:
                self.mood = self.mood + abs(self.mood-f.score)/10

        if self.mood < 0.0:
            self.mood = 0.0
        elif self.mood > 1.0:
            self.mood = 1.0

        if self.mood > 0.75:
            	print "I feel good and generate basic sentences"
        elif self.mood>0.25 and self.mood < 0.75:
            	print "I feel OK and generate academic sentences"
        else:
            	print "I feel angry and generate random sentences!!!"
            	
    def generateRandomSentence(self):
        noun = self.getRandomNoun()
        adverb = self.getRandomAdverb()
        verb = pattern.en.conjugate(self.getRandomVerb(),tense=pattern.en.PRESENT, person=3, number=pattern.en.SINGULAR, mood=pattern.en.INDICATIVE, negated=False)
        s_object = pattern.en.pluralize(self.getRandomNoun(),classical=True)
        sentence = noun+" "+ adverb+ " "+ verb + " " + s_object
        explanation = "I find the attribute random words to be as high as I prefer"
        self.propose(sentence, explanation)

    def generateBASICSentence(self):
        noun = self.getRandomBASICWord("NOUN")
        initialVerb = self.getRandomBASICWord("VERB")
        verb = pattern.en.conjugate(initialVerb, tense=pattern.en.PRESENT, person=3, number=pattern.en.SINGULAR, mood=pattern.en.INDICATIVE, negated=False)
        secondNoun = pattern.en.pluralize(self.getRandomBASICWord("NOUN"), pos=pattern.en.NOUN, classical=True)
        sentence = noun+" "+ verb + " " + secondNoun
        explanation = "I find the attribute basic words to be as high as I prefer"
        self.propose(sentence, explanation)

    def generateACADEMICSentence(self):
        noun = self.getRandomACADEMICWord("NOUN")
        initialVerb = self.getRandomACADEMICWord("VERB")
        verb = pattern.en.conjugate(initialVerb, tense=pattern.en.PRESENT, person=3, number=pattern.en.SINGULAR, mood=pattern.en.INDICATIVE, negated=False)
        secondNoun = pattern.en.pluralize(self.getRandomACADEMICWord("NOUN"), pos=pattern.en.NOUN, classical=True)
        sentence = noun+" "+ verb + " " + secondNoun
        explanation = "I find the attribute academic words to be as high as I prefer"
        self.propose(sentence, explanation)

    def getRandomNoun(self):
        randomNumber = random.randint(0, len(pattern.en.wordnet.NOUNS)-1)
        return pattern.en.wordnet.NOUNS[randomNumber].form

    def getRandomVerb(self):
        randomNumber = random.randint(0, len(pattern.en.wordnet.VERBS)-1)
        return pattern.en.wordnet.VERBS[randomNumber].form

    def getRandomAdverb(self):
        randomNumber = random.randint(0, len(pattern.en.wordnet.ADVERBS)-1)
        return pattern.en.wordnet.ADVERBS[randomNumber].form

    def getRandomBASICWord(self, wordType):
        randomWord = self.getRandomWordFromBASICWordList()
        if wordType=="VERB":
            while len(pattern.en.wordnet.synsets(randomWord, pos=pattern.en.VERB))==0:
                randomWord = self.getRandomWordFromBASICWordList()
        elif wordType=="NOUN":
            while len(pattern.en.wordnet.synsets(randomWord, pos=pattern.en.NOUN))==0:
                randomWord = self.getRandomWordFromBASICWordList()
        return randomWord

    def getRandomACADEMICWord(self, wordType):
        randomWord = self.getRandomWordFromACADEMICWordList()
        if wordType=="VERB":
            while len(pattern.en.wordnet.synsets(randomWord, pos=pattern.en.VERB))==0:
                randomWord = self.getRandomWordFromACADEMICWordList()
        elif wordType=="NOUN":
            while len(pattern.en.wordnet.synsets(randomWord, pos=pattern.en.NOUN))==0:
                randomWord = self.getRandomWordFromACADEMICWordList()
        return randomWord

    def getRandomWordFromBASICWordList(self):
        randomNumber = random.randint(0, len(pattern.en.wordlist.BASIC)-1)
        return pattern.en.wordlist.BASIC[randomNumber]

    def getRandomWordFromACADEMICWordList(self):
        randomNumber = random.randint(0, len(pattern.en.wordlist.ACADEMIC)-1)
        return pattern.en.wordlist.ACADEMIC[randomNumber]