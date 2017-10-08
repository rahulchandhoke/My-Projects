from pyspark import SparkContext
import sys

sc = SparkContext(appName="inf551")

ip = sc.textFile(sys.argv[1])
tusers = ip.count()

def umovies(s):
	isplit = s.split(",")
	for i in range(1, len(isplit)):
			isplit[i]=int(isplit[i])
	return isplit[1:]

def mhash(s):
	isplit = s.split(",")
	for i in range(1, len(isplit)):
			isplit[i]=int(isplit[i])
	column = []
	for i in range(0,20):
		min = 101
		for j in range(1,len(isplit)):
			val = ((3*isplit[j])+(13*i))%100
			if val < min:
				min = val
		column.append(min)
	return str(isplit[0])[1:],tuple(column)

def band(x,f,l):
	return x[1][f:l],x[0]
	
def genpairs(x):
	itlist = []
	y = []
	for i in x:
		itlist.append(i)
	for i in itlist:
		for j in itlist:
			if i!=j:
				y.append((i,j))
	for i in range(0,len(y)):
		y[i] = tuple(y[i])
	return y

def jaccard(s,v):
	s = list(s)
	v = list(v)
	j = int(s[0])
	sim = list(s[1])
	tosort = []
	for i in sim:
		i = int(i)
		num = len(set(v[i-1]).intersection(v[j-1]))
		den = len(v[i-1])+len(v[j-1])-num
		jac = float(num)/float(den)
		tosort.append([i,jac])
	tosort = sorted(tosort, key = lambda x: x[0])
	sortedlis = sorted(tosort, key = lambda x: x[1], reverse = True)
	fsortedlis  = []
	for i in sortedlis:
		fsortedlis.append(i[0])
	return s[0],fsortedlis
			
def choose5(s):
	s = list(s)
	s[1] = list(s[1])
	if len(s[1])>5:
		s[1] = s[1][:5]
		s[1] = sorted(s[1])
		return s[0],s[1]
	else:
		s[1] = sorted(s[1])
		return s[0],s[1]


movies = ip.map(umovies).collect()	
signature = ip.map(mhash)
band1 = signature.map(lambda x: band(x,0,4)).groupByKey().values()
cp1 = band1.map(lambda x: tuple(x)).filter(lambda x:len(x)>1).map(genpairs).flatMap(lambda x:x)
band2 = signature.map(lambda x: band(x,4,8)).groupByKey().values()
cp2 = band2.map(lambda x: tuple(x)).filter(lambda x:len(x)>1).map(genpairs).flatMap(lambda x:x)
band3 = signature.map(lambda x: band(x,8,12)).groupByKey().values()
cp3 = band3.map(lambda x: tuple(x)).filter(lambda x:len(x)>1).map(genpairs).flatMap(lambda x:x)
band4 = signature.map(lambda x: band(x,12,16)).groupByKey().values()
cp4 = band4.map(lambda x: tuple(x)).filter(lambda x:len(x)>1).map(genpairs).flatMap(lambda x:x)
band5 = signature.map(lambda x: band(x,16,20)).groupByKey().values()
cp5 = band5.map(lambda x: tuple(x)).filter(lambda x:len(x)>1).map(genpairs).flatMap(lambda x:x)

cp = cp1.union(cp2).union(cp3).union(cp4).union(cp5).distinct().groupByKey()
similar = cp.map(lambda x: jaccard(x,movies))
final = similar.map(choose5).collect()
final = sorted(final, key = lambda x:int(x[0]))

opfile = open(sys.argv[2],"w")
for i in final:
	opstr = "U"+i[0]+":U"
	slen = len(i[1])
	for j in range(0,slen):
		if j == slen-1:
			opstr += str(i[1][j])
		else:
			opstr = opstr + str(i[1][j]) + ",U"
	opfile.write("%s" % opstr)
	opfile.write("\n")
	
	
	
	
	
	