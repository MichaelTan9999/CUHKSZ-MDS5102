class Node:

    def __init__(self, val) -> None:
        self.val = val
        self.left = None
        self.right = None

    def printValue(self):
        if self.val != None:
            print('The value of the node is {}.'.format(self.val))
        else:
            print('The node is empty.')
    
    # It is easier to implement getSubTree in Node Class since every node can be regarded as the root of a tree.
    def getSubTree(self, orderList):
        if self.left != None:
            self.left.getSubTree(orderList)
        orderList.append(self.val)
        if self.right != None:
            self.right.getSubTree(orderList)

class Tree:

    def __init__(self) -> None:
        self.root = None
    
    def getRoot(self):
        return self.root
    
    def insert(self, val):

        if self.root == None:
            self.root = Node(val)
            return

        current = self.root

        while current != None:
            if val <= current.val:
                if current.left != None:
                    current = current.left
                else:
                    current.left = Node(val)
                    break
            else:
                if current.right != None:
                    current = current.right
                else:
                    current.right = Node(val)
                    break

    def search(self, val):
        current = self.root

        while current != None:
            if current.val == val:
                print('Find the matched value in the tree.', end=' ')
                return current.printValue()
            elif val < current.val:
                current = current.left
            else:
                current = current.right
        
        print('None')

    # Since Python will manage trash itself, here i just delete the root node. And the referrence count of other nodes will be zero,
    # so the space of other nodes will be released.
    def delete(self):
        self.root = None

    def printTree(self):
        if self.root == None:
            print('Nothing in the tree.')
        else:
            ascending = []
            self.root.getSubTree(ascending)
            print('Values of nodes in the tree: ')
            for i in ascending:
                print(i, end=' ')
            print()

a = Tree()
for i in [8, 10, 1, 2, 3, 4, 5, 6, 7]:
    a.insert(i)

print(a.getRoot().val)
for i in [2, 3, 4, 5, 6, 7, 100, 0]:
    a.search(i)
a.printTree()
a.delete()
a.printTree()