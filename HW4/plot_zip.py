import matplotlib.pyplot as plt

fileName = "TermFrecrency.txt"
handle = open(fileName, "r")
splitter = "\t"

x = []
y = []

for index, line in enumerate(handle):
	if len(line) < 1:
		continue
	line = line.rstrip()
	line = line.split(splitter)

	x.append(index + 1)
	y.append(int(line[1]))

sumOfY = float(sum(y))
for i in range(len(y)):
        y[i] = y[i] / sumOfY

plt.plot(x, y, 'o')
plt.ylabel('probability')
plt.xlabel('rank')
plt.savefig('ZipfianCurve.png')
