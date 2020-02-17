---
layout: single
title: "CodeEngn Basic 05"
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

이 프로그램의 등록키는 무엇인가

프로그램을 실행시키면 다음과 같은 창이 뜬다. 등록키로 인증받는 프로그램으로 보인다.

![crackmev3.0]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-05/0.png)

PEiD라는 프로그램을 통해 이 프로그램에 대한 정보를 구해보도록 한다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-05/1.png)

EP Section에 UPX1이라는 것이 있다(다른 프로그램은 .text였음). 이는 어떤 패킹 방식인데, PE 파일 압축기이며, 파일 크기를 줄이며 내부 코드와 리소스를 감추기 위한 목적으로 사용된다. 파일 내부에 압축 해제 코드를 포함하고 있기 때문에 실행되는 순간 압축 해제가 일어난다.

UPX패킹은 코드 맨 마지막에 OEP(Original entry point)로 가는 JMP문이 있다. 진짜 코드를 따로 저장할 수 있으나 편리한 툴을 이용해 UPX 언패킹을 하도록 한다.
다음은 이 프로그램을 올리디버거로 열었을 때의 처음 화면이다.

![pushad]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-05/2.png)

UPX라는 CLI 도구를 사용한다.

![runupx]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-05/3.png)

언패킹 이후 올리디버거로 다시 열어보면, 익숙한 시작 코드가 뜨는 것을 볼 수 있다.

![find string]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-05/4.png)

시리얼 키를 빨리 찾기 위해, 문자열을 골라서 보았다(Search for – All referenced text strings).

![search referenced text strings]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-05/5.png)


시리얼 키를 볼 수 있다.


정답: GFX-754-IER-954
