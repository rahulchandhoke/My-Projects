#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
The K-means algorithm written from scratch against PySpark. In practice,
one may prefer to use the KMeans algorithm in ML, as shown in
examples/src/main/python/ml/kmeans_example.py.

This example requires NumPy (http://www.numpy.org/).
"""
from __future__ import print_function

import sys

import numpy as np
from pyspark.sql import SparkSession
from pyspark import SparkContext
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import norm
import math

def intconv(x):
    for i in range(0,len(x)):
        x[i] = int(x[i])
    return x

def cosine(x,y):
    num = x.dot(y.transpose())[0,0]
    den = norm(x) * norm(y)
    cos = num / den
    return 1.0 - cos

def parseVector(line):
    return np.array([float(x) for x in line.split(' ')])


def closestPoint(p, centers):
    bestIndex = 0
    closest = float("+inf")
    for i in range(len(centers)):
        tempDist = cosine(p,centers[i])
        if tempDist < closest:
            closest = tempDist
            bestIndex = i
    return bestIndex


if __name__ == "__main__":

    print("""WARN: This is a naive implementation of KMeans Clustering and is given
       as an example! Please refer to examples/src/main/python/ml/kmeans_example.py for an
       example on how to use ML's KMeans implementation.""", file=sys.stderr)

    sc = SparkContext(appName="inf551")
    lines = sc.textFile(sys.argv[1])
    ip = lines.map(lambda x: x.split(" "))
    ip = ip.map(lambda x: intconv(x))
    docs = ip.collect()[0][0]
    vocab = ip.collect()[1][0]
    words = ip.collect()[2][0]

    dataset = ip.filter(lambda x: len(x) > 1)
    dataset = dataset.map(lambda x: intconv(x)).collect()

    content = {}
    unitvector = csc_matrix((docs, vocab + 1))
    for i in dataset:
        ele = {i[0] - 1: i[2]}
        if i[1] in content:
            content[i[1]].update(ele)
        else:
            content.update({i[1]: ele})
    sos = [0.0] * docs
    for i in content:
        for j in content[i]:
            tf = content[i][j]
            idf = math.log(float(docs + 1) / (len(content[i]) + 1), 2)
            unitvector[j, i] = tf * idf
            sos[j] += math.pow(unitvector[j, i], 2)
    for i in range(0, docs):
        unitvector[i, :] /= math.sqrt(sos[i])
    convdata = [(i,unitvector[i, :]) for i in range(0,docs)]

    rdddata = sc.parallelize(convdata)
    sorteddata = rdddata.sortByKey()
    data = sorteddata.map(lambda (x,y):y)

    K = int(sys.argv[2])
    convergeDist = float(sys.argv[3])

    kPoints = data.repartition(1).takeSample(False, K, 1)
    tempDist = 1.0

    while tempDist > convergeDist:
        closest = data.map(
            lambda p: (closestPoint(p, kPoints), (p, 1)))
        pointStats = closest.reduceByKey(
            lambda p1_c1, p2_c2: (p1_c1[0] + p2_c2[0], p1_c1[1] + p2_c2[1]))
        newPoints = pointStats.map(
            lambda st: (st[0], st[1][0] / st[1][1])).collect()

        tempDist = sum(csc_matrix.sum((kPoints[iK] - p).power(2)) for (iK, p) in newPoints)

        for (iK, p) in newPoints:
            kPoints[iK] = p

    count = [0] * len(kPoints)
    for i in range(0,len(kPoints)):
        count[i] = len(kPoints[i].nonzero()[0])

    opfile = open(sys.argv[4], "w")
    for i in count:
        opstr = str(i)
        opfile.write("%s" % opstr)
        opfile.write("\n")

    sc.stop()
