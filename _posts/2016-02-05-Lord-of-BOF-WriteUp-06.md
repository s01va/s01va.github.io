---
layout: single
title: "LOB 6번 (wolfman -> darkelf)"
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
﻿/*
        The Lord of the BOF : The Fellowship of the BOF
        - darkelf
        - egghunter + buffer hunter + check length of argv[1]
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

        // egghunter
        for(i=0; environ[i]; i++)
                memset(environ[i], 0, strlen(environ[i]));

        if(argv[1][47] != '\xbf')
        {
                printf("stack is still your friend.\n");
                exit(0);
        }

        // check the length of argument
        if(strlen(argv[1]) > 48){
                printf("argument is too long!\n");
                exit(0);
        }

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // buffer hunter
        memset(buffer, 0, 40);
}
```

Stack frame structure:

| i[4] |
| buffer[40] |
| Stack Frame Pointer |
| Return address |
| argc |
| argv |
| environ |


이전 문제의 조건에 argv[1]의 크기를 한정하는 조건이 추가되었다. 이전 문제들을 풀이할 때에도 argv[1]의 크기는 딱 48바이트로 맞추었으므로 같은 방식으로 문제를 풀어도 문제되지 않을 것이다. argv[1]에 48바이트를, argv[2]에 100바이트를 넣어 이들의 주소지를 확인해 보았다.

![argv addr](https://s01va.github.io/assets/images/2016-02-05-LOB-06/0.png)

(중략)

![argv addr2](https://s01va.github.io/assets/images/2016-02-05-LOB-06/1.png)

argv[2]는 0xbffffb0c부터 위치하는 것을 확인할 수 있다. 이를 바탕으로 아래와 같이 공격을 진행하였다.

![exploit](https://s01va.github.io/assets/images/2016-02-05-LOB-06/2.png)

![my-pass](https://s01va.github.io/assets/images/2016-02-05-LOB-06/3.png)


my-pass: kernel crashed