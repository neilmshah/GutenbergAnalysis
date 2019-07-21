from collections import defaultdict
import heapq
import sys
import re

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
        Returns dictionary of hashmap of (word,count) per chapter.
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
                
    
        
g = Gutenberg("GreatExpectations.txt", False)
# print(g.getTotalNumberOfWords())
# print(g.getTotalUniqueWords())
#print(g.get20MostFrequentWords())
#print(g.get20MostInterestingFrequentWords())
# print(g.get20LeastFrequentWords())
#print(g.getFrequencyOfWord("pip"))