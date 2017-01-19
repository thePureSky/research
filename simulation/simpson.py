#coding = utf-8
from math import *
from scipy.stats import norm
def func(x): 
	g = norm.cdf((x - 55) / 4.5)
	print x
	if x == 0:
		return 0
	return (pow(10, 6) / x) * g * pow(1 - g, 9)

def Get_N(a,b,width):
    N=int((b-a)/width + 1)
    if N%2 == 0:
        N=N+1
    return N

def GenerateData(a,b,n,width):
    datas = []
    r=a
    for i in range(0,n):
        datas.append(func(r))
        r = r+width
    return datas

def simpson_integral(datas,width,n):
    sum = datas[0]+datas[n-1]
    for i in range(2,n):
        if i%2== 0:
            sum = sum +4*datas[i-1]
        else:
            sum = sum +2*datas[i-1]
    return sum*width/3.0

if __name__ == "__main__":
    a=0.00
    b=100
    width=0.000625
    N=Get_N(a,b,width)
    datas = GenerateData(a,b,N,width)
    print simpson_integral(datas,width,N)
