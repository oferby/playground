# https://www.youtube.com/watch?v=oBt53YbR9Kk

# 1,1,2,3,5,...

def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


indx = int(input('enter number index:'))
print(fib(indx))
