---
layout: single
title: "Webhacking.kr 3번"
description: "리뉴얼 기념 정주행"
date: 2019-12-26 12:37:00 -0400
# modified: 
tags:
- webhacking
- webhacking.kr
- wargame
- writeup
- cookie
- sql-injection
comments: true
share: true
---

![03](https://s01va.github.io/assets/images/2019-12-26-WriteUp-Webhacking.kr-03/0.PNG)

네모로직 게임처럼 생긴 문제이다. 칸을 채워 제출해 보았다.

![03](https://s01va.github.io/assets/images/2019-12-26-WriteUp-Webhacking.kr-03/1.PNG)

![clear](https://s01va.github.io/assets/images/2019-12-26-WriteUp-Webhacking.kr-03/2.PNG)


```url
https://webhacking.kr/challenge/web-03/index.php?_1=1&_2=0&_3=1&_4=0&_5=1&_6=0&_7=0&_8=0&_9=0&_10=0&_11=0&_12=1&_13=1&_14=1&_15=0&_16=0&_17=1&_18=0&_19=1&_20=0&_21=1&_22=1&_23=1&_24=1&_25=1&_answer=1010100000011100101011111
```

s01va라고 제출했더니 아래와 같은 화면이 뜬다.

![log](https://s01va.github.io/assets/images/2019-12-26-WriteUp-Webhacking.kr-03/3.PNG)

이 세션을 웹 디버거로 캡쳐해서 분석했다.

![fiddler](https://s01va.github.io/assets/images/2019-12-26-WriteUp-Webhacking.kr-03/4.PNG)

answer값과 id값을 &로 묶어서 보내고 있는 것을 볼 수 있다. 양쪽 값을 모두 참으로 만들어 보았다.

![webdebugger1](https://s01va.github.io/assets/images/2019-12-26-WriteUp-Webhacking.kr-03/5.PNG)

빈 name에는 admin을 집어넣었다(아무 값이나 상관없음)

![result](https://s01va.github.io/assets/images/2019-12-26-WriteUp-Webhacking.kr-03/6.PNG)

3번을 풀었다. 일반적인 SQL injection 문제.