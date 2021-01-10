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

![2번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/2.jpg)

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

![4번문제 풀이](https://s01va.github.io/assets/images/2021-01-10-BOJ-Step08-BasicMath1/2.jpg)

```python
A, B, V = map(int, input().rstrip().split())
tmp = (V-B)%(A-B)
if tmp != 0:
	print(((V-B)//(A-B)) + 1)
else:
	print((V-B)//(A-B))
```

