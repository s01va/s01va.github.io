---
layout: single
title: "CodeEngn Basic 12"
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

Key를 구한 후 입력하게 되면 성공메시지를 볼 수 있다 
이때 성공메시지 대신 Key 값이 MessageBox에 출력 되도록 하려면 파일을 HexEdit로 오픈 한 다음 0x???? ~ 0x???? 영역에 Key 값을 overwrite 하면 된다. 
문제 : Key값과 + 주소영역을 찾으시오 
Ex) 7777777????????

![Bin]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/0.png)

프로그램을 실행시키면 다음과 같은 창이 뜬다. 키를 인증하는 프로그램으로 보인다. 이를 PEiD를 통해 조사해 보았다.

![PEiD]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/1.png)

패킹이 되어있지 않은 프로그램임을 알 수 있다. 이대로 리버싱을 시작한다.

![findkey]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-12/2.png)

길게 보이는 문자열이 키 값인 것으로 추측된다. 그리고 성공메시지에 진입하기 위해서는, 그 직전의 EAX값이 7A2896BF와 같아야 함을 알 수 있다.
