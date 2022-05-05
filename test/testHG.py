def Hello(input):
    strKor = str()
    strKor = 'GOOD MORNING' + ' ' + input
    #length1 = strKor.len
    for i in range(1, 10):
        print(i)
    return

def ReturnTuple(input):
    return ('a', 'b', 'c')

def TestTuple():
    tag = ReturnTuple('a')  #함수에서 input을 요구할 경우, 호출시 없으면 컴파일 에러 발생

    for i in tag:
        print(i)
    return

#딕은 해쉬 
def DicDickMobyDick(input):
    magic = {}
    magic[0] = 0x0
    magic[1] = 0x1      #16진수도 정수로 출력해줌
    magic[2] = 0x2
    magic['a'] = 0xA
    magic['b'] = 0xB
    magic['c'] = 0xC
    magic['d'] = 0xD
    magic['e'] = 0xE
    magic['BTS'] = 0xFFFF

    #for i in magic:
        #print(magic[i])
    
    #일단 되는 표현
    try :
        return magic[input]     
    except:
        return None


def ringIsString(input):
    temp = str(input)
    talk = str()
    talk = 'Let\'s Talk'
    temLen = len(temp)

    for i in range(temLen):
        print( talk + ' ' + str(i))     #talk + i는 에러 발생

    return talk

def main():
    #Hello('HG')
    #TestTuple()
    #res = DicDickMobyDick('1111')
    
    res = ringIsString('abcde')
    
    print(res)

    #print('[main] Hello World!') 

    return

print('name:', __name__)
if __name__ == '__main__':
    main()
elif __name__ == 'test':
    print('Imported!!!')
else:
    raise Exception('Invalid Name!!!')
