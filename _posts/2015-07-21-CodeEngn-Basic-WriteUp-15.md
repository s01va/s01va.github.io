---
layout: single
title: "CodeEngn Basic 15"
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


Name이 CodeEngn일때 Serial을 구하시오

![crackme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/0.png)

다음과 같이 Name과 Serial을 입력하여 인증하는 프로그램이다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/1.png)

PEiD로 확인해 보니 별다른 패킹은 되어있지 않고 Delphi로 작성된 프로그램임을 확인할 수 있다.

![Delphi]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/2.png)

string만 따로 찾아 정답 판별 여부를 나타내는 곳의 주소지를 찾았다.

![JNE]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/3.png)

458831에서 EAX와 45B844의 값과 같은지를 확인하여 정답 여부를 판별하는 것을 볼 수 있다. 프로그램을 실행하기 전이라 45B844는 비워져 있다.

![JNE]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/4.png)

적당한 위치에 BP를 걸고 Name에 CodeEngn, Serial에 임의의 값 12345를 넣어 실행시켰다. 함수 458760을 통과하자 CMP 분기문에서 EAX와 비교되는 45B844에 ASCII 값이 추가되는 것을 볼 수 있다.

![function 458760]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/5.png)

458460 함수에 진입한 모습이다. 대강 Name인 CodeEngn 문자열만 가지고 시리얼 값을 생성하는 것을 알 수 있다. 

![any serial]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/6.png)

시리얼을 무엇을 입력하든 Name이 변하지 않는 한 CMP에서 EAX와 비교하는 45B844의 값은 변하지 않는 것을 알 수 있다.

![6061]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/7.png)

45B844에는 6061이 들어있다(ASCII로는 \`a인 듯 하다). 이를 little endian으로 해석한 6160을 십진수로 바꾸면 24928이다. 이것이 키 값임을 알 수 있다.

![answer]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-15/8.png)


정답: 24673