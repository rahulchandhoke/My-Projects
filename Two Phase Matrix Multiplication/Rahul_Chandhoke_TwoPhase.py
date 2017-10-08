from pyspark import SparkContext
from operator import add

sc = SparkContext(appName="inf551")

mata = sc.textFile("mat-A/values.txt")
matb = sc.textFile("mat-B/values.txt")

def mapa1(s):
	m1splt=s.split(",")
	return (m1splt[1],["A",m1splt[0],m1splt[2]])

def mapb1(s):
	m1splt=s.split(",")
	return (m1splt[0],["B",m1splt[1],m1splt[2]])

def mult(s):
	la=[]
	lb=[]
	fl=[]
	for v in s:
		if v[0] == "A":
			la.append(v)
		elif v[0] == "B":
			lb.append(v)
	for v in la:
		for v1 in lb:
			prd=int(v[2])*int(v1[2])
			fl.append(((v[1],v1[1]),prd))
	return fl
						
maop = mata.map(mapa1)
mbop = matb.map(mapb1)
mcop = maop.union(mbop)
mcop = mcop.groupByKey()
mcop = mcop.flatMapValues(mult)
mdop = mcop.values()
fop = mdop.reduceByKey(add)
fmat = fop.collect()

op = open("output.txt","w")
for v in fmat:
	line = "%s,%s\t%s" % (v[0][0],v[0][1],v[1])
	op.write(line)
	op.write("\n")

	