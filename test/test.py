
# dictionary
# list
# string

def testList():
    tag = 'testList'
    print('[testList ] Hello World!')
    print('[testList ] test list!')

    test = [1, 2, 3]
    test[0] # 1
    test[-1] # 3
    test[0:1] # [1]
    test[1:] # [2, 3]
    test[:-1] # [1, 2]
    test[:-2] # [1, 2]
    # test[start:end] -> start <= X < end
    print('[testList ] ', 'test', test)
    print('[testList ] ', 'len(test)', len(test))
    print('[testList ] ', 'test[:1]', test[:1])
    print('[testList ] ', 'test[:2]', test[:2])
    print('[testList ] ', 'test[:-1]', test[:-1])
    print('[testList ] ', 'test[:-2]', test[:-2])

    test.append(4)
    print('[testList ] ', 'test', test)
    print('[testList ] ', 'len(test)', len(test))

    test2 = [5, 6, 7]
    print('[testList ] ', 'test2', test2)
    print('[testList ] ', 'len(test2)', len(test2))

    test.extend(test2)
    print('[testList ] ', 'extent test2 -> test')
    print('[testList ] ', 'test2', test2)
    print('[testList ] ', 'len(test2)', len(test2))
    print('[testList ] ', 'test', test)
    print('[testList ] ', 'len(test)', len(test))

    a = range(5)
    print('range', a)

    for i in test:
        print('[testList ] ', 'for each', i)
    for i in range(len(test)):
        print('[testList ] ', 'for range', i, test[i])


    return

def testString():
    tag = '[testString]'
    a = str()
    print(tag, a)
    a = '123'
    print(tag, a)
    a = 'ABCdef'
    print(tag, a)
    print(tag, a.lower())
    print(tag, a.upper())
    print(tag, a.upper())

    a = '       ABC|d|e|f'
    s = a.split('|')
    print(tag, 'split', a, s, len(s))
    a = a.strip()
    print(tag, 'strip', a)

    return

def testDict():
    tag = 'testDict'

    d = {}
    d['a'] = [1, 2, 3]
    d['b'] = 2
    d['c'] = 3
    d['d'] = 4

    print(tag, d)
    print(tag, d['a'])
    try:
        print(tag, d['d'])
    except:
        pass

    if 'd' in d:
        print(tag, d['d'])

    for key in d:
        print(tag, 'key of dict', key, d[key])

    k = list(d.keys())
    print(tag, 'keys', k)

    return

def returnTuple():
    return (1, 2, 3)

def testTuple():
    tag = 'testTuple'
    t = returnTuple()
    print(tag, 't', t)
    print(tag, 't[0]', t[0])
    print(tag, 'len(t)', len(t))
    for i in t:
        print(tag, 'tuple in for', i)

    (a, b, c) = returnTuple()
    print(tag, 'reparated return', a, b, c)
    a, b, c = returnTuple()
    print(tag, 'reparated return', a, b, c)
    (a) = returnTuple()
    print(tag, 'reparated return', a)
    return

def arithLogicTest():
    tag = 'alt'
    a = 1
    print(tag, 10/3)
    print(tag, 10//3)
    a += 1
    print(tag, a)
    f = 10/3
    print(tag, f)
    print(tag, int(f))

    var = None


    a = 1
    b = 1
    if a is b:
        print(tag, 'a is b')
    else:
        print(tag, 'a is not b')

    a = [1, 2, 3]
    b = a
    c = a[:]
    print(tag, 'a is b', a is b)
    print(tag, 'a is c', a is c)


    return

def main():
    #arithLogicTest()
    testList()
    print('[main] Hello World!')
    return

print('name:', __name__)
if __name__ == '__main__':
    main()
elif __name__ == 'test':
    print('Imported!!!')
else:
    raise Exception('Invalid Name!!!')

