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

# Test de sensibilidad de clave
# Hacemos uso de 2 claves, donde una de ellas difiere ligéramente de la otra
LFSR = []
LFSRb = []
for i in range(16):
    val1 = random.getrandbits(31)
    val2 = val1 ^ 1
    LFSR.append(val1)
    LFSRb.append(val2)

R1 = random.getrandbits(32)
R2 = random.getrandbits(32)
R1b = R1 ^ 1
R2b = R2 ^ 1

x = random.getrandbits(32)
y = random.getrandbits(32)
xb = x ^ 1
yb = y ^ 1

# Valor que almacena los valores generados
graphy = []
graphyb = []

# Valor que almacena el número de bits generados
graphx = []
graphxb = []

# Generamos 100 bits para la clave A
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
for i in range(100):
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

# Generamos 100 bits para la clave B
# Fase de inicialización
for i in range (32):
    X0 = int(format(LFSRb[15], f'0{31}b')[:16] + format(LFSRb[14], f'0{31}b')[15:], 2)
    X1 = int(format(LFSRb[11], f'0{31}b')[15:] + format(LFSRb[9], f'0{31}b')[:16], 2)
    X2 = int(format(LFSRb[7], f'0{31}b')[:16] + format(LFSRb[5], f'0{31}b')[15:], 2)
    X3 = int(format(LFSRb[2], f'0{31}b')[15:] + format(LFSRb[0], f'0{31}b')[:16], 2)

    F1 = (2 * pow(xb,2) - 1) % pow(2,32)
    F2 = (4 * pow(yb,3) - 3 * yb) % pow(2,32)

    xb = F1
    yb = F2

    D, R1b, R2b = F(X0, X1, X2, F1, F2, R1b, R2b)

    u = D >> 1
    v = (pow(2,13)*LFSRb[15] + pow(2,19)*LFSRb[13] + pow(2,17)*LFSRb[10] + pow(2,20)*LFSRb[6] + (1+pow(2,8))*LFSRb[0]) % (pow(2,31)-1)

    s = (u + v) % (pow(2,31)-1)
    if s == 0:
        s = pow(2,31)-1

    LFSRb.insert(0,s)
    LFSRb.pop(-1)

# Fase de generación
for i in range(100):
    X0 = int(format(LFSRb[15], f'0{31}b')[:16] + format(LFSRb[14], f'0{31}b')[15:], 2)
    X1 = int(format(LFSRb[11], f'0{31}b')[15:] + format(LFSRb[9], f'0{31}b')[:16], 2)
    X2 = int(format(LFSRb[7], f'0{31}b')[:16] + format(LFSRb[5], f'0{31}b')[15:], 2)
    X3 = int(format(LFSRb[2], f'0{31}b')[15:] + format(LFSRb[0], f'0{31}b')[:16], 2)

    F1 = (2 * pow(xb,2) - 1) % pow(2,32)
    F2 = (4 * pow(yb,3) - 3 * yb) % pow(2,32)

    xb = F1
    yb = F2

    D, R1b, R2b = F(X0, X1, X2, F1, F2, R1b, R2b)

    s = (pow(2,13)*LFSRb[15] + pow(2,19)*LFSRb[13] + pow(2,17)*LFSRb[10] + pow(2,20)*LFSRb[6] + (1+pow(2,8))*LFSRb[0]) % (pow(2,31)-1)
    if s == 0:
        s = pow(2,31)-1

    LFSRb.insert(0,s)
    LFSRb.pop(-1)

    Z = (D ^ X3)%256
    graphyb.append(Z)
    graphxb.append(i)


# Generamos el gráfico
plt.plot(graphx, graphy, label="Clave A")
plt.plot(graphxb, graphyb, label="Clave B")
plt.xlabel('Número de valores generados')
plt.ylabel('Valores generados')
plt.title('Test de sensibilidad de clave')

plt.xlim(0,100)
plt.ylim(0,256)

plt.legend()
plt.show()
