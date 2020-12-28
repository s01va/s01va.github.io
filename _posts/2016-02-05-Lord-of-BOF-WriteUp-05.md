---
layout: single
title: "LOB 5번 (orc -> wolfman)"
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
        - wolfman
        - egghunter + buffer hunter
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
        strcpy(buffer, argv[1]); 
        printf("%s\n", buffer);

        // buffer hunter
        memset(buffer, 0, 40);
}
```

Stack frame structure


| i[4] |
| buffer[40] |
| Stack Frame Pointer |
| Return Address |
| argc |
| argv |
| environ |


environ을 memset시키는 부분이 있다. 환경변수를 이용한 공격은 할 수 없다. 공격을 위한 조건은 이전의 문제와 같으니 같은 방법으로 풀이해 보았다. argv[1]에 48바이트를 채우고, argv[2]에 100바이트를 채운 후 그 주소값을 확인하였다.

![disas](https://s01va.github.io/assets/images/2016-02-05-LOB-05/0.png)

(중략)

![disas2](https://s01va.github.io/assets/images/2016-02-05-LOB-05/1.png)

argv[2]가 시작하는 주소지는 0xbffffc1c임을 알 수 있다. 이를 이용하여 다음과 같이 공격을 시도하였다.

![exploit](https://s01va.github.io/assets/images/2016-02-05-LOB-05/2.png)


my-pass: love eyuna