import math


class MyBPlusTreeNode:

    def __init__(self, m, keys=None, children=None, father=None, next_node=None):
        self.is_leaf = len(children) == 0
        # 列表判空https://www.cnblogs.com/ayistar/p/11371146.html
        self.keys = keys if keys else []
        self.children = children if children else []
        self.count = len(keys)
        self.m = m
        self.father = father
        self.next_node = next_node

    def root_divide(self):
        """
        出现某节点元素过多需要分裂时分为两种情况
        如果是根的话 保留根节点 并新建左右孩子初始化 再修改所有受影响的值
        """
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
        """如果是非根的话 新建兄弟节点并初始化 再修改所有受影响的值"""
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

    def check_count_too_big(self):
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
            # 插入该值后该节点的最大key值变大 需要做相应修改
            if i == self.count:
                i -= 1
                self.keys[i] = key
            self.children[i].add_key(key)
        self.check_count_too_big()

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

    def borrow_from_right_brother_node(self):
        if not self.next_node:
            return False
        right_brother_node = self.next_node
        if right_brother_node.father is not self.father:
            return False
        if right_brother_node.count <= math.ceil(self.m/2):
            return False
        self.keys.append(right_brother_node.keys.pop(0))
        self.children.append(right_brother_node.children.pop(0))
        self.count += 1
        right_brother_node.count -= 1
        return True

    def borrow_from_left_brother_node(self):
        father = self.father
        i = 0
        while i < self.count:
            if father.children[i] is self:
                break
            i += 1
        if i == 0:
            return False
        left_brother_node = father.children[i-1]
        if left_brother_node.count <= math.ceil(self.m/2):
            return False
        self.keys.append(left_brother_node.keys.pop())
        self.children.append(left_brother_node.children.pop())
        father.keys[i-1] = left_brother_node.keys[-1]
        self.count += 1
        left_brother_node.count -= 1
        return True

    def check_count_too_small(self):
        least_count = math.ceil(self.m/2)
        if self.count < least_count:
            # 如果是根节点
            if self.father:
                pass  # TBD
            else:
                # 先找右边兄弟节点借
                if self.borrow_from_right_brother_node():
                    pass
                # 再找左边兄弟节点借
                elif self.borrow_from_left_brother_node():
                    pass
                else:
                    pass  # TBD
        pass

    def change_key_recursively(self, changed_child, new_key):
        i = 0
        while i < self.count:
            if self.children[i] is changed_child:
                self.keys[i] = new_key
                if self.father and i == self.count-1:
                    self.father.change_key_recursively(self, new_key)
                break
            i += 1

    def delete_key(self, index):
        if index == self.count-1:
            if index == 0:
                # B+树中只有一个key
                self.keys.pop()
                self.count -= 1
            else:
                if self.keys[index] != self.keys[index-1]:
                    self.father.change_key_recursively(self, self.keys[index - 1])
        else:
            self.keys.pop(index)
        if self.father:
            # 如果不是在根节点处的叶子节点
            self.check_count_too_small()


class MyBPlusTree:

    M = 3

    def __init__(self):
        self.root = MyBPlusTreeNode(MyBPlusTree.M)

    def add_key(self, key):
        self.root.add_key(key)

    def find_key(self, key):
        return self.root.find_key(key)
