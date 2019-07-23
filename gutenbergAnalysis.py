from collections import defaultdict
import heapq
import sys
import re
import tries

class Gutenberg:
    def __init__(self, filename, countNums):
        self.filename = filename
        self.countNums = countNums
    
    def getWords(self):
        '''
        Parses file to extract words. Returns list of words.
        Words are sanitized to remove space, special characters,
        punctuations, convert to lowercase, etc. 
        Parsing numbers as words is optional.
        '''
        allWords=[]
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    words = line.split()
                    for word in words: 
                        word = word.lower()
                        if(self.countNums):
                            word = re.sub('[^A-Za-z0-9]+', '', word)
                            if(word != ''): allWords.append(word)
                        else:
                            word = re.sub('[^A-Za-z]+', '', word)
                            if(word != ''): allWords.append(word)
            return allWords
        except:
            print('An error occured trying to read the file.')
            print(sys.exc_info()[0])
            exit()
    
    def getWordsByChapter(self):
        '''
        Parses file to extract words by chapter. 
        Returns dictionary of hashmap of (word,count) per chapter so lookup is constant time.
        eg: {1: {'word1':10, 'word2':5}, 2: {'word1':5}}
        Words are sanitized to remove space, special characters,
        punctuations, convert to lowercase, etc. 
        Parsing numbers as words is optional.
        '''
        wordsByChapter={}
        chapter = 0
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    words = line.split()
                    if("Chapter" in words and len(words)==2):
                        chapter+=1
                    if(chapter>0):
                        if(len(wordsByChapter)<chapter):
                            wordsByChapter[chapter] = defaultdict(int)
                        for word in words: 
                            word = word.lower()
                            if(self.countNums):
                                word = re.sub('[^A-Za-z0-9]+', '', word)
                                if(word != ''): wordsByChapter[chapter][word]+=1
                            else:
                                word = re.sub('[^A-Za-z]+', '', word)
                                if(word != ''): wordsByChapter[chapter][word]+=1
            return wordsByChapter
        except:
            print('An error occured trying to read the file.')
            print(sys.exc_info()[0])
            exit()
    
    def getQuotesByChapter(self):
        '''
        Parses file to extract quotes by chapter. 
        Returns dictionary of hashmap of {chapter: {quote:1}} so lookup is constant time.
        '''
        quotesByChapter={}
        chapter,quote = 0 , ""
        quoteOpen = False
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    words = line.split()
                    if("Chapter" in words and len(words)==2):
                        chapter+=1
                        quoteOpen, quote = False, ""
                    if(chapter>0):
                        if(len(quotesByChapter)<chapter):
                            quotesByChapter[chapter] = defaultdict(int)
                        for word in words: 
                            if('\"' in word): 
                                if(word[0]=='\"' and word[-1]=='\"'):
                                    quotesByChapter[chapter][word[1:-1]]=1
                                    continue
                                quoteOpen = not quoteOpen
                                if(quoteOpen==False): quote+=word[:-1]
                                if(word[0]=='\"'): word=word[1:]
                            if(quoteOpen):
                                quote+= word + " "
                            elif(not quoteOpen and len(quote)>0):
                                quotesByChapter[chapter][quote]=1
                                quote=""
            return quotesByChapter
        except:
            print('An error occured trying to read the file.')
            print(sys.exc_info()[0])
            exit()
    
    def getTotalNumberOfWords(self):
        return len(self.getWords())
    
    def getTotalUniqueWords(self):
        uniqueWords = set()
        words = self.getWords()
        for word in words: uniqueWords.add(word)
        return len(uniqueWords)

    def get20MostFrequentWords(self):
        wordMap = defaultdict(int)
        words = self.getWords()
        for word in words: wordMap[word]+=1
        
        wordHeap = []
        for word in wordMap: 
            wordHeap.append((-wordMap[word], word))
        heapq.heapify(wordHeap)

        freqWords = []
        for i in range(20):
            num, word = heapq.heappop(wordHeap)
            freqWords.append([word, -num])
        
        return freqWords
    
    def get20MostInterestingFrequentWords(self):
        allWords = self.getWords()
        commonWords={}
        with open('1000commonEnglishWords.txt', 'r') as file:
            for line in file:
                words = line.split()
                for word in words: commonWords[word]=1
        
        wordMap = defaultdict(int)
        for word in allWords:
            if(word not in commonWords):
                wordMap[word]+=1
        
        wordHeap=[]
        for word in wordMap: wordHeap.append((-wordMap[word], word))
        heapq.heapify(wordHeap)
        
        freqWords = []
        for i in range(20):
            nums, word = heapq.heappop(wordHeap)
            freqWords.append([word, -nums])
        
        return freqWords

    def get20LeastFrequentWords(self):
        wordMap = defaultdict(int)
        words = self.getWords()
        for word in words: wordMap[word]+=1
        
        wordHeap = []
        for word in wordMap: 
            wordHeap.append((wordMap[word], word))
        heapq.heapify(wordHeap)

        LeastfreqWords = []
        for i in range(20):
            num, word = heapq.heappop(wordHeap)
            LeastfreqWords.append([word, num])
        
        return LeastfreqWords
    
    def getFrequencyOfWord(self, word):
        wordsByChapter = self.getWordsByChapter()
        wordFrequency=[]
        for chapter in wordsByChapter:
            if(word in wordsByChapter[chapter]):
                wordFrequency.append(wordsByChapter[chapter][word])
            else: wordFrequency.append(0)
        return wordFrequency

    def getChapterQuoteAppears(self, quote):
        chapterQuotes = self.getQuotesByChapter()
        for chapter in chapterQuotes:
            # if(chapter==6): 
            #     for quotes in chapterQuotes[chapter]:
            #         print(quotes)
            if(quote in chapterQuotes[chapter]):
                return chapter
        
        return -1

    def generateSentence(self, startsWith):
        #setting count nums to true since we want to consider numbers 
        #to generate the sentence as they may be signiticant
        origCountNums = self.countNums
        self.countNums = True
        words = self.getWords()
        self.countNums = origCountNums
        
        #create a hashmap of word:count to select the next word with
        #highest frequency
        wordMap = defaultdict(int)
        for word in words: wordMap[word]+=1
        startsWith = startsWith.lower()
        output, outputString = [startsWith], startsWith + " "

        def getNextWord(startWord):
            nextWord=[]
            with open(self.filename, 'r') as file:
                for line in file:
                    words = line.split()
                    for i in range (len(words)): 
                        words[i] = words[i].lower()
                        if(words[i]==startWord and i<len(words)-1):
                            nextWord.append(re.sub('[^A-Za-z0-9]+', '', words[i+1]))

            return nextWord

        while(len(output)<20):
            nextWords = getNextWord(output[-1])
            wordToAdd, freq = "", 0
            for nextWord in nextWords:
                if(wordMap[nextWord]>freq and nextWord not in output):
                    freq = wordMap[nextWord]
                    wordToAdd = nextWord
            output.append(wordToAdd)
            outputString += wordToAdd + " "
        
        return outputString

    def getAutoCompleteSentence(startOfSentence):
        t = tries.Trie()
    
    def findClosestMatchingQuote(self, quote):
        chapterQuotes = self.getQuotesByChapter()
        matchingWords, result = 0, ""
        quoteArr = quote.split()
        for chapter in chapterQuotes:
            for q2 in chapterQuotes[chapter]:
                tempCount=0
                for q in quoteArr:
                    if(q in q2): tempCount+=1
                if(tempCount>matchingWords):
                    matchingWords = tempCount
                    result = q2
        
        return result

        
        
g = Gutenberg("GreatExpectations.txt", False)
# print(g.getTotalNumberOfWords())
# print(g.getTotalUniqueWords())
# print(g.get20MostFrequentWords())
# print(g.get20MostInterestingFrequentWords())
# print(g.get20LeastFrequentWords())
#print(g.getFrequencyOfWord("estella"))
#print(g.getChapterQuoteAppears("You acted noble, my boy"))
#print(g.generateSentence("it"))
print(g.findClosestMatchingQuote("noble boy"))