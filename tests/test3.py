import random
import numpy as np
import matplotlib.pyplot as plt

# Función de generación
def F(X0, X1, X2, F1, F2, R1, R2):
    D = ((X0 ^ R1) + R2) % pow(2,32)
    D1 = (R1 + X1) % pow(2,32)
    D2 = R2 ^ X2
    R1 = D1 ^ F1
    R2 = D2 ^ F2
    return([D, R1, R2])

# Test de distribución
# (Hacemos uso de claves aleatorias)
LFSR = []
for i in range(16):
    LFSR.append(random.getrandbits(31))

R1 = random.getrandbits(32)
R2 = random.getrandbits(32)

x = random.getrandbits(32)
y = random.getrandbits(32)

# Valor que almacena los valores generados
graphy = []

# Valor que almacena el número de bits generados
graphx = []

# Generamos 2*10⁴ bits
# Fase de inicialización
for i in range (32):
    X0 = int(format(LFSR[15], f'0{31}b')[:16] + format(LFSR[14], f'0{31}b')[15:], 2)
    X1 = int(format(LFSR[11], f'0{31}b')[15:] + format(LFSR[9], f'0{31}b')[:16], 2)
    X2 = int(format(LFSR[7], f'0{31}b')[:16] + format(LFSR[5], f'0{31}b')[15:], 2)
    X3 = int(format(LFSR[2], f'0{31}b')[15:] + format(LFSR[0], f'0{31}b')[:16], 2)

    F1 = (2 * pow(x,2) - 1) % pow(2,32)
    F2 = (4 * pow(y,3) - 3 * y) % pow(2,32)

    x = F1
    y = F2

    D, R1, R2 = F(X0, X1, X2, F1, F2, R1, R2)

    u = D >> 1
    v = (pow(2,13)*LFSR[15] + pow(2,19)*LFSR[13] + pow(2,17)*LFSR[10] + pow(2,20)*LFSR[6] + (1+pow(2,8))*LFSR[0]) % (pow(2,31)-1)

    s = (u + v) % (pow(2,31)-1)
    if s == 0:
        s = pow(2,31)-1

    LFSR.insert(0,s)
    LFSR.pop(-1)

# Fase de generación
for i in range(10000):
    X0 = int(format(LFSR[15], f'0{31}b')[:16] + format(LFSR[14], f'0{31}b')[15:], 2)
    X1 = int(format(LFSR[11], f'0{31}b')[15:] + format(LFSR[9], f'0{31}b')[:16], 2)
    X2 = int(format(LFSR[7], f'0{31}b')[:16] + format(LFSR[5], f'0{31}b')[15:], 2)
    X3 = int(format(LFSR[2], f'0{31}b')[15:] + format(LFSR[0], f'0{31}b')[:16], 2)

    F1 = (2 * pow(x,2) - 1) % pow(2,32)
    F2 = (4 * pow(y,3) - 3 * y) % pow(2,32)

    x = F1
    y = F2

    D, R1, R2 = F(X0, X1, X2, F1, F2, R1, R2)

    s = (pow(2,13)*LFSR[15] + pow(2,19)*LFSR[13] + pow(2,17)*LFSR[10] + pow(2,20)*LFSR[6] + (1+pow(2,8))*LFSR[0]) % (pow(2,31)-1)
    if s == 0:
        s = pow(2,31)-1

    LFSR.insert(0,s)
    LFSR.pop(-1)

    Z = (D ^ X3)%256
    graphy.append(Z)
    graphx.append(i)

plt.scatter(graphx, graphy, marker='.', color='black')
plt.title('Test de distribución')
plt.xlabel('Posición')
plt.ylabel('Valor')

plt.xlim(0,10000)
plt.ylim(0,256)
plt.show()
