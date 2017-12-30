# -*- coding: UTF-8 -*-
# from sy2 import *


class Produce():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Terminator():
    def __init__(self, ontology, pri=set(), equ=set(), beh=set()):
        self.ontology = ontology
        self.pri = pri
        self.equ = equ
        self.beh = beh


class CFG():
    def __init__(self, terminator_set=[], non_terminator_set=[], start_character='', produce=[]):
        self.terminator_set = terminator_set            # 终结符号集
        self.non_terminator_set = non_terminator_set    # 非终结符号集
        self.start_character = start_character          # 开始符
        self.produce = produce                          # 产生式

    def read(self, file_path):
        # 从文件中读出文法
        with open(file_path, 'r') as f:
            self.terminator_set = f.readline().strip().split(' ')
            if len(self.terminator_set) != len(list(set(self.terminator_set))):
                print '终结符集含有重复元素'
                return -1
            self.non_terminator_set = f.readline().strip().split(' ')
            if len(self.non_terminator_set) != len(list(set(self.non_terminator_set))):
                print '非终结符集含有重复元素'
                return -1
            a = f.readline().strip()
            if len(a) != 1:
                print '开始符有且只能有一个元素'
                return -1
            self.start_character = a
            for line in f.readlines():
                p = line.strip().split('->')
                if set(p[0]).issubset(set(self.non_terminator_set)) and \
                    (set(list(p[1])) - set('|ε')).issubset(set(self.non_terminator_set) | set(self.terminator_set)):
                    self.produce.append(Produce(p[0], p[1].split('|')))
                else:
                    print line, '出错'
                    return -1
            return 1

    def show(self):
        # 打印文法
        for i in self.terminator_set:
            print i,
        print
        for i in self.non_terminator_set:
            print i,
        print
        print self.start_character
        for p in self.produce:
            # print p.left, p.right
            print p.left + '->' + '|'.join(p.right)

    def firstvt(self, a):
        if a not in self.non_terminator_set:
            print a, '不是非终结符'
            return
        fir = set()
        s = flat([p.right for p in self.produce if p.left == a])
        for i in s:
            if i[0] in self.terminator_set:
                fir.add(i[0])
            else:
                if a != i[0]:
                    fir = fir | self.firstvt(i[0])
                if len(i) > 1 and i[1] in self.terminator_set:
                    fir.add(i[1])
        return fir

    def lastvt(self, a):
        if a not in self.non_terminator_set:
            print a, '不是非终结符'
            return
        las = set()
        s = flat([p.right for p in self.produce if p.left == a])
        for i in s:
            if i[-1] in self.terminator_set:
                las.add(i[-1])
            else:
                if a != i[-1]:
                    las = las | self.lastvt(i[-1])
                if len(i) > 1 and i[-2] in self.terminator_set:
                    las.add(i[-2])
        return las

    def priority_relationship(self, b):
        relationship = {i: Terminator(i) for i in self.terminator_set}
        s = [i for p in self.produce for i in p.right]
        for i in s:
            for j in range(len(i)):
                if i[j] in self.terminator_set:
                    if len(i) - j > 1 and i[j + 1] in self.terminator_set:
                        relationship[i[j]].equ = relationship[i[j]].equ | set(i[j + 1])
                    if len(i) - j > 1 and i[j + 1] in self.non_terminator_set:
                        relationship[i[j]].pri = relationship[i[j]].pri | self.firstvt(i[j + 1])
                    if len(i) - j > 2 and i[j + 2] in self.terminator_set:
                        relationship[i[j]].equ = relationship[i[j]].equ | set(i[j + 2])
                    if j > 0 and i[j - 1] in self.non_terminator_set:
                        for k in self.lastvt(i[j - 1]):
                            relationship[k].beh = relationship[k].beh | set(i[j])

        relationship[b] = Terminator(b)
        relationship[b].equ = relationship[b].equ | set(b)
        relationship[b].pri = relationship[b].pri | set(self.firstvt(self.start_character))
        for k in self.lastvt(self.start_character):
            relationship[k].beh = relationship[k].beh | set(b)
        self.relationship = relationship

    def show_table(self):
        t = [i for i in self.relationship]
        t.sort()
        # t = ['+', '*', 'i', '(', ')', '#']
        table = [[' '] * len(t) for _ in range(len(t))]
        for i in t:
            for j in self.relationship[i].pri:
                table[t.index(i)][t.index(j)] = '<'
            for j in self.relationship[i].equ:
                table[t.index(i)][t.index(j)] = '='
            for j in self.relationship[i].beh:
                table[t.index(i)][t.index(j)] = '>'
        print ' ' * 3,
        for i in t:
            print '%-3s' % i,
        print
        for i in range(len(t)):
            print '%-3s' % t[i],
            for j in range(len(t)):
                print '%-3s' % table[i][j],
            print


    def check_opg(self):
        # 判断是否是算符优先文法
        s = [i for p in self.produce for i in p.right]
        if len([1 for i in s for j in range(len(i) - 1)
                if i[j] in self.non_terminator_set and i[j + 1] in self.non_terminator_set]) > 0:
            return 0
        for i in self.relationship:
            if len(self.relationship[i].pri & self.relationship[i].equ) + len(self.relationship[i].pri & self.relationship[i].beh) + len(self.relationship[i].equ & self.relationship[i].beh) > 0:
                return 0
        return 1


flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]


Gs = CFG()
Gs.read('1.txt')
Gs.show()
print
for i in Gs.non_terminator_set:
    print 'FIRSTVT(%s) =' % i, Gs.firstvt(i)
    print 'LASTVT(%s）=' % i, Gs.lastvt(i)
print

Gs.priority_relationship('#')
if Gs.check_opg():
    Gs.show_table()
else:
    print '该文法不是算符优先文法'
