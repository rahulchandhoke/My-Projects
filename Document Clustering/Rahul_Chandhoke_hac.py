from scipy.sparse import csc_matrix
from scipy.sparse.linalg import norm
import scipy.sparse as sp
from copy import deepcopy
import heapq
import sys
import math
import itertools

def cosine(x,y):
    num = x.dot(y.transpose())[0,0]
    den = norm(x) * norm(y)
    cos = num / den
    return 1.0 - cos

#ip = open(sys.argv[1],"r")
ip = open("E:\demp_500.txt","r")
lines = ip.readlines()

for i in range(0,len(lines)):
    lines[i] = lines[i].strip().split(" ")
    for j in range(0,len(lines[i])):
        lines[i][j] = int(lines[i][j])

docs = lines[0][0]
vocab = lines[1][0]
words = lines[2][0]
lines = lines[3:]
content = {}
unitvector = csc_matrix((docs,vocab+1))
for i in lines:
    ele = {i[0]-1: i[2]}
    if i[1] in content:
        content[i[1]].update(ele)
    else:
        content.update({i[1]:ele})

sos = [0] * docs
for i in content:
    for j in content[i]:
        tf = content[i][j]
        idf = math.log(float(docs+1)/(len(content[i])+1),2)
        unitvector[j,i] = tf * idf
        sos[j] += math.pow(unitvector[j,i],2)
for i in range(0,docs):
    unitvector[i,:] /= math.sqrt(sos[i])

unitcopy = deepcopy(unitvector)
docset = [i for i in range(0,docs)]
clusters = {i:[i] for i in docset}
refclusters = deepcopy(clusters)
h = []
#k = int(sys.argv[2])
k = 5
newcluster = docs
shapeval =  (0, unitvector[0].shape[1])
combns = itertools.combinations(docset, 2)
tempcluster = csc_matrix((shapeval))
for i in combns:
    heapq.heappush(h, (cosine(unitcopy[i[0],:], unitcopy[i[1],:]), [i[0], i[1]]))
while len(docset) > k:
    closest = heapq.heappop(h)[1]
    notpres = 0
    for i in closest:
        if i not in docset:
            notpres = 1
    if notpres == 1:
        continue
    newunit = csc_matrix((shapeval))
    vector = deepcopy(closest)
    while any(x >= docs for x in vector):
        for j in vector:
            if j >= docs:
                vector.remove(j)
                for v in refclusters[j]:
                    vector.append(v)
    for i in vector:
        newunit = sp.vstack((newunit,unitcopy[i,:]),format="csc")
    newunit = sp.csc_matrix.mean(newunit,axis=0)
    unitcopy = sp.vstack((unitcopy,newunit),format="csc")
    for i in closest:
        docset.remove(i)
        clusters.pop(i)
    for i in docset:
        pair = (newcluster,i)
        heapq.heappush(h, (cosine(unitcopy[pair[0],:], unitcopy[pair[1],:]), [pair[0], pair[1]]))
    docset.append(newcluster)
    clusters.update({newcluster:closest})
    refclusters.update({newcluster:closest})
    newcluster += 1

final = []
count = 0
for i in clusters:
    final.append(clusters[i])
    while any(x >= docs for x in final[count]):
        for j in final[count]:
            if j >= docs:
                final[count].remove(j)
                for k in refclusters[j]:
                    final[count].append(k)
    count += 1
for i in range(0,len(final)):
    for j in range(0,len(final[i])):
        final[i][j] += 1
    final[i] = str(final[i])

for i in final:
    print i[1:-1]