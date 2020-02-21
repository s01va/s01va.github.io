---
layout: single
title: "CodeEngn Basic 11"
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

OEP를 찾으시오. Ex) 00401000 / Stolenbyte 를 찾으시오. Ex) FF35CA204000E84D000000 
정답인증은 OEP+ Stolenbyte 
Ex ) 00401000FF35CA204000E84D000000

![crakme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/0.png)

![crackme_error]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/1.png)

프로그램을 실행시켜 보니 다음과 같은 창이 뜬다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/2.png)

PEiD로 확인해 보니 UPX로 패킹되어 있어서 이를 언패킹시켜 주었다.

![upx]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/3.png)

![dbg]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/4.png)

패킹을 풀자 이전의 9번 같은 문제가 되었다. OEP를 찾았음을 알 수 있으며(00401000) 실행시키면 다음과 같이 오류가 뜬다.

![error]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/5.png)

이제 언패킹시키기 이전의 정상적인 아래의 창처럼 뜨도록 메모리에 있는 텍스트 정보를 참고하여 어셈블리어를 만들어 보도록 한다.

![crackme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/6.png)

![assem]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-11/7.png)

```assembly

PUSH 0
PUSH 11.00402000
PUSH 11.00402012

```

이를 Big endien임에 주의하여 기계어로 옮긴다.

```assembly

6A 00
68 00204000
68 12204000

```

정답: 004010006A0068002040006812204000

