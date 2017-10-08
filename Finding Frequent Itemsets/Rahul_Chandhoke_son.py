from pyspark import SparkContext
from operator import add
import sys
import itertools

sc = SparkContext(appName="inf551")

baskets = sc.textFile(sys.argv[1])
supratio = float(sys.argv[2])
count = baskets.count()
sup = count*supratio

def apriori(v,suppratio):
	combn = []
	prev = []
	countt=0
	v=list(v)
	maxl = 0
	for s in v:
		countt+=1
		if len(s) > maxl:
			maxl = len(s)
	supp = countt*suppratio
	c = 2
	sets = []
	for s in v:
		isplit = s.split(",")
		for i in range(0, len(isplit)):
			isplit[i]=int(isplit[i])
		spl = [(x,1) for x in itertools.combinations(isplit,1)]
		for i in range(0,len(spl)):
			spl[i]=list(spl[i])
		tlist=[]
		for i in range(0,len(sets)):
			tlist.append(sets[i][0])
		for i in range(0,len(spl)):
			if spl[i][0] not in tlist:
				sets.append(spl[i])
			else:
				for j in range(0,len(sets)):
					if sets[j][0] == spl[i][0]:
						sets[j][1]+=1
	for i in range(0,len(sets)):
		if sets[i][1]>=supp:
			combn.append(sets[i])
	nxtel = []
	for i in range(0,len(combn)):
		nxtel.append(int(combn[i][0][0]))
	while True:
		csets = [(x,0) for x in itertools.combinations(nxtel,c)]
		for i in range(0,len(csets)):
			csets[i]=list(csets[i])
		ccsets = []
		if c > 2:
			for i in range(0,len(csets)):
				tpele = set()
				for j in range(0,len(csets[i][0])):
					tpele.add(csets[i][0][j])
				tsets = [x for x in itertools.combinations(tpele,c-1)]		
				tcount = 0
				for j in range(0,len(tsets)):
					for k in range(0,len(sets)):
						if set(tsets[j]).issubset(set(sets[k][0])):
							tcount+=1
				if tcount == len(tsets):
					ccsets.append(csets[i])
			csets = ccsets
		for s in v:
			isplit = s.split(",")
			for i in range(0,len(isplit)):
				isplit[i]=int(isplit[i])
			for i in range(0,len(csets)):
				if set(csets[i][0]).issubset(set(isplit)):
					csets[i][1]+=1
		sets = []
		for i in range(0,len(csets)):
			if csets[i][1]>=supp:
				sets.append(csets[i])
		if not sets:
			break
		ele = set()
		for i in range(0,len(sets)):
			combn.append(sets[i])
			for j in range(0,len(sets[i][0])):
				ele.add(sets[i][0][j])
		nxtel = list(ele)
		c+=1
	return combn	

def phase2(v,p2):
	p3 = []
	for i in range(0,len(p2)):
		p2[i] = list(p2[i])
		p2[i][0] = tuple(p2[i][0])
	for s in v:
		isplit = s.split(",")
		for i in range(0, len(isplit)):
			isplit[i]=int(isplit[i])
		for i in range(0,len(p2)):
			if set(p2[i][0]).issubset(set(isplit)):
				p3.append((p2[i][0],1))
	return p3

p1 = baskets.mapPartitions(lambda j: apriori(j,supratio))
p2 = p1.reduceByKey(lambda x,y: 1)
bp = p2.collect()
p3 = baskets.mapPartitions(lambda j: phase2(j,bp))
p3 = p3.reduceByKey(add).filter(lambda x:x[1]>=sup)
p4 = p3.keys()
op = p4.collect()

opfile = open(sys.argv[3],"w")
for v in op:
	l = []
	for i in range(0,len(v)):
		l.append(v[i])
	line = str(l)
	line = line[1:]
	line = line[:-1]
	line = line.replace(" ","")
	opfile.write("%s" % line)
	opfile.write("\n")