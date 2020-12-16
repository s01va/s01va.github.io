---
layout: single
title: "LOB 7번 (darkelf -> orge)"
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
        - orge
        - check argv[0]
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

        // here is changed!
        if(strlen(argv[0]) != 77){
                printf("argv[0] error\n");
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

이전 문제에 조건이 하나 더 추가되었다. argv[0]의 길이가 77이 되어야 한다. 링크를 이용해 이를 우회할 수 있을 것이다.

![ln]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-07/0.png)

하드 링크를 생성하였다. 하드 링크 파일을 생성하면 원본 파일과 inode number를 공유하기 때문에 원본 파일과 실질적으로 같은 파일이 된다. 권한 문제 때문에 하드 링크를 생성해야 한다. 하드 링크 파일이 위치하는 디렉토리의 이름은 70자로 하였다(./[2] + 디렉토리 이름[70] + /orge[5] == 7).

![ex]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-07/1.png)

해당 조건문이 우회되는 것을 확인하였다. 이후의 과정은 이전 문제와 같은 방식으로 해결하였다. 공격을 하는 상황과 유사하게 ‘Z’가 70번 반복되는 이름의 디렉토리를 생성한 후 그곳에 파일 orge를 복사하여 gdb로 분석하였다.

![argv addr]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-07/2.png)

(중략)

![argv addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-07/3.png)

argv[1]에 48자, argv[2]에 200자를 넣고 주소지를 확인하였다. argv[2]는 주소지\xbffffb5c부터 위치함을 볼 수 있다. 이를 이용하여 아래와 같이 공격을 진행하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-07/4.png)

![my-pass]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-07/5.png)

my-pass: timewalker