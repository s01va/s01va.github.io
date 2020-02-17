---
layout: single
title: "CodeEngn Basic 03"
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

비주얼베이직에서 스트링 비교함수 이름은?

![error]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/0.png)


올리디버거로 열려고 하니 오류창이 뜨면서 시작한다.
[설치경로](https://support.microsoft.com/ko-kr/help/180071/file-msvbvm50.exe-installs-visual-basic-5.0-run-time-files)
올리디버거로 파일 열기에 성공했을 시, 보여지는 entry point는 여기이다.

![entry point]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/1.png)

F7을 눌러 처음으로 call하는 함수로 들어갔다.

![mainassem]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/2.png)

전체 프로그램의 main처럼 보이는 곳에 진입하려는 것과, 모든 함수들이 한데 모여있는 것을 볼 수 있다.

4줄쯤 위에 비교함수처럼 보이는 함수가 눈에 띈다.
정답은 vbaStrCmp

해당 프로그램을 실행시키면 다음과 같은 화면이 뜬다.

![crackme]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/3.png)

Regcode칸에 아무 문자열이나 입력하면 다음과 같은 오류창이 뜬다.

![crackme2]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/4.png)

내친김에 패스워드까지 알아내 보도록 한다.

![findpw]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/5.png)

앞에서 찾은 비교함수 부분에 breakpoint를 걸고 프로그램을 실행시킨다.

![crackme3]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/6.png)

프로그램이 뜨면 아무 문자열이나 입력시켜 주고 확인버튼을 누르면 Stack이 다음과 같이 쌓여 있는 것을 볼 수 있다.

![stack]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-03/7.png)

앞에서 입력한 문자열과는 다른 패스워드로 추정되는 문자열이 있다.

