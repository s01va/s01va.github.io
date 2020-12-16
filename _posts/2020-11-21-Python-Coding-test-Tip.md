---
layout: single
title: "Python Coding test Tip"
description: "자주 쓰이는 것들 추가"
date: 2020-11-21 22:00:00 -0400
# modified: 
tags: 
- programing
- algorithm
- cogindtest
comments: true
share: true
---

1. 한 줄에 두 인수 입력받기
	ex) 5 2
	```python
	x, y = input().split()
	```
2. 빠른 입출력
	시간초과를 주의하기 위함이다.
	입출력 방식이 느리면 여러 줄을 입력받거나 출력할 때 시간초과가 날 수 있다.
	Python을 사용하고 있다면, `input` 대신 `sys.stdin.readline`을 사용할 수 있다.
	단, 이때는 맨 끝의 개행문자까지 같이 입력받기 때문에 문자열을 저장하고 싶을 경우 `.rstrip()`을 추가로 해 주는 것이 좋다.

	*from Baekjoon*


	- 응용

		1. 입력값 한번에 두개 받기

		```python
		x, y = sys.stdin.readline().rstrip().split()
		```

		2. 받은 입력값 int로 받기

		```python
		input()
		s = map(int, n.split()) for n in sys.stdin
		```

		3. dd

		```python
		input()
		s = list(sum(map(int, n.split())) for n in sys.stdin)
		```

3. print 이외에

`sys.stdout.write()`




4. Python이 느릴 시

pypy가 있다면 소스코드 그대로 pypy로 채점

