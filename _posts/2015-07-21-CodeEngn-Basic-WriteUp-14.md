---
layout: single
title: "CodeEngn Basic 14"
#description: ""
date: 2015-07-21 12:00:00 -0400
# modified: 
tags: 
- wargame
- writeup
- reversing
- codeengn-basic
comments: true
share: true
---

Name이 CodeEngn 일때 Serial을 구하시오. (이 문제는 정답이 여러개 나올 수 있는 문제이며 5개의 숫자로 되어있는 정답을 찾아야함, bruteforce 필요) 
Ex) 11111

![crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/0.png)

실행 화면이다. 시리얼 키를 입력하는 프로그램이다.

![PEiD](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/1.png)

PEiD로 분석해 보니 UPX패킹이 되어 있는 것을 볼 수 있다. 패킹을 풀어준다.

![UPX](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/2.png)

패킹을 풀고 올리디버거로 해당 프로그램을 열고, CodeEngn과 임의의 숫자 12345를 넣고 실행시켜 보았다.

![input crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/3.png)

![result crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/4.png)

잘못된 시리얼이라는 창을 띄우고 종료된다. 올리디버거로 해당 프로그램을 띄워 CodeEngn, 12345를 입력하고 분석한다. 그러던 중 정답을 판정하는 것으로 보이는 분기문을 발견하였다.

![JNE](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/5.png)

EAX와 ESI가 같을 시 정답으로 판정하는 것을 볼 수 있다. 그리고 그 바로 위에서 함수 401383의 return으로 EAX값이 결정되는 것을 볼 수 있다.

![return](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/6.png)

그 위에는 ESI값이 결정되는 듯한 알고리즘이 보인다.

![func](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/7.png)

CodeEndn, 12345를 입력하고 진행시킨 결과이다.

![calc result](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-14/8.png)

Name에 CodeEngn을 넣었을 시 그 연산 결과가 ESI에, 시리얼 값 12345에 대한 연산 결과는 함수 401383에 의해 연산 결과가 EAX에 담기는 것을 알 수 있다.

![ESI](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-12/9.png)

CodeEngn 문자열로 ESI 연산 알고리즘이 완료된 후의 레지스터 상태이다. ESI가 129A1임을 볼 수 있다. 129A1은 10진수로 76193이다.

![cracked](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-12/10.png)

이 값이 실제 시리얼 값임을 확인하였다.
좀더 알고리즘을 파헤쳐서 해결하고자 한다면 다음과 같은 방법으로 풀 수도 있다. 다음은 입력한 시리얼 값으로 EAX를 생성해내는 함수 401383이다.

![function](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-12/11.png)

| (첫번째 문자열의 아스키 코드 – 30)*A^4 + (두번째 문자열의 아스키 코드 – 30)*A^3 + (세번째 문자열의 아스키 코드 – 30) * A^2 + … |

이의 결과가 129A1과 같아야 한다. 이 연산결과에 맞는 값을 무작위 대입으로 알아내는 방법도 존재한다.

정답: 76193
