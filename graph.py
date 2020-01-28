from bplus import MyBPlusTree, MyBPlusTreeNode
from graphviz import Digraph, nohtml


class CountNode:
    amount = 0


def add_to_graph_recursively(g, node:MyBPlusTreeNode, father_count, node_index):
    CountNode.amount += 1
    current_count = CountNode.amount
    nohtml_str = ""
    i = 0
    if node.is_leaf:
        for i in range(node.count):
            nohtml_str = nohtml_str+"<%d>%d|"%(i,node.keys[i])
        nohtml_str = nohtml_str[:-1]
        g.node(str(current_count),nohtml(nohtml_str))
        if father_count >= 0:
            g.edge("%d:%d" % (father_count, node_index),
                   "%d:%d" % (current_count, node.count//2))
    else:
        for i in range(node.count):
            nohtml_str = nohtml_str + "<%d>|" % (2 * i)
            add_to_graph_recursively(g, node.children[i], current_count, 2 * i)
            if i<node.count-1:
                nohtml_str = nohtml_str + "<%d>%d|" % (2 * i + 1, node.keys[i])
        nohtml_str = nohtml_str[:-1]
        g.node(str(current_count), nohtml(nohtml_str))
        if father_count >= 0:
            g.edge("%d:%d" % (father_count, node_index),
                   "%d:%d" % (current_count, node.count-1))


def show_graph(b_plus_tree: MyBPlusTree):
    g = Digraph('g', filename='btree.gv',
                node_attr={'shape': 'record', 'height': '.1'})
    CountNode.amount = 0
    add_to_graph_recursively(g, b_plus_tree.root, -1, -1)
    g.view()









