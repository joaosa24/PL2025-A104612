class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
    
    def eval(self):
        if self.type == 'num':
            return int(self.value)
        elif self.type == 'plus':
            return self.left.eval() + self.right.eval()
        elif self.type == 'minus':
            return self.left.eval() - self.right.eval()
        elif self.type == 'times':
            return self.left.eval() * self.right.eval()
        elif self.type == 'div':
            return self.left.eval() // self.right.eval()
