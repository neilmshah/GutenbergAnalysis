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
        pass

g = Gutenberg("SherlockHolmes.txt")
print(g.getTotalUniqueWords("SherlockHolmes.txt"))
