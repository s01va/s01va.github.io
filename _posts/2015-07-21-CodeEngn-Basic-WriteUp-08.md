---
layout: single
title: "CodeEngn Basic 08"
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

OEP를 구하시오

Ex) 00400000

![Rekenmachine]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-08/0.png)

계산기 프로그램이다.
올리디버거로 열기 이전에, 어떤 파일인지를 파악하기 위해 PEiD로 열어보았다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-08/1.png)

UPX1으로 패킹되어 있는 것을 볼 수 있다. upx 도구를 이용해 언패킹을 한다.

![upx]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-08/2.png)

이제 패킹이 풀린 파일을 올리디버거로 실행시킨다.

![findOEP]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-08/3.png)

패킹이 풀렸음을 확인할 수 있다. OEP는 01012475이다.

정답: 01012475
