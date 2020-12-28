---
layout: single
title: "CodeEngn Basic 18"
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

Name이 CodeEngn일때 Serial은 무엇인가

![crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/0.png)

프로그램은 다음과 같이 Name과 Serial을 넣게 되어 있다.

![PEiD](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/1.png)

아무런 패킹도 되어있지 않다. 이대로 분석을 진행한다.

![string](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/2.png)

모든 string을 참조하는 것으로 시작했다. 이를 바탕으로 시리얼의 판별 부분을 찾았다.

![EAX](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/3.png)

EAX값의 OR연산 결과를 바탕으로 시리얼 값 판별을 진행하는 것을 확인하였다. EAX가 0이 되어야만 정답 판정을 받을 수 있다. 현재 EAX값은 1이므로 OR연산을 했을 때 EAX값은 1이다. EAX값의 결과는 위의 함수 <JMP.&kernel32.lstrcmpiA>에서 발생한다. 해당 함수 이전에 중단점을 걸고 진행시킨 후 함수를 관찰하려고 한다.

![stack](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/4.png)

![reg](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/5.png)

lstrcmpiA 함수에 진입하기 직전의 스택과 레지스터 상태이다.

![function](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/6.png)

함수의 내용은 짧다. [EBP+0C]에는 “06162370056B6AC0”이 들어 있고 [EBP+8]에는 “123”이 들어 있다. [EBP+0C]에 들어있는 값이 시리얼 값으로 추정되어 프로그램을 재실행시켜 확인해 보았다.

![G0od](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-18/7.png)

시리얼 값이 맞음을 확인하였다.

정답: 06162370056B6AC0
