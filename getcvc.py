import argparse
import math
import sys
import textwrap

n=m=4
sboxes = dict()


def Init():
    print('S: ARRAY BITVECTOR({:d}) OF BITVECTOR({:d});'.format(m,n))
    print('x,a,SumFreq:BITVECTOR({:d});'.format(m))
    print('u,L,b:BITVECTOR({:d});'.format(n))
    print('DDT:ARRAY BITVECTOR({:d}) OF BITVECTOR({:d});'.format(m+n,m))
    print('Freq,FreqLAT:ARRAY BITVECTOR({:d}) OF BITVECTOR({:d});'.format(m + n, 1))
    print('IsTrue:ARRAY BITVECTOR({:d}) OF BITVECTOR(1);'.format(2*m+n))
    print('IsTrueLAT:ARRAY BITVECTOR({:d}) OF BITVECTOR(1);'.format(2 * m + n))
    print('ABLAT,LATT,LAT:ARRAY BITVECTOR({:d}) OF BITVECTOR({:d});'.format(m + n,n))
    print('SumFreqLAT:ARRAY BITVECTOR({:d}) OF BITVECTOR({:d});'.format(m + n, 1))


def init_SBox(n):
    l=2**n

    for i in range(0, l-1):
        for j in range(i + 1, l):
            print('ASSERT(S[0bin' + '{0:04b}'.format(i) + ']/=S[0bin' + '{0:04b}'.format(j) + ']);')

def S1_define(n):
    l=2**n
    x=y=0
    for i in range(0,l):
        print('ASSERT(S[0bin'+'{0:04b}'.format(i)+']=y_{:d}'.format(y),end='')
        for j in range(1,n):
            print('@y_{:d}'.format(y+j),end='')
        print(');')
        y=y+n
    for i in range(0,l):
        print('ASSERT(0bin'+'{0:04b}'.format(i)+'=x_{:d}'.format(x),end='')
        for j in range(1,n):
            print('@x_{:d}'.format(x+j),end='')
        print(');')
        x=x+n
    x=y=0

    q=t=0
    for i in range(0, l):
        a = b = 0
        Z = ['x_' + str(x + _x) for _x in range(n)]
        Z1 = ['x_' + str(x + _x) for _x in range(n)]
        Z2 = ['x_' + str(x + _x) for _x in range(n)]
        for d in range(0, 4):
            if (d == 0 or d == 2):
                for _ in range(0, 2):
                    print(
                        'ASSERT(t_{:d}=BVPLUS(1 , q_{:d} & q_{:d} , b_{:d} & q_{:d} , b_{:d} & q_{:d} , b_{:d} ));'.format(
                            t, q, q + 1, b , q, b, q + 1, b + 1))
                    b = b + 2
                    for _q in range(0, 2):
                        print('ASSERT(q_{:d}=BVPLUS(1'.format(q + _q), end='')
                        for z in Z:
                            print(', a_{:d} & {:s}'.format(a, z), end='')
                            a = a + 1
                        print(' ));')
                        if(i==0):
                            print('ASSERT(BVLE(BVPLUS(4', end='')
                            for _a in range(0, len(Z)):
                                print(', 0bin000@a_{:d} '.format(a - len(Z) + _a), end='')
                            print('),0x1));')
                    q = q + 2
                    t = t + 1

                Z.append('t_' + str(t - 2))
                Z.append('t_' + str(t - 1))
            else:
                for _ in range(0, 2):
                    print('ASSERT(t_{:d}=BVPLUS(1'.format(t), end='')
                    for z in Z:
                        print(', a_{:d} & {:s}'.format(a, z), end='')
                        a = a + 1
                    print(',a_{:d}));'.format(a))
                    if(i==0):
                        print('ASSERT(BVLE(BVPLUS(4', end='')
                        for _a in range(0, len(Z)):
                            print(', 0bin000@a_{:d} '.format(a - len(Z) + _a), end='')
                        print('),0x2));')
                    a = a + 1
                    t = t + 1
                Z.append('t_' + str(t - 2))
                Z.append('t_' + str(t - 1))

        for j in range(0, n):
            print('ASSERT(y_{:d}=BVPLUS(1'.format(y+j), end='')
            for z in range(0,8):
                print(', a_{:d} & t_{:d}'.format(a, z+8*i), end='')
                a = a + 1
            print('));')
            if(i==0):
                print('ASSERT(BVPLUS(4', end='')
                for _a in range(0, 8):
                    print(', 0bin000@a_{:d} '.format(a - 8 + _a), end='')
                print(')=0x1);')

        x = y = x + n
    f = open('init.txt', 'a')
    for i in range(a - 1):
        print('a_{:d},'.format(i), end='', file=f)

    print(('a_{:d}'.format(a - 1) + ':BITVECTOR(1);'), file=f)
    for i in range(0, t):
        print('t_{:d},'.format(i), end='', file=f)
    print('t:BITVECTOR(1);', file=f)
    for i in range(0, q):
        print('q_{:d},'.format(i), end='', file=f)
    print('xq:BITVECTOR(1);', file=f)
    for i in range(0, b):
        print('b_{:d},'.format(i), end='', file=f)
    print('xb:BITVECTOR(1);', file=f)
    f.close()

