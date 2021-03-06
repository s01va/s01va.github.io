---
layout: single
title: "LOB 12번 (golem -> darkknight)"
#description: ""
date: 2016-02-05 12:00:00 -0400
# modified: 
tags: 
- wargame
- writeup
- pwnable
- lob
comments: true
share: true
---

source code:

```c
/*
        The Lord of the BOF : The Fellowship of the BOF
        - darkknight
        - FPO
*/

#include <stdio.h>
#include <stdlib.h>

void problem_child(char *src)
{
        char buffer[40];
        strncpy(buffer, src, 41);
        printf("%s\n", buffer);
}

main(int argc, char *argv[])
{
        if(argc<2){
                printf("argv error\n");
                exit(0);
        }

        problem_child(argv[1]);
}
```

Stack frame structure:

| buffer[40] |
| [problem_child] SFP |
| [problem_child] RET |
| [main] SFP  |
| [main] RET |
| argc |
| argv |
| environ |

힌트로 FPO를 주었다. FPO는 Frame Pointer Overflow의 약자로, fake ebp의 일종이다. 여태까지 공격한 것들을 보면 return address 이후로는 손을 댈 수 없는 것이 원칙이었으나, fake ebp기법을 활용해 ebp의 위치를 옮기면 공격자가 원하는 위치에서 원하는 return address를 추출하는 것이 가능하다.

problem_child 함수를 보면 strncpy(buffer, src, 41) 함수가 존재하는데, 이 함수에는 원래는 40bytes인 buffer의 1byte를 오버플로우 시킬 수 있는 취약점이 존재한다. 즉 problem_child 함수의 SFP의 1byte를 수정시킬 수 있는 점을 보고 FPO라는 공격기법을 힌트로 준 것으로 보인다. 아래는 이를 시도한 것이다.

![disas](https://s01va.github.io/assets/images/2016-02-05-LOB-12/0.png)

bp를 problem_child가 종료되기 직전인 0x8048469(leave)에 걸고 buffer에 41바이트를 채워넣어 보았다.

![memory1](https://s01va.github.io/assets/images/2016-02-05-LOB-12/1.png)

![memory2](https://s01va.github.io/assets/images/2016-02-05-LOB-12/2.png)

ebp의 한 바이트가 덮여있는 것을 볼 수 있다. 또한 ebp가 한 바이트가 덮여있는 SFP 주소지인 0xbffffa41을 가리키고 있는 것을 볼 수 있다. 본래 buffer의 크기만큼 채워 보았을 때 ebp가 어떠한지도 확인해 보았다.

![memory3](https://s01va.github.io/assets/images/2016-02-05-LOB-12/3.png)

이로써 ebp의 한 바이트를 조작할 수 있음을 확인하였다. 이제 0xbfffa00 ~ 0xbfffaff 범위에 쉘코드를 넣고 이 범위에 맞추어서 problem_child의 ebp를 조작하면 된다. strncpy 직후인 problem_child+21에 bp를 걸고 buffer의 위치를 확인해 보았다.

![memory4](https://s01va.github.io/assets/images/2016-02-05-LOB-12/3.png)

![memory5](https://s01va.github.io/assets/images/2016-02-05-LOB-12/4.png)

![info_frame](https://s01va.github.io/assets/images/2016-02-05-LOB-12/5.png)

buffer가 0xbffffab4 ~ 0xbffffadb에 위치하고 있는 것을 확인하였다. 또한 바로 다음에 수행할 명령어의 위치를 나타내는 eip가 ebp보다 4만큼 큰 것을 확인하였다. 이를 이용하여 buffer 자리에 25바이트 쉘코드를 삽입하고 0xbffffab4로 eip를 조작하면 공격이 성공할 것이다. 페이로드를 아래와 같이 만들어서 공격을 진행해 보았다.

![exploit](https://s01va.github.io/assets/images/2016-02-05-LOB-12/6.png)


my-pass: new attacker