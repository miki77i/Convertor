n = 100 - 14 * 32 // 3
x = 3
for i in range(5,n):
    for j in range(5,n):
        x = x + 5
        print(x, "Hello")
        

print(x)

name = input()

if n % 5 == 0: 
    if x == 3:
        print(1)
    else:
        print(4)
