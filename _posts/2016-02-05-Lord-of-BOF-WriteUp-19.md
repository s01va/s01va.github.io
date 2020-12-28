---
layout: single
title: "LOB 19번 (nightmare -> xavius)"
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
        - xavius
        - arg
*/

#include <stdio.h>
#include <stdlib.h>
#include <dumpcode.h>

main()
{
        char buffer[40];
        char *ret_addr;

        // overflow!
        fgets(buffer, 256, stdin);
        printf("%s\n", buffer);

        if(*(buffer+47) == '\xbf')
        {
                printf("stack retbayed you!\n");
                exit(0);
        }

        if(*(buffer+47) == '\x08')
        {
                printf("binary image retbayed you, too!!\n");
                exit(0);
        }

        // check if the ret_addr is library function or not
        memcpy(&ret_addr, buffer+44, 4);
        while(memcmp(ret_addr, "\x90\x90", 2) != 0)     // end point of function
        {
                if(*ret_addr == '\xc9'){                // leave
                        if(*(ret_addr+1) == '\xc3'){    // ret
                                printf("You cannot use library function!\n");
                                exit(0);
                        }
                }
                ret_addr++;
        }

        // stack destroyer
        memset(buffer, 0, 44);
        memset(buffer+48, 0, 0xbfffffff - (int)(buffer+48));

        // LD_* eraser
        // 40 : extra space for memset function
        memset(buffer-3000, 0, 3000-40);
}
```

가장 먼저 여태까지 대부분 argv로 입력값을 받고 있던 것을 stdin으로 받고 있다.
그리고 buffer+47에 있는 값, 즉 return address의 주소지 맨 앞부분이 \xbf이거나 \x08인지 체크하고 있다(20번째, 26번째줄).
또한 buffer + 44, buffer+45가 각각 \x90와 같지 않으면 while문을 돌게 하고 있다(33 ~ 34번째줄).
fgets는 stdin으로 입력을 받는다. 우선 입력받는 stdin이 어느 주소지에 위치해 있는지를 알아볼 필요가 있다고 생각했다.

![disas](https://s01va.github.io/assets/images/2016-02-05-LOB-19/0.png)

어떤 함수에 인자로 들어가는 값과 리턴되는 값은 eax를 통한다. fgets에 들어가기 전 eax에 마지막으로 담기는 값은 0x8049a3c에 들어있는 값이다(main+6).

![memory_stdin](https://s01va.github.io/assets/images/2016-02-05-LOB-19/1.png)

stdin값이 맞다. 그리고 해당 주소지에 들어있는 값은 0x401068c0이다. 이전의 문제들에서는 buffer+47의 값이 \x40와 같은지를 확인했었는데 이 문제에서는 확인하고 있지 않는 이유는 이를 활용하는 문제이기 때문일 것이라고 추측하였다. 다시한번 fgets가 끝나는 시점인 main+26에 breakpoint를 걸고 stdin에 입력값을 넣은 후 이의 주소지를 확인해 보았다.

![memory](https://s01va.github.io/assets/images/2016-02-05-LOB-19/2.png)

stdin에 반복적으로 나타나는 0x40015000 주소지를 확인해 보았다.

![memory2](https://s01va.github.io/assets/images/2016-02-05-LOB-19/3.png)

stdin 입력값은 0x40015000에 들어있음을 확인하였다. 이제 main함수가 다 끝나고 leave-ret을 하기까지 stdin에 입력값이 남아있는지 확인해 보았다.

![memory3](https://s01va.github.io/assets/images/2016-02-05-LOB-19/4.png)

stdin에 값이 남아있음을 확인하였다. 이 위치에 쉘코드를 입력하면 공격이 성공할 것이다.

![exploit](https://s01va.github.io/assets/images/2016-02-05-LOB-19/5.png)


my-pass: throw me away
