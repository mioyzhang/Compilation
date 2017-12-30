# -*- coding: UTF-8 -*-


class Edge:
    def __init__(self, start, cost, dest):
        self.start = start
        self.cost = cost
        self.dest = dest


class DFA:
    def __init__(self, state_set=[], alphabet=[], mapping_function=[], initial_state=[], final_state=[]):
        self.state_set = state_set                  # 有限状态集
        self.alphabet = alphabet                    # 字母表
        self.mapping_function = mapping_function    # 映射函数
        self.initial_state = initial_state          # 初态
        self.final_state = final_state              # 终态

    def read(self, file_path):
        # 从文件中读取DFA
        with open(file_path, 'r') as f:
            state_set = f.readline().strip(). split(' ')
            if len(state_set) != len(list(set(state_set))):
                print '状态集中含有重复元素'
                return -1
            alphabet = f.readline().strip().split(' ')
            if len(alphabet) != len(list(set(alphabet))):
                print '字母表中含有重复元素'
                return -1
            initial_state = f.readline().strip().split(' ')
            if len(initial_state) != 1:
                print '确定有限自动机只能含有一个初态'
                return -1
            if state_set.count(initial_state[0]) != 1:
                print '初态不在状态集中'
                return -1
            final_state = f.readline().strip().split(' ')
            if len(final_state) < 1:
                print '终态不能为空'
                return -1
            for i in final_state:
                if state_set.count(i) != 1:
                    print i, '不在状态集中'
                    return -1
            mapping_function = []
            for line in f.readlines():
                func = line.strip().split(' ')
                if state_set.count(func[0]) != 1 or state_set.count(func[2]) != 1 or state_set.count(func[2]) != 1:
                    print 'f(%s, %s) = %s不符规则' % (func[0], func[1], func[2])
                    return -1
                mapping_function.append(Edge(func[0], func[1], func[2]))
        self.state_set = state_set
        self.alphabet = alphabet
        self.mapping_function = mapping_function
        self.initial_state = initial_state
        self.final_state = final_state
        return 1

    def input(self):
        # 通过输入的方式获取DFA
        state_set = raw_input('输入有限状态集(输入一行中间用空格隔开):\n').split(' ')
        if len(state_set) != len(list(set(state_set))):
            print '状态集中含有重复元素'
            return
        alphabet = raw_input('输入字母表\n').split(' ')
        if len(alphabet) != len(list(set(alphabet))):
            print '字母表中含有重复元素'
            return
        initial_state = raw_input('输入初态\n').split(' ')
        if len(initial_state) != 1:
            print '确定有限自动机只能含有一个初态'
            return
        if state_set.count(initial_state[0]) != 1:
            print '初态不在状态集中'
            return
        final_state = raw_input('输入终态集\n').split(' ')
        if len(final_state) < 1:
            print '终态不能为空'
            return
        for i in final_state:
            if state_set.count(i) != 1:
                print i, '不在状态集中'
                return
        mapping_function = []
        print '输入映射关系(先输入一个数字表示有多少个映射关系，每个映射占一行，中间用空格隔开)'
        for i in range(int(raw_input())):
            func = raw_input().split(' ')
            if state_set.count(func[0]) != 1 or state_set.count(func[2]) != 1 or state_set.count(func[2]) != 1:
                print 'f(%s, %s) = %s不符规则' % (func[0], func[1], func[2])
                return
            mapping_function.append(Edge(func[0], func[1], func[2]))

        self.state_set = state_set
        self.alphabet = alphabet
        self.mapping_function = mapping_function
        self.initial_state = initial_state
        self.final_state = final_state

    def write_dfa(self, file_path):
        # 将DFA写入文件
        with open(file_path, 'wb') as f:
            for i in self.state_set:
                f.write(i + ' ')
            f.write('\n')
            for i in self.alphabet:
                f.write(i + ' ')
            f.write('\n')
            for i in self.initial_state:
                f.write(i + ' ')
            f.write('\n')
            for i in self.final_state:
                f.write(i + ' ')
            f.write('\n')
            for edge in self.mapping_function:
                f.write(edge.start+ ' ' + edge.cost + ' ' + edge.dest + '\n')

    def show(self):
        # 输出DFA
        print '有限状态集:'
        for i in self.state_set:
            print i,
        print
        print '字母表:'
        for i in self.alphabet:
            print i,
        print
        print '初态:'
        for i in self.initial_state:
            print i,
        print
        print '终态集:'
        for i in self.final_state:
            print i,
        print
        print '映射函数:'
        for i in self.mapping_function:
            print 'f(%s, %s) = %s' % (i.start, i.cost, i.dest)

        print '状态转换表:'
        table = [[' '] * (len(self.alphabet) + 1) for i in range(len(self.state_set) + 1)]
        for i in range(len(self.alphabet)):
            table[0][i + 1] = self.alphabet[i]
        for i in range(len(self.state_set)):
            table[i + 1][0] = self.state_set[i]
        for i in self.mapping_function:
            table[self.state_set.index(i.start) + 1][self.alphabet.index(i.cost) + 1] = i.dest
        for line in table:
            for i in line:
                print '%-5s' % i,
            print

    def f(self, start, cost):
        # f(start, cost) = dest
        for edge in self.mapping_function:
            if edge.start == start and edge.cost == cost:
                return edge.dest

    def check(self, str):
        # 检查str是否属于DFA的语言集
        S = self.initial_state[0]
        for k in str:
            if k not in self.alphabet:
                return -1
            S = self.f(S, k)
        if S in self.final_state:
            return 1
        else:
            return 0

    def output(self, n):
        # 返回DFA其识别的所有长度小于等于n的字符串
        # return [j for i in range(1, n + 1) for j in string(i, self.alphabet) if self.check(j)]
        str = []
        for i in range(1, n + 1):
            for j in string(i, self.alphabet):
                if self.check(j):
                    str.append(j)
        return str

def string(n, a):
    # 返回由a中元素组成的所有长度为n的字符串
    if n == 1:
        return a
    return [i + j for i in a for j in string(n - 1, a)]


n = 3
path = '/Users/mio/code/Compilation/sy1/2.txt'
md = DFA()
if(md.read(path) != -1):
    md.show()
print '长度小于等于%d的所有符合DFA规则的字符串：' % n
for i in md.output(n):
    print i
print '请输入需要测试的字符串：'
while 1:
    print md.check(raw_input())