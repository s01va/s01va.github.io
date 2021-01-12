---
layout: single
title: "BOJ 8단계 기본수학1 풀이"
description: "기본수학1 풀이"
date: 2021-01-10 13:37:00 -0400
# modified: 
tags:
- codingtest
- algorithm
- programming
comments: true
share: true
---

[BOJ 단계별로 풀어보기: 기본 수학 1](https://www.acmicpc.net/step/8)

수학적으로 접근하여 반복문을 최소화 시키는 것을 의도한 것으로 보인다.

## 단계1 손익분기점

![1번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/0.jpg)

```python
A, B, C = map(int, input().rstrip().split())
if (B >= C):
	print(-1)
else:
	N = (A // (C - B)) + 1
	print(N)
```



## 단계2 벌집

![2번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/1.jpg)

```python
N = int(input())
n = 1
while(True):
	if (3*n*(n-1) + 1) >= N:
		break
	else:
		n+=1
print(n)
```



## 단계3 분수찾기

![3번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/2.jpg)

```python
X = int(input())
N = 1
M = 1
while True:
	if M >= X:
		break
	N += 1
	M = M + N
if N % 2 == 1:
	print(str(M-X+1) + "/" + str(N-M+X))
else:
	print(str(N-M+X) + "/" + str(M-X+1))
```



## 단계4 달팽이는 올라가고 싶다

![4번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/3.jpg)

```python
A, B, V = map(int, input().rstrip().split())
tmp = (V-B)%(A-B)
if tmp != 0:
	print(((V-B)//(A-B)) + 1)
else:
	print((V-B)//(A-B))
```



## 단계5 ACM 호텔

![5번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/4.jpg)

```python
import sys
T = int(input())
for i in range(T):
	H, W, N = map(int, sys.stdin.readline().rstrip().split())
	Y = N % H
	if Y == 0:
		Y = str(H)
	else:
		Y = str(Y)
	X = N // H
	if X != N / H:
		X += 1
	if X < 10:
		X = "0"+str(X)
	else:
		X = str(X)
	print(Y + X)
```



## 단계6 부녀회장이 될테야

![6번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/5.jpg)

수학적으로 해결하기보다 배열을 사용하여 해결하였다.

```python
T = int(input())
for i in range(T):
	k = int(input())
	n = int(input())
	l = [i for i in range (1, n+1)]
	for i in range(k):
		for j in range(1, n):
			l[j] = l[j-1] + l[j]
	print(l[-1])
```

