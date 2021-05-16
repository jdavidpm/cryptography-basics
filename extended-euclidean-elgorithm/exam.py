from math import floor
equaC = []
def egcd(a, b):
    if a == 0:
        return (b, 1, 0)
    else:
        gcd, y, x = egcd(b % a, a)
        equaC.append([1, (b, x), (a, y - x * (b//a))])
        return (gcd, x, y - (b//a) * x)

def _gcd(a, b):
    maxVal = max(a, b)
    minVal = min(a, b)
    coeVal = floor(maxVal/minVal)
    zeroVal = maxVal - coeVal * minVal
    if (zeroVal == 0): return
    #equaA.append([maxVal, (minVal, coeVal), zeroVal])
    #equaB.append([zeroVal, maxVal, (minVal, coeVal)]) #minVal must be negative
    _gcd(minVal, zeroVal)
gcd, x, y = egcd(115, 256)

for i in equaC:
    print(i)
#print(gcd, x)
#print(gcd(115, 256))