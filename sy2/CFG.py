# -*- coding: UTF-8 -*-


flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L]


def before(a, b):
    # 判断a是否在b前
    return len(a) < len(b) and a == b[0:len(a)]


def sortlength(L):
    # 按元素长度排序
    n = len(L)
    for i in range(n):
        k = i
        j = i + 1
        while j < n:
            if len(L[k]) > len(L[j]):
                k = j
            j = j + 1
        if i != k:
            L[k], L[i] = L[i], L[k]


class Produce():
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def left_recursion(self):
        # 判断是否左递归
        for i in self.right:
            if self.left == i[0]:
                # print self.left + '->' + '|'.join(self.right), '存在左递归'
                return 1
        return 0

    def left_common_factor(self):
        # 判断是否含有左公因子
        a = [i[0] for i in self.right]
        if len(list(set(a))) != len(a):
            # print self.left + '->' + '|'.join(self.right), '存在左公因子'
            return 1
        else:
            return 0


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

    def input(self, file_path):
        # 输入文法
        self.terminator_set = raw_input().strip().split(' ')
        if len(self.terminator_set) != len(list(set(self.terminator_set))):
            print '终结符集含有重复元素'
            return -1
        self.non_terminator_set = raw_input().strip().split(' ')
        if len(self.non_terminator_set) != len(list(set(self.non_terminator_set))):
            print '非终结符集含有重复元素'
            return -1
        a = raw_input().strip()
        if len(a) != 1:
            print '开始符有且只能有一个元素'
            return -1
        self.start_character = a
        t = raw_input()
        for _ in range(int(t)):
            p = raw_input().split('->')
            if set(p[0]).issubset(set(self.non_terminator_set)) and \
                    (set(list(p[1])) - set('|ε')).issubset(set(self.non_terminator_set) | set(self.terminator_set)):
                self.produce.append(Produce(p[0], p[1].split('|')))
            else:
                print p, '出错'
                return -1
        return 1

    def show(self):
        # 打印文法
        print '终结符集'
        for i in self.terminator_set:
            print i,
        print
        print '非终结符集'
        for i in self.non_terminator_set:
            print i,
        print
        print '开始符'
        print self.start_character
        print '产生式'
        for p in self.produce:
            # print p.left, p.right
            print p.left + '->' + '|'.join(p.right)

    def write(self, file_path):
        with open(file_path, 'wb') as f:
            for i in self.terminator_set:
                f.write(i + ' ')
            f.write('\n')
            for i in self.non_terminator_set:
                f.write(i + ' ')
            f.write('\n')
            f.write(self.start_character + '\n')
            for p in self.produce:
                f.write(p.left + '->' + '|'.join(p.right) + '\n')

    def left_recursion(self):
        # 判断文法是否含有左递归
        if len([1 for p in self.produce if p.left_recursion()]) > 0:
            return 1
        return 0

    def eliminate_recursion(self):
        # 消除左递归
        a = [p for p in self.produce if p.left_recursion()]
        for p in a:
            f = 'A'
            while f in self.non_terminator_set:
                f = chr(ord(f) + 1)
            self.non_terminator_set.append(f)
            self.produce.remove(p)
            f1 = []
            f2 = []
            for i in p.right:
                if i[0] != p.left:
                    f1.append(i + f)
                else:
                    f2.append(i[1:] + f)
            f2.append('ε')
            self.produce.append(Produce(p.left, f1))
            self.produce.append(Produce(f, f2))

    def left_common_factor(self):
        # 判断文法是否含有左递归
        if len([1 for p in self.produce if p.left_common_factor()]) > 0:
            return 1
        return 0

    def eliminate_factor(self):
        # 提取左公因子
        a = [p for p in self.produce if p.left_common_factor()]
        for p in a:
            self.produce.remove(p)
            f = 'A'
            while f in self.non_terminator_set:
                f = chr(ord(f) + 1)
            c = [[i[0:j] for j in range(1, len(i) + 1)] for i in p.right]
            d = [c[i][j] for i in range(len(c)) for j in range(len(c[i]))]
            e = list(set([d[i] for i in range(len(d)) for j in range(i + 1, len(d)) if d[i] == d[j]]))
            g = {}      # 用字典存储带有共同左因子的右部
            for i in range(len(e)):
                g[e[i]] = [[j for j in p.right if len(j) >= len(e[i]) and j[0:len(e[i])] == e[i]],
                           [j for j in p.right if len(j) < len(e[i]) or j[0:len(e[i])] != e[i]]]
            h = list(set([i for i in e for j in e if before(i, j) and len(g[i][0]) - len(g[j][0]) < 2]))
            for i in h:     # 删除多余的左因子
                e.remove(i)
                del g[i]
            sortlength(e)
            e.reverse()
            for i in e:
                f1 = g[i][1]
                f1.insert(0, i + f)
                f2 = [g[i][0][j][len(i):] for j in range(len(g[i][0]))]
                for j in f2:
                    if j == '':
                        f2[f2.index(j)] = '\xce\xb5'
                self.produce.append(Produce(p.left, f1))
                self.produce.append(Produce(f, f2))

    def f(self, a):
        if a not in self.non_terminator_set:
            print a, '不在文法的非终结符中'
            return
        return [i.right for i in self.produce if a == i.left][0]

    def first(self, a):
        # 求a的FIRST集
        if a not in self.non_terminator_set and a not in self.terminator_set:
            print a, '不在文法的终结或非终结符中'
            return
        if a == '\xce\xb5':
            return set(list(['\xce\xb5']))
        elif a in self.terminator_set:
            return set(a)
        fir = set([i[0] for i in self.f(a) if i[0] in self.terminator_set])
        fir_n = set([i[0] for i in self.f(a) if i[0] in self.non_terminator_set])
        if '\xce\xb5' in self.f(a):
            fir.add('\xce\xb5')
        elif len([1 for i in fir_n if '\xce\xb5' in self.first(i)]) == len(fir_n) > 0 and len(fir) == 0:
            fir.add('\xce\xb5')
        for i in fir_n:
            fir = fir | (self.first(i) - set(list(['\xce\xb5'])))
        return set(fir)

    def follow(self, a):
        # 求a的FOLLOW集
        if a not in self.non_terminator_set:
            print a, '不在文法非终结符中'
            return
        fol = set()
        s = flat([p.right for p in self.produce])
        if a == self.start_character or len([1 for i in s if i[-1] == a]) > 0:
            fol.add('#')
        back1 = [i[j + 1:] for i in s for j in range(len(i) - 1) if i[j] == a]
        for i in back1:
            for j in range(len(i)):
                fol = fol | (self.first(i[j]) - set(list(['\xce\xb5'])))
                if '\xce\xb5' not in self.first(i[j]):
                    break
        le = [p.left for p in self.produce for i in p.right if i[-1] == a and p.left != a]
        for i in le:
            fol = fol | self.follow(i)
        return fol

    def check_ll1(self):
        for p in self.produce:
            if '\xce\xb5' in p.right:
                if len([1 for i in p.right if i != '\xce\xb5' and len(self.first(i[0]) & self.follow(p.left)) != 0]) > 0:
                    return 0
            else:
                if len([1 for i in range(len(p.right)) for j in range(i + 1, len(p.right))
                        if len(self.first(p.right[i]) & self.first(p.right[j])) > 0]) > 0:
                    return 0
        return 1

    def analysis(self):
        # 求文法的LL(1)分析表
        terminator = [i for i in self.terminator_set]
        if '\xce\xb5' in terminator:
            terminator.remove('\xce\xb5')
        terminator.append('#')
        table = [[''] * len(terminator) for _ in range(len(self.non_terminator_set))]
        for p in self.produce:
            for i in p.right:
                if i != '\xce\xb5':
                    for j in self.first(i[0]):
                        table[self.non_terminator_set.index(p.left)][terminator.index(j)] = p.left + '->' + i
                else:
                    for j in self.follow(p.left):
                        table[self.non_terminator_set.index(p.left)][terminator.index(j)] = p.left + '->' + '\xce\xb5'
        self.table = table

    def showtable(self):
        # 打印文法的LL(1)分析表
        terminator = [i for i in self.terminator_set]
        if '\xce\xb5' in terminator:
            terminator.remove('\xce\xb5')
        terminator.append('#')
        print '-' * len(terminator) * 5 + 'LL(1)分析表' + '-' * len(terminator) * 5
        print ' ' * 10,
        for i in terminator:
            print '%-10s' % i,
        print
        for i in range(len(self.table)):
            print '%-10s' % self.non_terminator_set[i],
            for j in self.table[i]:
                print '%-10s' % j,
            print
        print '-' * (len(terminator) + 1) * 10



path = '/Users/mio/code/Compilation/sy2/3.txt'
GS = CFG()
if GS.read(path) != 1:
    exit(-1)

while GS.left_recursion():
    GS.eliminate_recursion()
while GS.left_common_factor():
    GS.eliminate_factor()
GS.show()

for i in GS.non_terminator_set:
    print 'FIRST(%s) =' % i, GS.first(i)
for i in GS.non_terminator_set:
    print 'FOLLOW(%s) =' % i, GS.follow(i)

if GS.check_ll1():
    GS.analysis()
    GS.showtable()
else:
    print '该文法不是LL(1)文法'