---
layout: single
title: "LOB cobolt -> goblin"
#description: ""
date: 2016-02-05 12:00:00 -0400
# modified: 
tags: 
- wargame
- writeup
- pwnable
comments: true
share: true
---

source code:

```c

1  ﻿/*
2          The Lord of the BOF : The Fellowship of the BOF
3          - goblin
4          - small buffer + stdin
5  */
6  
7  int main()
8  {
9      char buffer[16];
10     gets(buffer);
11     printf("%s\n", buffer);
12 }

```

Stack frame structure:

| buffer[16] |
| Stack Frame Pointer[4] |
| Return Address[4] |
| argc |
| argv |
| eviron |

이전과는 다르게 strcpy 함수가 아닌 gets함수를 사용하였다. gets 함수는 프로그램이 실행된 이후에 입력값을 받기 시작하기 때문에 이제까지 썼던 방법으로 인자값 및 쉘코드를 전달할 수 없다.

![goblin]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-03/0.png)

입력값을 이미 넘겨 주었으나 입력값을 받기 위해 대기하고 있는 것을 볼 수 있다. 입력값이 위와 같은 방법으로는 넘어가지 않는 것을 확인하였다. 이번엔 파이프를 사용하여 값을 넘겨보았다.

![pipe]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-03/1.png)

이상 없이 완료된 것을 볼 수 있다. 아래는 gdb로 본 goblin의 어셈블리어이다.

![disas]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-03/2.png)

이전 문제에서 했던 것처럼 argument에 shellcode를 적재하여 공격을 시도하고자 하여, argument를 주었을 시 프로그램 내에 잘 적재가 되는지 확인해 보았다.

![argument addr]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-03/3.png)

(중략)

![argument addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-03/4.png)

argument가 잘 적재된 것을 볼 수 있다. 시작 주소는 0xbffffc08이다. 공격을 아래와 같이 진행하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-03/5.png)

공격이 성공하지 않았다. 원인은 gets함수가 받는 stdin을 파이프로 전달받는 과정에 있다. 위의 (python –c ‘print “\x90” * 20 + “\x10\xfc\xff\xbf”’)를 그대로 stdin으로 넘겨준 후, 문자열 읽기를 끝내기 위해 stdin의 끝에 EOF를 달고 입력받는 것을 끝낼 것이다. 이런 과정이었다면 쉘은 실행되었으나 실행되자마자 종료되었을 것이다. 그래서 페이로드를 아래처럼 다시 작성하였다.

![exploit2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-03/6.png)

공격에 성공하였다. 리눅스 명령어에서 세미콜론은 한줄에 여러 개의 명령어를 주고자 할때 쓰인다. $ [첫번째 명령어];[두번째 명령어] 와 같이 입력했을 때, 첫번째 명령어에서 오류가 생겨도 두번째 명령어는 반드시 실행이 된다. 위의 페이로드는 쉘 실행 후 cat을 바로 실행시켜 종료되는 것을 막고자 하였다.


my-pass: hackers proof