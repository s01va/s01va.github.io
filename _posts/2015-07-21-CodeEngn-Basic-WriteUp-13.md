---
layout: single
title: "CodeEngn Basic 13"
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

정답은 무엇인가

다음은 실행시킨 최초의 화면이다. 패스워드를 알아내는 프로그램임을 알 수 있다.

![program]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/0.png)

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/1.png)

PEiD로 조사해 보니 C# 닷넷 프레임워크로 짠 프로그램임을 알 수 있다. C#은 Managed code로, 이 C# 컴파일러는 바로 기계어로 컴파일을 하는 것이 아니라 다른 중간 언어로 컴파일을 해 낸다. 특정 플러그인을 설치하지 않은 올리디버거로는 분석이 불가능하므로, 닷넷용 무료 분석툴인 dotPeek을 사용하였다.

![dotpeek]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/2.png)

소스코드 수준으로 분석해낸 것을 볼 수 있다.

![source]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/3.png)

str이 정답임을 알 수 있다. str를 출력하기 위해 코드를 그대로 복사해서 컴파일하였다.

![Rijindael]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/4.png)

Rijindael.exe를 생성하여 실행시켰다.

![answer]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/5.png)

정답: Leteminman
