def isPrime(i):
    prime = True
    div = 1
    if(i == 2 or i == 3 or i == 5 or i == 7):
        print(str(i) + " is a prime number")
    elif (i % 2 == 0):
        prime = False
    elif (i % 3 == 0):
        prime = False
    elif (i % 5 == 0):
        prime = False
    elif (i % 7 == 0):
        
        prime = False
    else:
        print(str(i) + " is a prime number")
    return prime

for i in range(1, 101):
    isPrime(i)