'''
    NAME:        Justin Smith
                 Alessandra Gudoy
    
    HOMEWORK:    Assignment 2

    CLASS:       ICS 311

    INSTRUCTOR:  Brook Conner

    DATE:        September 21, 2024

    FILE:        sayings-database.py

    DESCRIPTION: This file will correctly read the sayings.txt file and use that data to create Saying objects and store them in a red-black tree.
                 Also implements Assignment 2 required methods and has test cases.
'''

'''
    Class name:  RBNode

    DESCRIPTION: Will create a red-black tree node along with containing methods on getting the grandparent, sibling, and uncle of a node

    Parameters:  saying : Saying object
                 color  : string ('red' | 'black')

    Credit:      The Red-Black Node logic is adapted from:
                 https://www.geeksforgeeks.org/red-black-tree-in-python/
'''

class RBNode:
    def __init__(self, saying, color="red"):
        self.saying = saying # saying is a Saying object
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent
    
    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.left:
            return self.parent.right
        return self.parent.left
    
    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()

'''
    Class name:  RBTree

    DESCRIPTION: This is the red-black tree data structure. Will correctly search, insert, rotate, find minimum, find maximum and travere in-order.

    Parameters:  None

    Credit:      The Red-Black Tree implementation logic is adapted from:
                 https://www.geeksforgeeks.org/red-black-tree-in-python/
'''

