---
layout: single
title: "CodeEngn Basic 16"
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

![crakme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-16/0.png)

Name과 Serial을 CLI로 입력하는 프로그램이다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-16/1.png)

PEiD로 보면 패킹은 되어있지 않음을 알 수 있다. 그대로 분석을 진행한다.

![0040159F]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-16/2.png)

![0040163C]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-16/3.png)

정답을 판별하는 부분이다. EAX와 LOCAL.15의 값을 비교하여 그 둘이 같을 시 정답으로 판별하는 것을 볼 수 있다. LOCAL.15는 지역변수 값으로 스택에서 확인할 수 있으므로 실행시켜가면서 그곳에 어떤 값이 확인하고자 한다. 다음은 CodeEngn과 12345를 입력했을 시 LOCAL.15에 들어가 있는 값이다.

![3838184855]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-16/4.png)

E4C60D97은 십진수로 3838184855이다. 그래서 프로그램을 재실행 시킨 후 CodeEngn과 3838184855를 입력해 보았다.

![crackme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-16/5.png)

EAX와 LOCAL.15의 값을 동일하게 맞추었다.

![crack]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-16/6.png)

정답 인증에 성공하였다.

정답: 3838184855