def print_DDT(U):
    for a in range(1, 2 ** m):
        for b in range(1, 2 ** n):
            L = []
            for x0 in range(0, 2 ** m):
                for x1 in range(x0, 2 ** m):
                    if (x0 ^ x1 == a):
                        text = 'ASSERT(IF BVXOR(S[0x%X' % x0 + '],S[0x%X' % x1 + '])=0x%X' % b + ' THEN IsTrue[0x%X' % a + '@0x%X' % b + '@0x%X' % x0 + ']=0bin1 ELSE IsTrue[0x%X' % a + '@0x%X' % b + '@0x%X' % x0 + ']=0bin0 ENDIF);'
                        L.append(x0)
                        print(text)

            print('ASSERT(DDT[0x%X' % a + '@0x%X' % b + ']=BVPLUS(4', end='')
            for x in L:
                print(',0bin000@IsTrue[0x%X' % a + '@0x%X' % b + '@0x%X' % x + ']', end='')
            print('));')
            if ((a + b) != 0):
                print('ASSERT(BVLE(DDT[0x%X' % a + '@0x%X' % b + '],0x%X' % U + '));')

def inner(x,a):
    sum=0
    for i in range(0,m):
        if((a>>i)&0x1):
            sum=sum^((x>>i)&0x1)
    return sum

def bit_to_list(t, n):
    S = [0 for i in range(n)]
    i = -1
    while t != 0:
        S[i] = t % 2
        t = t >> 1
        i -= 1
    return S

def LAT(L):
    l = int(L / 2)
    for i in range(0, 2 ** m):
        for j in range(0, 2 ** m):
            for k in range(0, 2 ** m):
                left = inner(k, i)
                M = bit_to_list(j, m)
                text = 'ASSERT( IF BVPLUS(1,0bin0'
                for t in range(0, m):
                    if (M[t] != 0):
                        text = text + ',S[0bin' + '{0:04b}'.format(k) + '][{:d}:{:d}]'.format(m - 1 - t, m - 1 - t)

                text = text + ')=0bin{0:01b}'.format(left) + ' THEN IsTrueLAT[0bin' + '{0:04b}'.format(
                    i) + '@0bin' + '{0:04b}'.format(
                    j) + '@0bin' + '{0:04b}'.format(k) + ']=0bin1 ELSE IsTrueLAT[0bin' + '{0:04b}'.format(
                    i) + '@0bin' + '{0:04b}'.format(j) + '@0bin' + '{0:04b}'.format(k) + ']=0bin0 ENDIF);'
                print(text)
            textn = 'ASSERT(LAT[0bin' + '{0:04b}'.format(i) + '@0bin' + '{0:04b}'.format(j) + ']=BVPLUS(4'
            print(textn, end='')
            for k in range(0, 2 ** m):
                text = ',0bin000@IsTrueLAT[0bin' + '{0:04b}'.format(i) + '@0bin' + '{0:04b}'.format(
                    j) + '@0bin' + '{0:04b}'.format(k) + ']'
                print(text, end='')
            print('));')
            if ((i + j) != 0):
                text = 'ASSERT( BVLE(LAT[0bin' + '{0:04b}'.format(i) + '@0bin' + '{0:04b}'.format(
                    j) + '],0bin' + '{0:04b}'.format(l + 8) + '));'
                print(text)
                text = 'ASSERT( BVGE(LAT[0bin' + '{0:04b}'.format(i) + '@0bin' + '{0:04b}'.format(
                    j) + '],0bin' + '{0:04b}'.format(8 - l) + '));'
                print(text)
    

def maxonea(start, end):
    for i in range(start, end):
        for j in range(i + 1, end):
            print('ASSERT(a_{:d} & a_{:d}=0bin0);'.format(i, j))

def maxone(lista, listb):
    for i in lista:
        for j in listb:
            print('ASSERT(a_{:d} & a_{:d}=0bin0);'.format(i, j))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('mode', metavar='mode', choices=['mc', 'bgc', 'gc', 'depth'], help="Mode to operate in. One of:\nmc     for multiplicative complexity\nbgc    for bitslice gate complexity\ngc     for gate complexity\ndepth  for depth complexity")
    parser.add_argument('k', metavar='k', type=int, choices=range(1, 50), help=textwrap.fill('Value to test for. E.g. number of nonlinear gates for mode=mc, circuit depth for mode=depth, etc.', 68))
    parser.add_argument('width', metavar='width', nargs='?', type=int, choices=range(1, 50), help=textwrap.fill('Only applicable to mode=depth. Set width of circuit layer to test for.', 68))
    args = parser.parse_args()
    if args.mode == 'depth' and args.width is None:
        parser.print_usage(sys.stderr)
        print(sys.argv[0] + ': error: the following arguments are required for mode=depth: width', file=sys.stderr)
        exit()

    n = m = 4
    x = y = q = t = 0
    for i in range((2**n)*n):
        print('x_{:d},y_{:d}'.format(i,i)+':BITVECTOR(1);')
    Init()
    init_SBox(n)
    S1_define(4)
    print_DDT(2)
    LAT(8)

    print('QUERY(FALSE);\nCOUNTEREXAMPLE;')

