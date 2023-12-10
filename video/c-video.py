# importing the necessary libraries
import cv2
import numpy as np
import random

# Función de cifrado
def xor_encrypt(image, key):
    image_np = np.array(image)
    key_np = np.array(key)
    
    key_np = np.resize(key_np, image_np.shape)
    
    result = np.bitwise_xor(image_np, key_np)
    return result

# Función de generación
def F(X0, X1, X2, F1, F2, R1, R2):
    D = ((X0 ^ R1) + R2) % pow(2,32)
    D1 = (R1 + X1) % pow(2,32)
    D2 = R2 ^ X2
    R1 = D1 ^ F1
    R2 = D2 ^ F2
    return([D, R1, R2])

 
# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture('sample.mp4')

# Generación de números para seeds
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

LFSR = []
for i in range(16):
    LFSR.append(random.getrandbits(31))
seeds = []

R1 = random.getrandbits(32)
R2 = random.getrandbits(32)

x = random.getrandbits(32)
y = random.getrandbits(32)

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
    
for i in range(frames):
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

    Z = D ^ X3

    seeds.append(Z)

frameCount = 0
# Loop until the end of the video
while (cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    if frame is None:
        break

    frame = cv2.resize(frame, (540, 380), fx = 0, fy = 0,
                         interpolation = cv2.INTER_CUBIC)
 
    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Key generation
    seed = seeds[frameCount]
    np.random.seed(seed)
    key = np.random.randint(0, 256, size=frame.shape, dtype=np.uint8)

    # Encrypt and decrypt the frames
    en_frame = xor_encrypt(frame, key)
 
    cv2.imshow('Encryption', en_frame)

    de_frame = xor_encrypt(en_frame, key)

    cv2.imshow('Decryption', de_frame)

    frameCount += 1
    # define q as the exit button
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
 
# release the video capture object
cap.release()
# Closes all the windows currently opened.
cv2.destroyAllWindows()
