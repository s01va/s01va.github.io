---
layout: single
title: "Python Coding test Tip"
description: "자주 쓰는 것들 추가"
date: 2020-11-21 22:00:00 -0400
modified: 2021-08-03 10:07:00 -0400
tags: 
- programming
- algorithm
- codingtest
- python
- cheatingsheet
comments:
 true
share: true
toc_sticky: true
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

## Dictionary

dictionary는 순서가 없다는 점 유의하기

for문 사용 시, **임의의 순서로 사용**하게 된다. **정렬 관련한 문제에서는 그렇게 좋은 선택지가 아닐수도 있음.**

- 선언

  ```python
  dict1 = {"a":"apple", "b":"bannana", "c":"coconut"}
  ```

- 추가

  list가 append함수를 쓴다면, dictionary는 그냥 씀.

  ```python
  dict1["d"] = "durian"
  # 결과: {'a': 'apple', 'b': 'bannana', 'c': 'coconut', 'd': 'durian'}
  ```

- 요소 삭제

  ```python
  del dict1["a"]
  # 결과: {'b': 'bannana', 'c': 'coconut', 'd': 'durian'}
  ```

### 반복문 관련

list 돌리듯 반복문 돌리면 key값만 반환한다.

```python
# dict1 = {'a': 'apple', 'b': 'bannana', 'c': 'coconut', 'd': 'durian'}

for member in dict1:
	print(member)

# 결과: 
# a
# b
# c
# d
```

아래와 같이 사용하면 value를 반환한다.

```python
for member in dict1:
	print(dict1[member])

# 결과:
# apple
# bannana
# coconut
# durian
```

이렇게 해도 됨

```python
for val in dict1.values():
	print(val)
```

반복문 돌면서 key와 value를 동시에 얻고 싶을 경우 items 함수 사용

```python
for val in dict1.items():
	print(val)
    
# 결과:
# ('a', 'apple')
# ('b', 'bannana')
# ('c', 'coconut')
# ('d', 'durian')
```

key, value를 각기 다른 변수로 취하려면 이렇게

```python
for key, value in dict1.items():
	print(key, value)
    
# 결과:
# a apple
# b bannana
# c coconut
# d durian
```

유의점: dictionary의 in은 key에 한정한다.

```python
print("apple" in dict1)
# 결과: False
print("a" in dict1)
# 결과: True
```

### List로 전환해야 할 경우

```python
dict2list = list(dict1)
# 결과: ['a', 'b', 'c', 'd']
```

위와 같은 경우  key만 반환된다.

value만 list화 시키려면 아래와 같이 한다.

```python
dict2list = list(dict1.values())
# 결과: ['apple', 'bannana', 'coconut', 'durian']
```

python3는 dictionary의 순서대로 반환해준다.



## Heap

**빠른 최대/최소 탐색**을 위해서 씀.

시간제한 등이 걸려있는 알고리즘 문제에서는 최대/최소 관련한 문제가 등장했을 때 빠르게 heapq를 응용할 생각을 해야 한다.

사용법:

```python
import heapq

heaplist = [] # 리스트를 우선 생성

inputex = [25, 4, 9, 72, 11]

for i in inputex:
    heapq.heappush(heaplist, i) # heap 형태로 push

heaplist2 = heaplist.copy()
heaplist3 = heaplist.copy()

while len(heaplist) > 0:
    print(heapq.heappop(heaplist))

# 결과:
# 4
# 9
# 11
# 25
# 72
```

결과를 보면 알겠지만 이 파이썬 heapq는 무조건 최소트리로 만들어진다.

최대탐색이 필요할 때는 트릭이 필요하다.

```python
while len(heaplist2) > 0:
    print(heapq.heappop(heaplist2))

# 결과: 
# (-72, 72)
# (-25, 25)
# (-11, 11)
# (-9, 9)
# (-4, 4)
```

`heappush([해당 리스트], (-i, i))`로 push 후 다음과 같이 pop되는 것을 활용하여 최대 탐색은 다음과 같이 하면 된다.

```python
while len(heaplist3) > 0:
    print(heapq.heappop(heaplist3)[1])

# 결과:
# 72
# 25
# 11
# 9
# 4
```

