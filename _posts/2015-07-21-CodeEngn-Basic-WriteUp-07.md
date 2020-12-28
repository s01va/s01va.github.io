---
layout: single
title: "CodeEngn Basic 07"
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

컴퓨터 C 드라이브의 이름이 CodeEngn 일경우 시리얼이 생성될때 CodeEngn은 "어떤것"으로 변경되는가

![crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/0.png)

시리얼 키를 인증하는 프로그램으로 보인다.

![JE](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/1.png)

어떤 함수를 리턴한 EAX값과 비교하여 시리얼 넘버를 판별하는 듯한 조건문이 보인다. 프로그램을 실행시켜 경과를 보도록 한다.

![input](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/2.png)

눈에 보이는 문자열을 넣었다.

![serial num](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/3.png)

시리얼 넘버는 ConcatString, String1임을 추측할 수 있다.

![serial](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/4.png)

코드엔진에서 원하는 답을 찾기 위해 C드라이브의 이름을 바꾸었다.

![JE](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/5.png)

비어있던 ConcatString에 CodeEngn이라는 문자열이 들어옴을 확인하였다.

![StringToAdd](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/6.png)

계속 실행시켜 보면, CodeEngn이 ADD연산자로 인해 변하는 것을 볼 수 있다.

![ConcatString](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/7.png)

CodeEngn이 EqfgEngn으로 바뀐 것을 볼 수 있다.

C드라이브의 이름이 바뀐 후의 시리얼 넘버는 위에서 보았던 것처럼 4023FD의 StringToAdd와 40225C의 StringToAdd가 합쳐진 값이 됨을 알 수 있다. 즉 C드라이브의 이름이 CodeEngn으로 바뀐 후의 시리얼 넘버는 L2C-5781EqfgEngn4562-ABEX일 것이다.

![answer](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-07/8.png)


정답: EqfgEngn