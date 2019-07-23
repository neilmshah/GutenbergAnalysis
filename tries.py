class Trie:
    def __init__(self):
        self._end = '*'
        self.trie = dict()
    
    def makeTrie(self,words):
        trie=dict()
        for word in words:
            temp_dict=trie
            for letter in word:
                temp_dict=temp_dict.setdefault(letter,{})
            temp_dict[self._end]=self._end
        self.trie=trie
        return trie
    
    def findWord(self,word):
        trie=self.trie
        for w in word:
            if(w in trie): trie=trie[w]
            else: return False
        #if you only want to chk substr existance, return true here.
        if(self._end in trie): return True

        return False

    def addWord(self,word):
        if(self.findWord(word)): return self.trie
        subTrie=self.trie
        for w in word:
            if(w in subTrie): subTrie=subTrie[w]
            else: subTrie=subTrie.setdefault(w,{})
        subTrie[self._end]=self._end
        return self.trie 
    
    def printTrie(self):
        print(self.trie)