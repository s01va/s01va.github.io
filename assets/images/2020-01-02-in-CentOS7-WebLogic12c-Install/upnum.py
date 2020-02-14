import os, sys


upnum = int(input("Up to number : "))
# upnum == 얼마나 숫자를 올릴 것인가
untilnum = int(input("Until : "))
# untilnum == 가장 숫자가 높은 파일부터 어떤 파일(untilnum)까지 이름을 변경할 것인가
maxnumindir = len(os.listdir("./")) -1
pngs = []

for n in range(0, maxnumindir):
	pngs.append(str(n) + ".PNG")

ext = pngs[0][-4:]

for n in range(maxnumindir, untilnum, -1):
	os.rename(pngs[n-1], str(n - 1 + upnum) + ext)
	print(pngs[n-1] + " -> " + str(n - 1 + upnum) + ext)
