---
layout: single
title: "CodeEngn Basic 10"
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

OEP를 구한 후 "등록성공"으로 가는 분기점의 OPCODE를 구하시오. 정답인증은 OEP + OPCODE
EX) 00400000EB03

![crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/0.png)

시리얼 키를 인증하는 프로그램으로 보인다. PEiD로 이 프로그램에 대한 정보를 얻는다.

![PEiD](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/1.png)

ASPack으로 패킹되어 있는듯하다.

![before unpack entrypoint](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/2.png)

언패킹 이전 entry point이다. 이를 언패킹하기 위해서는 retn 0c를 찾은 후, 그 아래에 있는 retn으로 돌아가면 된다.

![before unpack retn](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/3.png)

retn으로 돌아갔을 시 도달하는 곳이다.

![DB55](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/4.png)

여기에서 dump를 뜨고 LordPE라는 툴을 사용해 PE로 리빌드해준다.

![ollyDump](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/5.png)

![LordPE](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/6.png)

![entrypoint](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/7.png)

OEP는 445834이다.

![JNZ](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-10/8.png)

한줄씩 실행시키면서 등록성공에 진입하는 것으로 보이는 분기문을 찾았다. 해당 OPCODE는  7555이다.

정답: 004458347555

