from bplus import MyBPlusTree


def test1():
    tree = MyBPlusTree()
    tree.add_key(1)
    tree.add_key(6)
    tree.add_key(3)
    tree.add_key(4)

    tree.add_key(9)
    tree.add_key(7)


    tree.add_key(11)
    tree.add_key(12)
    tree.add_key(13)
    tree.add_key(14)
    print(tree.find_key(13))

    tree.add_key(15)
    tree.add_key(17)
    tree.add_key(19)
    tree.add_key(21)
    tree.add_key(23)
    tree.add_key(25)
    print(tree.find_key(23))


def test2():
    tree = MyBPlusTree()
    tree.add_key(1)
    tree.add_key(1)
    tree.add_key(1)
    tree.add_key(1)

    tree.add_key(1)
    tree.add_key(1)
    tree.add_key(1)
    tree.add_key(1)

    tree.add_key(1)
    tree.add_key(1)
    tree.add_key(1)
    tree.add_key(1)

    print(1)

test2()
