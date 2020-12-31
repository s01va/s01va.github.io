---
layout: single
title: "Python Coding test Tip"
description: "자주 쓰는 것들 추가"
date: 2020-11-21 22:00:00 -0400
modified: 2020-12-28 10:45:00 -0400
tags: 
- programming
- algorithm
- codingtest
- python
comments: true
share: true
---





맨날 까먹는 나를 위해서

유사시 여기서 검색하기



## 한 줄에 두 인수 입력받기

ex) 5 2
```python
x, y = input().split()
```



## 빠른 입출력

시간초과를 주의하기 위함이다.

입출력 방식이 느리면 여러 줄을 입력받거나 출력할 때 시간초과가 날 수 있다.

Python을 사용하고 있다면, `input` 대신 `sys.stdin.readline`을 사용할 수 있다.

단, 이때는 맨 끝의 개행문자까지 같이 입력받기 때문에 문자열을 저장하고 싶을 경우 `.rstrip()`을 추가로 해 주는 것이 좋다.

*from Baekjoon*

### 응용
1. 입력값 한번에 두개 받기

   ```python
   x, y = sys.stdin.readline().rstrip().split()
   ```

2. 받은 입력값 int로 받기

   ```python
   input()
   s = map(int, n.split() for n in sys.stdin)
   ```

3. 한번에 총합 계산

   ```python
   input()
   s = list(sum(map(int, n.split())) for n in sys.stdin)
   ```

## Python이 느릴 시

pypy가 있다면 소스코드 그대로 pypy로 채점



## print 이외에

```python
sys.stdout.write()
```



## 배열 초기화

```python
testlist1 = [0 for i in range(10)]
# 결과: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

```python
testlist2 = [i for i in range(10)]
# 결과: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```



## list 중 중복 없애기

```python
testlist3 = [0, 0, 0, 1, 1, 2, 2, 3]
resultlist = set(testlist3)
# 결과: [0, 1, 2, 3]
```



## `import` 없이 쓰는 간단한 수학 함수 활용

- 총합

  ```python
  sum(testlist2)
  # 결과: 45
  ```

- 최대

  ```python
  max(testlist2)
  # 결과: 9
  ```

- 최소

  ```python
  min(testlist2)
  # 결과: 0
  ```

- 평균

  ```python
  sum(testlist2)/len(testlist2)
  # 결과: 4.5
  ```

  평균은 `import` 없이 쓸 수 있는 함수가 따로 없음
  
- 소수점 출력

  ```python
  pi = 3.1415926535
  print("%0.2f%%" % pi)
  print("%0.4f%%" % pi)
  ```




## 증감연산자

맨날헷갈림...

다른 언어에서 `++`, `--` 형태로 사용하던 버릇대로 쓰려니 **파이썬에서 당연히 안먹힘**

python에선 `var += 1`과 같은 형태로 쓸 것



## `print` formatting 방식

```python
# 테스트용 str 추가
exstr = "helloworld"
```

- 기존 방식

  ```python
  print("exstr = %s / testlist2[9] = %d / pi = %f" % (exstr, testlist2[9], pi))
  # 결과: exstr = helloworld / testlist2[9] = 9 / pi = 3.141593
  ```

- `.format` 방식

  이는 string을 선언할 때에도 유용하다.

  ```python
  print("exstr = {0} / testlist2[9] = {1} / pi = {2}".format(exstr, testlist2[8], pi))
  ```

  변수 사용도 가능

  ```python
  print("exstr = {exstr} / testlist2[8] = {tl} / pi = {pi2}".format(exstr=exstr, tl=testlist2[8], pi2=pi))
  ```

  같은 문자열이 여러번 들어가는데, 이 문자열이 변동 여지가 있을 때 쓰기 좋음

  

## 문자열 거꾸로 출력하기

```python
reversed_exstr = exstr[::-1]
```



## 어떤 정수의 각 자릿수 구하기

```python
num = 98765	# 정수 아무거나
elements = [int(ch) for ch in str(num)]
# 결과: [9, 8, 7, 6, 5]
```

가장 간단하지만 이는 아주 Pythonic한 방법

또 다른 방법은 [여기](https://shoark7.github.io/programming/algorithm/3-ways-to-get-length-of-natural-number) 참고



