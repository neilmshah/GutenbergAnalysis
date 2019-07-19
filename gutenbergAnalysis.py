from collections import defaultdict
import heapq

class Gutenberg:
    def __init__(self, filename):
        self.filename = filename
    
    def getTotalNumberOfWords(self, filename):
        wordCount=0
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
                wordCount+= len(words)
        return wordCount
    
    def getTotalUniqueWords(self, filename):
        uniqueWords = set()
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
                for word in words: uniqueWords.add(word)
        return len(uniqueWords)

    def get20MostFrequentWords(self, filename):
        wordMap = defaultdict(int)
        with open(filename, 'r') as file:
            for line in file:
                words = line.split()
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
        
g = Gutenberg("SherlockHolmes.txt")
print(g.get20MostFrequentWords("SherlockHolmes.txt"))
