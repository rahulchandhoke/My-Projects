import numpy as np
import sys

ip = open(sys.argv[1],"r")

n = int(sys.argv[2])
m = int(sys.argv[3])
f = int(sys.argv[4])
titer = int(sys.argv[5])

u = [[1.0 for x in range(f)]for y in range(n)]
v = [[1.0 for x in range(m)]for y in range(f)]
size = 0
mat = [[0.0 for x in range(m)]for y in range(n)]
for i in ip:
    size += 1
    strip = i.rstrip()
    line = strip.split(",")
    for j in range(0,len(line)):
        line[j]=int(line[j])
    mat[line[0]-1][line[1]-1] = float(line[2])

for iter in range(0,titer):
    for r in range(0,n):
        for s in range(0,f):
            outersum = 0.0
            for j in range(0,m):
                if mat[r][j] == 0:
                    continue
                innersum = 0.0
                for k in range(0,f):
                    if k!=s:
                        innerprod = u[r][k] * v[k][j]
                        innersum += innerprod
                diff = mat[r][j] - innersum
                outerprod = v[s][j] * diff
                outersum += outerprod
            sqsum = 0.0
            for j in range(0,m):
                if mat[r][j]==0:
                    continue
                sqprod = v[s][j]*v[s][j]
                sqsum += sqprod
            u[r][s] = outersum/sqsum

    unp = np.matrix(u)

    for s in range(0,m):
        for r in range(0,f):
            outersum = 0.0
            for i in range(0,n):
                if mat[i][s] == 0:
                    continue
                innersum = 0.0
                for k in range(0,f):
                    if k!=r:
                        innerprod = u[i][k]*v[k][s]
                        innersum += innerprod
                diff = mat[i][s] - innersum
                outerprod = u[i][r] * diff
                outersum += outerprod
            sqsum = 0.0
            for i in range(0,n):
                if mat[i][s]==0:
                    continue
                sqprod = u[i][r] * u[i][r]
                sqsum += sqprod
            v[r][s] = outersum/sqsum


    vnp = np.matrix(v)
    matmult = np.matmul(unp,vnp)
    matmultlist = matmult.tolist()
    numsum = 0
    for i in range(0,n):
        for j in range(0,m):
            if mat[i][j] == 0:
                continue
            diff = mat[i][j] - matmultlist[i][j]
            sq = diff**(2.0)
            numsum += sq

    div = numsum/size
    rms = div**(1.0/2)

    print "%.4f"%rms