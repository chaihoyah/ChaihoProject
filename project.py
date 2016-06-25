class rbnode(object):

    def __init__(self, key):
        self._key   = key
        self._red   = False
        self._left  = None
        self._right = None
        self._p     = None
    key    = property(fget=lambda self: self._key  , doc="The node's key")
    red    = property(fget=lambda self: self._red  , doc="The node's color")
    left   = property(fget=lambda self: self._left , doc="The node's left child")
    right  = property(fget=lambda self: self._right, doc="The node's right child")
    p      = property(fget=lambda self: self._p    , doc="The node's parent")

    def __str__(self): return str(self.key)
    def __repr__(self): return str(self.key)

class rbtree(object):

    def __init__(self):
        self._nil  = rbnode(key=None)
        self._root = self._nil

    nil  = property(fget=lambda self: self._nil,  doc="The tree's nil node")
    root = property(fget=lambda self: self._root, doc="The tree's root node")

    def search(self, key, x=None):
        """ Search for node with key """
        if None == x:
            x = self.root
        while x != self.nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def minimum(self, x=None):
        """ Return node with minimum value """
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x
        
    def maximum(self, x=None):
        """ Return node with maximum value """
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right
        return x

    def print_tree(self, x=None):
        """ Print the tree nodes as a list of lists"""
        if None == x:
            x = self.root
        tree_list = []
        self._print_tree(x,tree_list)
        for level in tree_list:
            print(level)

    def _print_tree(self, x, tree_list, level=0):
        if len(tree_list) > level+1:
            tree_list[level].append(x and (x.key,x.red) or None)
        else:
            tree_list.insert(level,[x and (x.key,x.red) or None])
        if x:
            self._print_tree(x.left,  tree_list, level=level+1)
            self._print_tree(x.right, tree_list, level=level+1)

    def insert_key(self, key):
        """ Insert a key into the tree """
        self.insert_node(rbnode(key=key))
    
    def insert_node(self, z):
        """ Insert a node into the tree """
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)
    
    def delete_key(self, key):
        """ Delete a node with a given key """
        z = self.search(key)
        self.delete_node(z)

    def delete_node(self, z):
        """ Delete a given node """
        y = z
        y.orig = y.red
        if z.left == self.nil:
            x = z.right
            self._transplant(z,z.right)
        elif z.right == self.nil:
            x = z.left
            self._transplant(z,z.left)
        else:
            y = self.minimum(x=z.right)
            y.orig = y.red
            x = y.right
            if y.p == z:
                x._p = y
            else:
                self._transplant(y,y.right)
                y._right = z.right
                y.right._p = y
            self._transplant(z,y)
            y._left = z.left
            y.left._p = y
            y._red = z.red
        if not y.orig:
            self._delete_fixup(x)

    def _insert_fixup(self,z):
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False

    def _transplant(u,v):
        if u.p == self.nil:
            self._root = v
        elif u == u.p.left:
            u.p._left = v
        else:
            u.p._right = v
        v._p = u.p

    def _delete_fixup(x):
        while x != self.root and not x.red:
            if x == x.p.left:
                w = x.p.right
                if w.red:
                    w._red = False
                    x.p._red = True
                    self._left_rotate(x.p)
                    w = x.p.right
                if not w.left.red and not w.right.red:
                    w._red = True
                    x = x.p
                else:
                    if not w.right.red:
                        w.left._red = False
                        w._red = True
                        self._right_rotate(w)
                        w = x.p.right
                    w._red = x.p.red
                    x.p._red = False
                    w.right._red = False
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.red:
                    w._red = False
                    x.p._red = True
                    self._right_rotate(x.p)
                    w = x.p.left
                if not w.right.red and not w.left.red:
                    w._red = True
                    x = x.p
                else:
                    if not w.left.red:
                        w.right._red = False
                        w._red = True
                        self._left_rotate(w)
                        w = x.p.left
                    w._red = x.p.red
                    x.p._red = False
                    w.left._red = False
                    self._right_rotate(x.p)
                    x = self.root
        x._red = False

    def _left_rotate(self,x):
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y
    
    def _right_rotate(self,y):
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x


def RBtraverse1(tree):
    root=rbnode(0)
    root=tree.root
    keyli=list()
    
    if tree == None:
        return keyli
    if(keyli==None):
        keyli[0][0]=root.key[0]
        keyli[1][0]=1
    else:
        for i in range(len(keyli)):
            if(keyli[0][i]==root.key[0]):
                keyli[1][i]=keyli[1][i]+1
    RBtraverse1(root.left)
    RBtraverse1(root.right)
    
def RBtraverse2(tree):
    if tree == None: return
    print tree.key[0],
    RBtraverse2(tree.left)
    RBtraverse2(tree.right)


def interface():
    print("0. Read data files")
    print("1. display statistics")
    print("2. Top 5 most tweeted words")
    print("3. Top 5 most tweeted users")
    print("4. Find users who tweeted a word")
    print("5. Find all people who are friends of the above users")
    print("6. Delete all mentions of a word")
    print("7. Delete all users who mentioned a word")
    print("8. Find strongly connected components")
    print("9. Find shortest path from a given user")
    print("99. Quit")
    Action=int(raw_input("Select Menu:"))
    if(Action==1):
        return 1
Action_case={
        "0": 0,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10
        }

    
def userdataSave():
    f1 = open('user.txt')
    lines = f1.readlines()
    num=0
    mainT=rbtree()
    for i in range(len(lines)):
        if(i%4==0):
            x=rbnode((lines[i]+lines[i+2]).split("\n"))
            mainT.insert_node(x)
            num=num+1
    return mainT

def friendshipTree():
    f2 = open('friend.txt')
    lines = f2.readlines()
    num=0;
    friendT=rbtree()
    T=rbtree()
    for i in range(len(lines)):
        if(i%3==0):
            x=rbnode((lines[i]+lines[i+1]).split("\n"))
            friendT.insert_node(x)
            num=num+1
    return friendT

def tweetTree():
    f3 = open('word.txt')
    lines = f3.readlines()
    num=0;
    friendT=rbtree()
    T=rbtree()
    for i in range(len(lines)):
        if(i%4==0):
            x=rbnode((lines[i]+lines[i+2]).split("\n"))
            friendT.insert_node(x)
            num=num+1
    return friendT


    
        
    
            

def main():
    mainT=userdataSave()
    friendT=friendshipTree()
    wordT=tweetTree()
    Action=interface()
    if(Action==0):
        print("Total users: ")
        print("Total friendship records: ")
        print("Total tweets: ")
    elif(Action==1):
        key0=list()
        key1=list()
        keyli=list()
        keyli=RBtraverse1(friendT)
        keyli[1].sort()
        max=len(keyli[1])-1
        min=0
        print(keyli[1][max])
        print(keyli[1][min])
        
        
main()

