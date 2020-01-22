
class MyBPlusTreeNode:

    def __init__(self, m, keys=[], children=[], father=None, next_node=None):
        self.is_leaf = len(children) == 0
        # 列表判空https://www.cnblogs.com/ayistar/p/11371146.html
        self.keys = keys
        self.children = children
        self.count = len(keys)
        self.m = m
        self.father = father
        self.next_node = next_node

    def root_divide(self):
        mid_point = self.m // 2
        left_child_keys = self.keys[:mid_point+1]
        right_child_keys = self.keys[mid_point+1:]
        left_child_children = self.children[:mid_point+1]
        right_child_children = self.children[mid_point+1:]
        right_child = MyBPlusTreeNode(self.m, right_child_keys, right_child_children, self)
        left_child = MyBPlusTreeNode(self.m, left_child_keys, left_child_children, self, right_child)
        for child in left_child_children:
            child.father = left_child
        for child in right_child_children:
            child.father = right_child
        self.keys = [self.keys[mid_point], self.keys[self.m]]
        self.children = [left_child, right_child]
        self.count = 2
        self.is_leaf = False

    def branch_divide(self):
        mid_point = self.m // 2
        new_self_keys = self.keys[:mid_point+1]
        new_node_keys = self.keys[mid_point+1:]
        new_self_children = self.children[:mid_point+1]
        new_node_children = self.children[mid_point+1:]
        new_node = MyBPlusTreeNode(self.m, new_node_keys, new_node_children, self.father, self.next_node)
        for child in new_node_children:
            child.father = new_node
        father = self.father
        i = 0
        while i < father.count:
            if father.children[i] is self:
                break
            i += 1
        father.keys.insert(i, self.keys[mid_point])
        father.children.insert(i+1, new_node)
        father.count += 1
        self.keys = new_self_keys
        self.children = new_self_children
        self.next_node = new_node
        self.count = len(new_self_keys)
        self.is_leaf = False

    def check_count(self):
        if self.count > self.m:
            if self.father:
                self.branch_divide()
            else:
                self.root_divide()

    def add_key(self, key):
        i = 0
        while i < self.count:
            if key < self.keys[i]:
                break
            i += 1
        if self.is_leaf:
            self.keys.insert(i, key)
            self.count += 1
        else:
            if i == self.count:
                i -= 1
                self.keys[i] = key
            self.children[i].add_key(key)
        self.check_count()

    def find_key(self, key):
        if self.count == 0:
            return None
        i = 0
        while i < self.count:
            if key <= self.keys[i]:
                break
            i += 1
        if self.is_leaf:
            if self.keys[i] == key:
                return {'leaf': self, 'index': i}
            else:
                return None
        else:
            return self.children[i].find_key(key)


class MyBPlusTree:

    M = 3

    def __init__(self):
        self.root = MyBPlusTreeNode(MyBPlusTree.M)

    def add_key(self, key):
        self.root.add_key(key)

    def find_key(self, key):
        return self.root.find_key(key)

