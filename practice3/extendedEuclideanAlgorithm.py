from os import system
equaA, equaB, equaC = [], [], []

def gcd(a, b):
    if (a == 0):
        return b
    val = gcd(b % a, a)
    equaA.append([b, (a, b//a), b - a * (b//a)])
    equaB.append([b - a * (b//a), b, (a, b//a)])
    return val

def egcd(a, b):
    if (a == 0):
        return (b, 0, 1)
    else:
        val, x, y = egcd(b % a, a)
        equaC.append([val, (b, x), (a, y - x * (b//a))])
        return (val, y - (b//a) * x, x)

if __name__ == "__main__":
    res = 0
    while (res != 1):
        system('cls')
        print("\n\t\t\tExtended Euclidean Algorithm")
        print("Enter \u03b1: ", end = '')
        alpha = int(input())
        print("Enter n: ", end='')
        n = int(input())
        res = gcd(n, alpha)
    print("\n\t1° Step: Set the maximum value in terms of the minimum then add the rest.")
    for i in equaA[:-1][::-1]:
        print('\t\t%3s %s' % (str(i[0]), " = " + str(i[1][0]) + "("+ str(i[1][1]) + ") + "  +  str(i[2])))
    j = 3
    print("\n\t2° Step: Rearrange so the left side of the equation has what was added in step 1.")
    for i in equaB[0:-1][::-1][0:-1]:
        print('\t\t' + chr(97 + len(equaB) - j) + ') %3s %s' % (str(i[0]), " = " + str(i[1])  + " - " + str(i[2][0]) +  "("+ str(i[2][1]) + ")"))
        j += 1
    print("\n\t3° Step: In eq. a) clear the greates value, and then replance it in eq. b) and then minize, and so forth and so on with all of them.")
    GCD, X, Y = egcd(n, alpha)
    for i in equaC[1:]:
        print('\t\t%2s = %s(%s) + %s(%s)' % (str(i[0]), str(i[1][0]), str(i[1][1]), str(i[2][0]), str(i[2][1])))
    print("\n\tAs: " + str(Y) + " mod " + str(n) + " = " + str(Y % n))
    print("\tAnd: " + str(alpha) + "(" + str(Y % n) + ") = " + str(alpha * (Y % n)))
    print("\tBut: " + str(alpha * (Y % n)) + " mod " + str(n) + " = " + str((alpha * (Y % n)) % n))

    if ((alpha * (Y % n)) % n) == 1:
        print("\n\t\tThus \u03b1\u207b\u00b9 = " + str(Y % n))
        print("\t\t" + "(" + str(alpha) + ")(" + str(Y % n) + ") mod " + str(n) + " = " + str(((alpha)*(Y % n))%n))
    else:
        print("n and \u03b1\u207b\u00b9 aren't coprimes")