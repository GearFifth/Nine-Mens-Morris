# Tree data structure
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def is_root(self):
        return self.parent == None

    def is_leaf(self):
        return len(self.children) == 0

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(self):
        spaces = ' ' * self.get_level() * 3 + "-"
        print(spaces + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()
        
class Tree:
    def __init__(self,root):
        self.root = root

# root = TreeNode("Electronics")

# laptop = TreeNode("Laptop")
# tablet = TreeNode("tablet")
# phone = TreeNode("phone")

# root.add_child(laptop)
# root.add_child(tablet)
# root.add_child(phone)

# keyboard = TreeNode("keyboard")
# screen = TreeNode("screen")

# laptop.add_child(keyboard)
# laptop.add_child(screen)

# root.print_tree()