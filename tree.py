# coding=utf-8

__author__ = "ericwu<zephor@qq.com>"


class Node(object):
    def __init__(self, key, value):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.bf = 0


class AVLTree(object):
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        a = p = self.root
        if a is None:
            self.root = Node(key, value)
            return
        a_father, p_father = None, None
        while p is not None:
            if p.bf != 0:
                a_father, a, = p_father, p
            p_father = p
            if key < p.key:
                p = p.left
            else:
                p = p.right

        node = Node(key, value)
        if key < p_father.key:
            p_father.left = node
        else:
            p_father.right = node

        if key < a.key:
            p = b = a.left
            d = 1
        else:
            p = b = a.right
            d = -1

        while p != node:
            if key < p.key:
                p.bf = 1
                p = p.left
            else:
                p.bf = -1
                p = p.right
        if a.bf == 0:
            a.bf = d
            return
        if a.bf == -d:
            a.bf = 0
            return

        if d == 1:
            if b.bf == 1:
                a.left = b.right
                b.right = a
                a.bf = b.bf = 0
            else:
                c = b.right
                a.left, b.right = c.right, c.left
                c.left, c.right = b, a
                if c.bf == 0:
                    a.bf = b.bf = 0
                elif c.bf == 1:
                    a.bf = -1
                    b.bf = 0
                else:
                    a.bf = 0
                    b.bf = 1
                c.bf = 0
                b = c
        else:
            if b.bf == -1:
                a.right = b.left
                b.left = a
                a.bf = b.bf = 0
            else:
                c = b.left
                a.right, b.left = c.left, c.right
                c.left, c.right = a, b
                if c.bf == 0:
                    a.bf = b.bf = 0
                elif c.bf == 1:
                    a.bf = 0
                    b.bf = -1
                else:
                    a.bf = 1
                    b.bf = 0
                c.bf = 0
                b = c
        if a_father is None:
            self.root = b
        else:
            if a_father.key > b.key:
                a_father.left = b
            else:
                a_father.right = b

    def search(self, start_key, end_key):
        start_n, end_n = None, None
        bt = self.root
        while bt is not None:
            if start_key < bt.key:
                if bt.left is None:
                    start_n = bt
                    break
                start_n = bt
                bt = bt.left
            elif start_key > bt.key:
                bt = bt.right
            else:
                if bt.left is None or start_key > bt.left.key:
                    start_n = bt
                    break
                bt = bt.left
        bt = self.root
        while bt is not None:
            if end_key < bt.key:
                bt = bt.left
            elif end_key > bt.key:
                if bt.right is None:
                    end_n = bt
                    break
                end_n = bt
                bt = bt.right
            else:
                if bt.right is None or end_key < bt.right.key:
                    end_n = bt
                    break
                bt = bt.right
        return self._get_values(start_n, end_n)

    def _get_values(self, start, end):
        bt, stack, res = self.root, [], []
        if bt is None:
            return res
        if start is not None:
            while bt.key < start.key:
                bt = bt.right
        while bt is not None or stack:
            while bt is not None:
                stack.append(bt)
                if bt is start:
                    break
                bt = bt.left
            bt = stack.pop()
            res.append(bt.value)
            if bt is end:
                break
            bt = bt.right
        return res

    def print_all_values(self):
        bt, s = self.root, []
        while bt is not None or s:
            while bt is not None:
                s.append(bt)
                bt = bt.left
            bt = s.pop()
            print bt.key, bt.value
            bt = bt.right


if __name__ == "__main__":
    entries = [(5, 'a'), (2.5, 'g'), (2.3, 'h'), (3, 'b'), (2, 'd'), (4, 'e'),
               (3.5, 'f')]
    t = AVLTree()
    for _key, _value in entries:
        t.insert(_key, _value)
    t.print_all_values()
    print
    print t.search(1.9, 2.7)
    t.insert(1, "i")
    print
    t.print_all_values()

    print
    entries = [(2.5, 'g'), (3, 'b'), (4, 'e'), (3.5, 'f')]
    t = AVLTree()
    for _key, _value in entries:
        t.insert(_key, _value)
    t.print_all_values()
    print 'after inserting\n'
    t.insert(3.2, 'i')
    t.print_all_values()
