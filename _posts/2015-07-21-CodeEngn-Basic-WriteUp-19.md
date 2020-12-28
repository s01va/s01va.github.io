---
layout: single
title: "CodeEngn Basic 19"
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


이 프로그램은 몇 밀리세컨드 후에 종료 되는가

![crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/0.png)

다음과 같은 창이 뜨는 프로그램이다. 확인 버튼을 눌러도 종료되지만, 방치해 두어도 수 초 뒤에 저절로 종료되는 것을 볼 수 있었다. 이 프로그램을 PEiD로 분석해 보았다.

![PEiD](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/1.png)

UPX로 패킹되어 있었다. 패킹을 풀어주도록 한다.

![unpack](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/2.png)

패킹을 풀고 올리디버거로 열었다.

![func](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/3.png)

내부 함수들만 모아 보았다. Sleep, timeGetTime, SetTimer 등의 시간과 관련된 듯 한 함수들이 보인다. DestroyWindow 함수도 찾을 수 있었다. timeGetTime 함수는 Sleep함수 호출 시 몇 밀리세컨드만큼 중지할 것인지를 리턴하는 함수라고 한다. 이 함수들에 중단점을 걸고 실행시켜 보았다.

![warning](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/4.png)

다음과 같은 경고창이 뜨며 실행을 계속할 수 없었다. 디버거 안에서 실행시키지 않을 때에는 다음과 같은 현상이 없으므로 안티디버깅 기법이 걸려 있다고 판단했다.

![IsDebuggerPresent](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/5.png)

다음과 같은 함수가 있음을 발견했다. 이 함수가 있는 곳에 중단점을 걸고 실행시켰더니 아까와 같은 경고창이 뜨지 않았다. 이제 이 함수를 우회하도록 하겠다.

![TEST](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/6.png)

IsDebuggerPresent함수를 지난 후, EAX값을 And연산을 하여 그 결과가 0이 아닐 시 Jump를 수행한다. 아래는 Jump해서 도달하는 곳이다.

![after jump](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/7.png)

위에서 보았던 경고 구문임을 확인할 수 있다. IsDebuggerPresent 함수에서 리턴하는 EAX값을 0으로 만드는 방법도 있으나 MOV EAX,0으로 코드패치를 하는 방법을 선택했다. 

![codepatch](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/8.png)

다음과 같이 코드패치를 하고 그대로 덤프를 뜬 파일로 디버깅을 진행한다. 전과 같은 안티디버깅은 일어나지 않았다. 이제 본래 하려고 했던 timeGetTime함수에 중단점들을 걸고 프로그램을 실행시켜 관찰해 보도록 하겠다.

![004193AA](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/9.png)

그대로 실행시켜 보니 다음과 같은 지점에서 멈추었다.

![timeGetTime](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/10.png)

계속 실행시키면 다른 곳에서 멈추지 않고 창이 바로 떴다. 다른 곳은 참조하지 않는 것으로 판단했다. 리턴 값이 중요하니 함수 내부는 관찰하지 않았다. 444C3E에서 timeGetTime의 리턴값을 ESI에 넣고, 444C5F의 Sleep함수의 리턴값을 EAX에 넣어 이를 비교시킨다. 아래는 444C63의 JNB에서 분기하는 지점이다.

![444D3A](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/11.png)

444D3A에서 EAX의 값이 [EBX+4]의 값보다 크지 않으면 timeGetTime 함수를 한번 더 거치게 되어 있다. [EBX+4]의 주소값에 들어 있는 값은 2B70이다.

![10](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-19/12.png)

2B70은 10진수로 11120이다. timeGetTime함수의 리턴값과 Sleep함수의 리턴값의 차가 이것을 넘지 않았을 시 계속 수행하는 것으로 보아 이 프로그램은 11120 밀리세컨드 뒤에 자동종료가 된다고 판단할 수 있다.

정답: 11120
