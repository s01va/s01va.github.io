---
layout: single
title: "CodeEngn Basic 20"
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

![start](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/0.png)

이 프로그램은 Key파일을 필요로 하는 프로그램이다. 위 문구가 출력되도록 하려면 crackme3.key 파일안의 데이터는 무엇이 되어야 하는가 
Ex) 41424344454647 
(정답이 여러개 있는 문제로 인증시 맞지 않다고 나올 경우 게시판에 비공개로 올려주시면 확인해드리겠습니다

![crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/1.png)

그냥 실행시키면 다음과 같이 뜬다. Key파일이 있으면 문제와 같이 뜨는 걸로 추정된다. 

![PEiD](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/2.png)

PEiD로 프로그램에 대한 조사를 해 보니 아무런 패킹이 되어있지 않다. 이대로 올리디버거로 분석을 진행한다.

![first](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/3.png)

올리디버거로 열었을 시의 첫 화면이다. CRACKME3.KEY라는 파일을 생성하고 이를 읽는 것을 볼 수 있다.

![Text string](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/4.png)

모든 문자열을 조사했다. 문제에서 보였던 문구가 있는 주소들이 존재한다. 이들에게 중단점을 걸고 주변을 관찰해 보았다. 다음은 401191주소지 근처이다.

![cmp](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/5.png)

CMP AL,1 이후 AL과 1이 같을 시 이 파트를 지나가는 것을 볼 수 있다. 다음은 40137F 주소지 근처이다.

![function](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/6.png)

이 문구가 뜨게 하는 부분이 하나의 함수로 이루어져 있음을 볼 수 있다. 함수의 시작은 주소 401362이다. 위의 401191 주소지 근처에서 여기로 이어지는 것을 볼 수 있다. 다시 401191주소지 근처로 돌아가서 CMP 구문에 중단점을 걸고 실행시켜 보았다.

![EAX](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/7.png)

AL은 EAX의 뒤의 8비트이므로 0E이다. EAX의 마지막 두 16진수가 01이 되어야 정답 판정을 받을 수 있을 것이다. 다음은 CMP AL,1 명령어가 있는 401188주소지의 이전 부분이다.

![pop eax](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/8.png)

POP EAX를 함으로써 CMP를 하기 직전 시점에서 스택의 가장 위에 있는 값을 EAX로 pop하는 것을 볼 수 있다. 즉 CMP하는 시점에서 스택의 맨 위의 값에 따라 키값의 여부가 결정된다고 결론내릴 수 있다. 이제부터 스택을 기준으로 분석을 하도록 하겠다.

![CreateWindowExA](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/9.png)

![stack](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/10.png)

CreateWindowExA 함수를 지난 후의 스택이다. 401159 주소지의 PUSH 0040210E WindowName = “CrackMe v3.0 - Uncracked”가 그대로 최종 스택이 됨을 볼 수 있다. 이제부터 40210E를 추적해 가며 관찰해 보도록 하겠다.

![entry point](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/11.png)

Entry point 지점이다. CreateFileA 함수를 지난 후 401037주소지에서 PUSH 20.0040210E를 하는 부분이 있다. “CrackMe v3.0” 뒤에 공백으로 되어 있지만 바로 아래의 4012F5함수를 지나고 나면 아래와 같이 “Uncracked”라는 문자열이 붙는다.

![Uncracked](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/12.png)

함수 4012F5함수를 조사하였다. 아래는 함수 4012F5이다.

![4012F5](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/13.png)

“CrackMe v3.0”이라는 문자열이 들어 있는 40210E의 뒤에 Little Endian 방식으로 55202D20( - U), 6172636E(ncra), 64656B63(cked)라는 문자열을 쌓고 있다. 이 문자열들은 함수 4012F5 이전의 과정에서 온 것으로 보인다.

![restart](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/14.png)

다시 실행시켜서 처음부터 한줄씩 실행시켜 보았다. CreateFileA함수를 지난 후 CMP EAX,-1을 하여 같지 않으면 401043주소지로 jump하는데, 40210E의 문자열 뒤에 Uncracked라는 문자열이 붙고 401041주소지에서 JUMP가 발생하여 ReadFile함수를 실행하지 않게 되는 것을 확인하였다. 인위적으로 CreateFileA의 인자로 들어가는 “CRACKME3.KEY”라는 이름의 파일을 생성한 후 임의의 문자열 “12345”를 해당 파일에 저장한 후 다시 실행시켜 보았다.

![EAX](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/15.png)

EAX가 FFFFFFFF가 아닌 1E4가 됨으로써 401035주소지에서 jump를 하여 4012F5함수를 실행하지 않고, 뒤이어 401041주소지에서 jump를 수행하지 않아 ReadFile을 수행하는 것을 관찰하였다.

![after ReadFile](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/16.png)

ReadFile 함수를 지나온 직후이다. 아무것도 없던 402008주소지에 CRACKME3.KEY에 입력했던 ASCII “12345”가 들어 있다. 401066주소지에서 CMP를 하고 jump를 수행하는데, 4021A0 주소지에 5가 들어 있다. 12와 같지 않으므로 401037로 jump한다. 그렇게 되면 위에서 수행하지 않았던 함수 4012F5를 수행하고, 전과 같이 “CrackMe v3.0” 문자열 뒤에 Uncracked 문자열이 붙게 된다. 4021A0은 ReadFile의 인자로서 들어가는 pBytesRead였다. CRACKME3.KEY파일에 들어가는 문자열이 16진수로 12, 즉 18바이트가 되면 이를 우회할 수 있을 것이다. CRACKME3.KEY파일을 다음과 같이 수정하였다.

![CRACKME3.KEY](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/17.png)

우회가 되는 것을 확인하였다. 계속 한줄씩 진행하던 도중 다음과 같이 문자열이 변형되는 것을 발견하였다.

![after 401311](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/18.png)

함수 401311을 통과하자 402008주소지에 ASCII “123456789abcdef012”라고 입력되어 있던 문자열이 앞의 아홉 바이트는 모두 p로 바뀌었고, 열 번째 문자열부터 다섯 바이트는 변형이 되었으며, 나머지 바이트는 유지되었다. 아래는 함수 401311과 함수 시작 시 레지스터 상태이다.

![reg](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/19.png)

문자열의 변형은 XOR 연산으로 인해 일어난 것임을 알 수 있었다. EBX의 일부인 BL을 41로 채우고, 이를 1씩 증가시켜 4F가 될 때까지 반복시키기 때문에 앞의 14바이트만 변형이 일어나고 나머지 문자열은 그대로 유지되는 것을 확인할 수 있다.

![return](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/20.png)

함수가 끝나고 리턴한 이후이다. 어떠한 과정을 거치고 AL의 값을 AND연산한 결과를 바탕으로 jump를 수행하는데, 이 분기하는 지점은 위에서 Uncracked를 띄우는 함수 4012F5를 지나가는 곳이다. Uncracked가 뜨지 않게 하기 위해서는 AL이 반드시 1이 되어야 한다. 주소지 40109F에서 jump가 발생하지 않게 하기 위한 조건을 위의 어셈블리어를 분석해 가며 조사하였다.

| XOR DWORD PTR DS:[4020F9],12345678 | 4020F9 주소지에 들어있는 문자열과 12345678를 XOR연산을 시키고 있다. 주소지 4020F9에는 4C7이 들어 있으며, 12345678과 XOR연산을 한 결과는 123452BF가 되며 이것이 주소지 4020F9에 담긴다. |
| ADD ESP,4 | 스택을 쌓는 과정이다. |
| PUSH 20.00402008 | CRACKME3.KEY의 문자열이 변형된 결과인 ppp~f012 문자열을 스택에 쌓는다. |
| CALL 20.0040133C | 이 함수를 통과한 후 EAX에 32313066이라는 값이 쌓였다. 주소지 402008의 맨 마지막 4바이트가 little endian 방식으로 저장된 것과 같다. |
| ADD ESP,4 | 스택을 쌓는 과정이다. |
| CMP EAX,DWORD PTR DS:[4020F9] | EAX에 있는 32313066과 4020F9 주소지에 있는 123452BF를 비교한다. |
| SETE AL | SETE은 Set if Equal이다. 위의 비교대상이 같다면 AL을 1로, 다르면 0으로 세트한다. |
| PUSH EAX | 현재 EAX에 있는 값을 스택에 쌓는다. |
| TEST AL,AL | AL값끼리 AND연산을 진행한다. |
| JE SHORT 20.00401037 | 결과가 0일 시 jump를 수행한다. |

결론적으로 jump를 수행하는 40109F에서 jump를 우회하기 위해서는 4020F9에 little endian으로 들어있는 아스키 코드와 CRACKME3.KEY에 저장되어 있는 18바이트의 문자열 중 마지막 4바이트의 아스키 코드가 일치하면 된다. 한편, 주소지 4020F9는 CRACKME3.KEY파일에 들어있는 문자열을 변형시키던 함수 401311에서 영향을 받은 곳이었다. 어떤 방식으로 영향을 받았는지 다시 확인하기 위해 함수 401311을 다시 조사하였다.

![function 401311](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/21.png)

반복을 진행하며 EAX에 있는 값을 주소지 4020F9에 더하고 있는 것을 볼 수 있다. 즉 최종적으로 4020F9에 들어가는 결과값은 CRACKME3.KEY의 앞 14바이트에 어떤 문자열이 오느냐에 따라 달려 있다고 볼 수 있다. 정리하자면, CRACKME3.KEY에 들어 있는 문자열의 앞 14바이트가 함수 401311을 통해 생성된 4020F9 주소지에 저장되는 값을 0x12345678과 AND연산한 결과가 CRACKME3.KEY의 나머지 4바이트와 일치하는 것이 정답의 조건이 된다.

![401093](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/22.png)

우선, 주소 401093 지점 이전에 4020F9 값을 EAX와 같게 조작해 주고 경과를 관찰해 보았다.

![bypass](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/23.png)

JE 부분에서 jump가 일어나지 않았고 CrackMe 문자열 뒤에 Cracked가 뜸으로써 우회가 성공하였다.

![good work cracker 2](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/24.png)

단, 완성된 창에서 “Cracked by: CodeEngn이 아닌 다른 문자열이 들어가 있다. CodeEngn 대신에 들어가 있는 문자열은 CRACKME3.KEY 파일에 넣었던 문자열의 앞 14바이트가 변조된 값이다. 변조 과정은 XOR 연산이었으며, XOR 연산은 역연산을 해도 같은 결과가 나오므로 변조 전의 문자가 무엇이었는지를 다음과 같은 과정으로 추적하였다.

| CodeEngn 문자열의 ASCII 코드
C = 0x43   o = 0x6f   d = 0x64   e = 0x65
E = 0x45   n = 0x6e   g = 0x67   n = 0x6e

이 CodeEngn의 아스키 코드를 41부터 1씩 증가시켜가며 XOR 연산을 시킨다.
결과는 아래와 같다.
0x02 0x2d 0x27 0x21 0x00 0x28 0x20 0x26
아스키 코드 0x21 아래로는 문자로 표기할 수 없다. |

9번째 바이트부터 14번째 바이트까지는 없어져야 한다. 여기서 잠시 함수 401311을 다시 확인해 보도록 한다.

![401311](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/25.png)

40132A에서 AL이 0과 같을 시 함수를 바로 빠져나오는 것을 볼 수 있다. 즉 아홉번째 반복에서 BL값인 0x49와 XOR 연산을 하였을 때 null이 되는 것을 아홉번째 바이트에 들어가도록 하고, 10번째 바이트부터 15번째 바이트는 아무 문자나 넣어도 상관 없을 것이다.  맨 마지막 4바이트는  위에서 4020F9 주소지에서 연산했던 과정과 같으므로 위와 같은 과정을 통해 찾았다. 이로써 CRACKME3.KEY에 들어갈 문자열의 아스키 코드 16진수 값은 아래와 같다.
02 2D 27 21 00 28 20 26 49 ?? ?? ?? ?? ?? 7B 55 34 12

![cracked](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-20/26.png)

제출한 정답: 022D27210028202649DEADBEEF007B553412
