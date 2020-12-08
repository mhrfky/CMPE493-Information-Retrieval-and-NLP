class node:
    def __init__(self):
        self.children = {}    #holds the children nodes
        self.isWord = False   #is a check for if it is the end of a word
    def get_children(self):
        return self.children
    
    