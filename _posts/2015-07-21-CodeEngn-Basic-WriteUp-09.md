---
layout: single
title: "CodeEngn Basic 09"
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

StolenByte를 구하시오
Ex) 75156A0068352040

![crackme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/0.png)

![crackme_Error]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/1.png)

키파일을 체크하는 프로그램으로 보인다. 우선, PEiD로 이 프로그램에 대해 파악하도록 한다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/2.png)

UPX1으로 패킹되어 있음을 알 수 있다. upx 툴로 언패킹을 시켜준다.

![upx]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/3.png)

언패킹을 하였더니 이전의 Click OK to check~~ 창 대신 오류 창이 뜬다.

![Error]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/4.png)

![dbg]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/5.png)

올리디버거로 열어보면 프로그램 시작 부분이 이상한 것을 볼 수 있다.

![MessageBoxA]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/6.png)

아랫부분 코드를 참고하면, MessageBoxA의 인자를 4개씩 받는데에 비해, 처음 부분의 MessageBoxA는 hOwner 하나만 받고 있었다는 것을 알 수 있다. 여기가 stolenbyte인 것을 추측할 수 있다.

![crackme1]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/7.png)

처음에 이 창이 뜨도록 아래의 MessageBoxA부분 코드를 흉내내서 코드를 채워주도록 한다.

![hexdump]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-09/8.png)

희망하는 어셈블리어는 다음과 같다.

```assembly

PUSH 0
PUSH 09.004020000
PUSH 09.004020012

```

이제 이것을 기계어로 쓰도록 한다. Big endian임에 주의한다.

```assembly

6A 00
68 00204000
68 12204000

```

정답: 6A0068002040006812204000
