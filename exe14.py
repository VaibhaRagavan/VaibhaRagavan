#! /usr/bin/python3
n=int(input())
if(n%2==0):
    if(2<=n>=5):
        print("not weird")
    elif(6<=n>20):
        print("weird")
    else:
        print("not weird")
else:
    print("weird")
