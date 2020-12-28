---
layout: single
title: "LOB 11번 (skeleton -> golem)"
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
        - golem
        - stack destroyer
*/

#include <stdio.h>
#include <stdlib.h>

extern char **environ;

main(int argc, char *argv[])
{
        char buffer[40];
        int i;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        if(argv[1][47] != '\xbf')
        {
                printf("stack is still your friend.\n");
                exit(0);
        }

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // stack destroyer!
        memset(buffer, 0, 44);
        memset(buffer+48, 0, 0xbfffffff - (int)(buffer+48));
}
```

Stack frame structure:

| i[4] |
| buffer[40] |
| Stack frame pointer |
| Return address |
| argc |
| argv |
| environ |

환경변수를 초기화시키고 buffer를 0부터 40까지 0로 초기화시키고 있으며 argv를 모두 초기화시키고 있다. 거기에 남은 스택 영역까지 모두 0으로 초기화시키고 있다. 환경변수를 응용한 공격기법도 argv를 이용한 공격기법도 통하지 않게 되었다. 공유 라이브러리에 대한 힌트를 주었는데, 우선 라이브러리에 대한 개념을 간단히 정리해 보고자 한다.

자주 사용되는 기능들을 분리시켜 바이너리 형태로 모아놓은 것을 라이브러리라고 하며, 라이브러리에는 정적 라이브러리와 동적 라이브러리가 있다. 정적 라이브러리(Static library)는 컴파일, 링킹 단계에서 라이브러리를 실행 바이너리에 포함시키는 방식의 라이브러리를 뜻한다. 이와 같은 방식은 라이브러리를 사용하는 프로그램이 늘어날수록 불필요하게 실행 파일들의 크기가 커지고 퍼포먼스가 떨어지는 등 비효율적이기 때문에 자주 사용되지 않는다.

위와 같은 이유로 동적 라이브러리(Dynamic Library)가 더 잘 사용되는 경향이 있다. 동적 라이브러리는 여러 프로그램들이 공통으로 필요로 하는 기능들을 따로 모아 필요할 때에 쓸 수 있게끔 만들어 놓은 것이다. 동적 라이브러리는 호출하는 프로그램을 해당 모듈을 실행시킬 때에만 불러와서 사용하는 방식으로, 프로그램에는 호출할 라이브러리 함수의 정보만 적재하면 되기 때문에 정적 라이브러리에 비해 메모리를 효율적으로 사용할 수 있는 장점이 있다. 윈도우에서는 DLL(Dynamic Linked Library)이라고 부르며, 리눅스에서는 공유 라이브러리(Shared Library)라고 부른다. 공유 라이브러리는 프로그램 시작 시 메모리에 적재된다.

위와 같은 것을 알아둔 후, 맨 위에서 언급했던 메모리 영역 이미지를 상기시켜 보자.

![stack frame](https://s01va.github.io/assets/images/2016-02-05-LOB-11/0.png)

Stack 영역 아래에 Shared library영역이 존재하는 것을 알 수 있다. 이 공유라이브러리를 응용해서 공격을 진행해 보았다.

![ls](https://s01va.github.io/assets/images/2016-02-05-LOB-11/1.png)

ldsh.c라는 빈 파일을 생성한 후 이것으로 쉘코드를 컴파일한다.

![gcc](https://s01va.github.io/assets/images/2016-02-05-LOB-11/2.png)

![ls2](https://s01va.github.io/assets/images/2016-02-05-LOB-11/3.png)


- shared: 공유 라이브러리를 우선 링크하라
- fPIC: object 파일을 만들 시 심볼이 어느 위치에 있던 동작을 하는 구조로 컴파일 하라

공유 라이브러리는 LD_PRELOAD라는 환경변수에 등록시키면 해당 영역에 올릴 수 있게 된다. 이를 환경변수에 등록시킨다.

![export](https://s01va.github.io/assets/images/2016-02-05-LOB-11/4.png)

gdb로 분석하여 LD_PRELOAD에 포함되어 있는 쉘코드의 위치를 찾는다.

![memory](https://s01va.github.io/assets/images/2016-02-05-LOB-11/5.png)

0xbffff564부터 쉘코드가 위치하고 있는 것을 찾았다. 이를 이용해 공격을 진행하였다.

![my-pass](https://s01va.github.io/assets/images/2016-02-05-LOB-11/6.png)

my-pass: cup of coffee
