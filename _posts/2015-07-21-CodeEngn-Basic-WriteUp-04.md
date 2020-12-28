---
layout: single
title: "CodeEngn Basic 04"
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

이 프로그램은 디버거 프로그램을 탐지하는 기능을 갖고 있다. 디버거를 탐지하는 함수의 이름은 무엇인가

![exe](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-04/0.png)


우선 프로그램을 실행시켜 보면, 정상이라는 텍스트가 반복되어서 나오는 것을 볼 수 있다.

이제 올리디버거를 통해 이 프로그램을 실행시키면 다음과 같은 화면을 볼 수 있다.

![check_debugtool](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-04/1.png)

프로그램의 처음부터, “디버깅 당함”이라는 문자열이 뜨기 시작하는 부분의 함수를 찾았다.

![find function](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-04/2.png)

이 함수로 내부로 진입한다.

![isdebuggerpresent](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-04/3.png)

디버깅을 탐지하는 것으로 보이는 함수 이름이 코멘트로 달려있는 것을 확인할 수 있다.

정답: IsDebuggerPresent
