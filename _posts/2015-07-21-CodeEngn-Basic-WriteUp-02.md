---
layout: single
title: "CodeEngn Basic 02"
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

패스워드로 인증하는 실행파일이 손상되어 실행이 안되는 문제가 생겼다. 패스워드가 무엇인지 분석하시오


![error](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-02/0.png)

올리디버거로 열면 다음과 같은 오류가 뜬다.
Hex editor로 열어보도록 한다. 본인은 010 editor를 사용하였다.

![010editor](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-02/1.png)


쭉쭉 내리다 보면 해냈다는 메시지와 함께 플래그를 확인할 수 있다.
정답은 JK3FJZh
