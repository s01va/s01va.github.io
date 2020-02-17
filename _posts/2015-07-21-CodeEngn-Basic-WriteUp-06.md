---
layout: single
title: "CodeEngn Basic 06"
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

Unpack을 한 후 Serial을 찾으시오. 정답인증은 OEP + Serial
Ex) 00400000PASSWORD

![crackme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-06/0.png)

시리얼 키를 입력하는 창과 확인버튼이 있는 프로그램이다.

![pushad]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-06/1.png)

올리디버거로 열어보니, 5번문제와 같이 PUSHAD로 시작하는 것을 볼 수 있다. PEiD 툴로 이 프로그램에 대해 조사한다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-06/2.png)

UPX1으로 패킹되어 있다고 뜬다. 언패킹을 해주도록 한다.

![upx]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-06/3.png)

![unpacking]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-06/4.png)

언패킹에 성공하고, 제대로 된 entry point로 시작함을 볼 수 있다.
OEP는 401360이다.
이제 시리얼 키를 찾기 위해 문자열을 모아 보았다.

![strings]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-06/5.png)


시리얼 키를 볼 수 있다.

정답: 00401360AD46FS547
