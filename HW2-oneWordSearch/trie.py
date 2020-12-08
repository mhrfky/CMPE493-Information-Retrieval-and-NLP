from node import node
class trie:
    def __init__(self):
        self.root = node() #create a node for to be root of traditional trie structure
        
    def add(self,string : str): #starts the add sequence
        self.addSequence(self.root,string,0)
    def addSequence(self,curr : node,string : str,length : int): #traditional algorithm for adding to a trie
        if len(string) == length: #checks if the end of the word is reached and marks it
            curr.isWord = True
            return
        nodes = curr.get_children() 
        if string[length] in curr.get_children() : #checks if the character to be added at that location

            self.addSequence(nodes[string[length]],string,length+1)
        else: #if it does not exist in children adds it
            curr.get_children()[string[length]] = node()
            self.addSequence(nodes[string[length]],string,length+1)
            
    def get(self,pattern : str): # starts the get sequence
        return list(set(self.getSequence(pattern,self.root, "", 0)))
        
    def getSequence(self,pattern : str, curr : node, sofar : str,length : int):

        if curr == None: #checks the current node for errorous input
            return []
        children = curr.get_children() 
        if len(pattern) == length:  #checks if the end of the pattern has already been reached
            if curr.isWord:         #if it is a word, returns it
                return [sofar]
            return []
        
        if pattern[length] == '*': #checks the wildcards
            #it calls a case where wildcard amount to nothing
            merge = self.getSequence(pattern, curr, sofar, length+1)
            #calls a function for every child to cover all the cases and merges their results
            for char in children:
                node = children[char]
                merge += self.getSequence(pattern, node, sofar+char, length)
            return merge
        else:
            #if it is a normal character in the pattern, it tries to find the 
            #char in children, if it cannot, it returns empty list
            if pattern[length] in children:
                strlist = self.getSequence(pattern, children[pattern[length]],
                                           sofar + pattern[length], length+1)
                return strlist
            else:
                return []
