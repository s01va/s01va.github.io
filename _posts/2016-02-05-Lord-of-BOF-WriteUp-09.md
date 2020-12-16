---
layout: single
title: "LOB 9번 (troll -> vampire)"
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
        - vampire
        - check 0xbfff
*/

#include <stdio.h>
#include <stdlib.h>

main(int argc, char *argv[])
{
        char buffer[40];

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        if(argv[1][47] != '\xbf')
        {
                printf("stack is still your friend.\n");
                exit(0);
        }

        // here is changed!
        if(argv[1][46] == '\xff')
        {
                printf("but it's not forever\n");
                exit(0);
        }

        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);
}
```

Stack frame structure:

| buffer[40] |
| Stack frame pointer |
| Return address |
| argc |
| argv |
| environ |


이전 문제와는 다르게 argv[1][46]의 값도 체크하고 있다. 환경변수 영역을 초기화시키지 않아서 환경변수를 응용하는 방법을 떠올릴 수 있지만 \xbfff0000 이상의 위치에 환경변수가 위치하고 있기 때문에 이는 사용할 수 없다. 그렇다고 argv[0]을 이용할 수도 없다. 이 또한 \xbfff0000 이상의 위치에 있기 때문이다.
주소지 \xbfff0000 아래로 내려가는 한 가지 방법으로 스택을 키우는 것이 있다. buffer에 많은 수의 문자열을 넣어 스택을 낮은 주소지 쪽으로 키우는 것이다. gdb를 실행시켜 buffer에 팔만개의 바이트를 입력하였다.

![buffer argv]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-09/0.png)

(중략)

![buffer argv2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-09/1.png)

이쯤 되니 주소지가 \xbffe ... 이 되는 것을 확인할 수 있다. 이를 이용하여 페이로드를 다음과 같이 입력하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-09/2.png)


my-pass: music world