class RBTree:
    def __init__(self):
        self.root = None
    
    def search(self, saying):
        current = self.root
        while current is not None:
            if saying.hawaiian == current.saying.hawaiian:
                return current
            elif saying.hawaiian < current.saying.hawaiian:
                current = current.left
            else:
                current = current.right
        return None
    
    def insert(self, saying):
        new_node = RBNode(saying)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if saying.hawaiian < current.saying.hawaiian:
                    if current.left is None:
                        current.left = new_node
                        new_node.parent = current
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        new_node.parent = current
                        break
                    else:
                        current = current.right
        self.insert_fix(new_node)

    def insert_fix(self, new_node):
        while new_node.parent and new_node.parent.color == 'red':
            if new_node.parent == new_node.grandparent().left:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color == 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.rotate_left(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_right(new_node.grandparent())
            else:
                uncle = new_node.uncle()
                if uncle and uncle.color == 'red':
                    new_node.parent.color = 'black'
                    uncle.color = 'black'
                    new_node.grandparent().color = 'red'
                    new_node = new_node.grandparent()
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.rotate_right(new_node)
                    new_node.parent.color = 'black'
                    new_node.grandparent().color = 'red'
                    self.rotate_left(new_node.grandparent())
        self.root.color = 'black'

    def rotate_left(self, node):
        right_child = node.right
        node.right = right_child.left

        if right_child.left is not None:
            right_child.left.parent = node
        
        right_child.parent = node.parent

        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        
        right_child.left = node
        node.parent = right_child

    def rotate_right(self, node):
        left_child = node.left
        node.left = left_child.right

        if left_child.right is not None:
            left_child.right.parent = node
        
        left_child.parent = node.parent

        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        
        left_child.right = node
        node.parent = left_child

    def minimum(self, node):
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node
    
    def maximum(self, node):
        if node is None:
            return None
        while node.right is not None:
            node = node.right
        return node
    
    def inorder_traversal(self, node):
        result = []
        if node is not None:
            result += self.inorder_traversal(node.left)
            result.append(node.saying)
            result += self.inorder_traversal(node.right)
        return result

'''
    Class name:  Saying

    DESCRIPTION: Will store information containing the hawaiian phrase, english translation, hawaiian explanation and english explanation

    Parameters:  hawaiian            : hawaiian phrase stored as a string
                 english             : english phrase stored as a string
                 hawaiianExplanation : the hawaiian explanation of phrase in hawaiian stored as a string
                 englishExplanation  : the english explanation of a phrase in english stored as a string
'''

class Saying:
    def __init__(self, hawaiian, english, hawaiianExplanation, englishExplanation):
        self.hawaiian = hawaiian
        self.english = english
        self.hawaiianExplanation = hawaiianExplanation
        self.englishExplanation = englishExplanation

'''
    Class name:  Database

    DESCRIPTION: Incorporates the Assignment 2 required methods and correctly read the saying data from a text file.
                 The database data is stored in a red-black tree.

    Parameters:  None
'''

class Database:
    def __init__(self):
        self.sayingsDatabase = RBTree()

    '''
        Method name:   member

        DESCRIPTION:   Searches for saying node in RBTree.

        Parameters:    saying: Saying object

        Return values: True  : Found
                       False : Not Found
    '''

    def member(self, saying):
        return self.sayingsDatabase.search(saying) != None
    
    '''
        Method name:   first

        DESCRIPTION:   Retrieves the "smallest" saying in the sayingsDatabase. 
                       Does this by calling minimum method on root of tree which returns the leftmost (smallest) node.
        
        Parameters:    None

        Return values: saying : Success
                       None   : Empty tree
    '''

    def first(self):
        return self.sayingsDatabase.minimum(self.sayingsDatabase.root).saying

    '''
        Method name:   last

        DESCRIPTION:   Retrieves the "largest" saying in the sayingsDatabase.
                       Does this by calling the maximum method on root of tree which returns the rightmost (largest) node.

        Parameters:    None
        
        Return values: saying : Success
                       None   : Empty tree
    '''

    def last(self):
        return self.sayingsDatabase.maximum(self.sayingsDatabase.root).saying

    '''
        Method name:   predecessor

        DESCRIPTION:   Finds node that comes immediately before a given node in in-order traversal of red-black tree.
                       Either looks for maximum node in left subtree or moves upward to find first ancestor where node is right child

        Parameters:    saying : Saying object

        Return values: saying : Success
                       None   : Empty tree
    '''

    def predecessor(self, saying):
        node = self.sayingsDatabase.search(saying)
        
        if node.left is not None:
            return self.sayingsDatabase.maximum(node.left)
        else:
            parent = node.parent
            tmp = node
        while parent is not None and tmp is parent.left:
            tmp = parent
            parent = tmp.parent
        return parent
        
    '''
        Method name:   successor

        DESCRIPTION:   Finds node that comes immediately after a given node in in-order traversal of red-black tree.
                       Either finds the minimum node in right subtree or moves upward to find first ancestor where node is left child

        Parameters:    saying : Saying object

        Return values: saying : Success
                       None   : Empty tree
    '''

    def successor(self, saying):
        node = self.sayingsDatabase.search(saying)
        
        if node.right is not None:
            return self.sayingsDatabase.minimum(node.right)
        else:
            parent = node.parent
            tmp = node
            while parent is not None and tmp is parent.right:
                tmp = parent
                parent = tmp.parent
            return parent

    '''
        Method name:   insert

        DESCRIPTION:   Adds saying to the sayingDatabase which is a red-black tree. 
                       Calls RBTree insert method to insert node in correct position.

        Parameters:    saying : Saying object

        Return values: void
    '''

    def insert(self, saying):
        self.sayingsDatabase.insert(saying)

    '''
        Method name:   meHua

        DESCRIPTION:   Goes through red-black tree using in-order traversal and stores all Saying objects into allSayings array
                       Iterates through allSayings array to find Saying objects where word is in hawaiian phrase
        
        Parameters:    word : string

        Return values: [Saying object(s)] : Results found
                       []                 : No results

    '''

    def meHua(self, word):
        allSayings = self.sayingsDatabase.inorder_traversal(self.sayingsDatabase.root) # array
        sayingsWithWord = []
        for saying in allSayings:
            if word in saying.hawaiian.lower():
                sayingsWithWord.append(saying)
        return sayingsWithWord
    
    '''
        Method name:   withWord

        DESCRIPTION:   Goes through red-black tree using in-order traversal and stores all Saying objects into allSayings array
                       Iterates through allSayings array to find Saying objects where word is in english phrase

        Parameters:    word : string

        Return values: [Saying object(s)] : Results found
                       []                 : No results
    '''

    def withWord(self, word):
        allSayings = self.sayingsDatabase.inorder_traversal(self.sayingsDatabase.root) # array
        sayingsWithWord = []
        for saying in allSayings:
            if word in saying.english.lower():
                sayingsWithWord.append(saying)
        return sayingsWithWord
    
    '''
        Method name:   loadFromFile

        DESCRIPTION:   Reads sayings.txt file which contain the data for the Saying objects.
                       Accounts for non-ASCII characters by encoding full unicode characters
                       After creating a Saying object, it calls the insert method to add to the red-black tree

        Parameters:    filePath : string

        Return values: void
    '''
    
    def loadFromFile(self, filePath):
        individualSayingData = []
        file = open(filePath, 'r', encoding='utf-8')

        # Looping through each line of file and removing newline characters
        for line in file:
            line = line.rstrip("\n")

            # If line is not empty, append to the individualSayingData.
            # If the length of individualSayingData is 4, that means all data is there to create saying
            if len(line) != 0:
                individualSayingData.append(line)
            if len(individualSayingData) == 4:
                hawaiian = individualSayingData[0].replace("Hawaiian: ", "")
                english = individualSayingData[1].replace("English: ", "")
                hawaiianExplanation = individualSayingData[2].replace("Explanation (Hawaiian): ", "")
                englishExplanation = individualSayingData[3].replace("Explanation (English): ", "")

                saying = Saying(hawaiian, english, hawaiianExplanation, englishExplanation)

                self.insert(saying)

                individualSayingData = []

# Example of usage
database = Database()
database.loadFromFile('sayings.txt')
allSayings = database.sayingsDatabase.inorder_traversal(database.sayingsDatabase.root)
testSaying1 = Saying('I ka ʻōlelo no ke ola, i ka ʻōlelo no ka make', 'In language there is life, in language there is death', 'He mana ko ka ʻōlelo, hiki ke hoʻopōmaikaʻi a i ʻole hoʻi hiki ke hoʻopilikia.', 'Language has power; it can either bless or bring harm.')
testSaying2 = Saying('Ua ola loko i ke aloha', 'Love gives life within', "Ka nohona o ke aloha, he ola ia no ke kino a me ka na'au.", 'A life lived with love brings wellness to body and soul.')

# Test cases
print('first() method test:    ',database.first().hawaiian, '\n')    # A'ohe hana nui ke alu 'ia
print('last() method test:     ',database.last().hawaiian, '\n')     # Ua ola loko i ke aloha
print('insert() method test:   ',len(allSayings), '\n')              # 10
print('member() method test:   ',database.member(testSaying1))       # False
print('                        ',database.member(testSaying2), '\n') # True
print('meHua() method test:    ',database.meHua('ka'))               # Array of 8 object addresses
print('                        ',database.meHua('FAIL'), '\n')       # Empty array
print('withWord() method test: ',database.withWord('past'))          # Array of 1 object address
print('                        ',database.withWord('FAIL'), '\n')    # False

print('successor() and predessor() test using hawaiian phrases: ')
for saying in allSayings:
    predecessor = database.predecessor(saying)
    successor = database.successor(saying)
    print('     Saying:   ', saying.hawaiian)
    if predecessor is not None:
        print("     Predessor:", predecessor.saying.hawaiian)
    if successor is not None:
        print("     Successor:", successor.saying.hawaiian, '\n')
