---
layout: single
title: "LOB goblin -> orc"
#description: ""
date: 2016-02-05 12:00:00 -0400
# modified: 
tags: 
- wargame
- writeup
- pwnable
comments: true
share: true
---

source code:

```c

1  ﻿/*
2          The Lord of the BOF : The Fellowship of the BOF
3          - orc
4          - egghunter
5  */
6  
7  #include <stdio.h>
8  #include <stdlib.h>
9  
10 extern char **environ;
11 
12 main(int argc, char *argv[])
13 {
14         char buffer[40];
15         int i;
16 
17         if(argc < 2){
18                 printf("argv error\n");
19                 exit(0);
20         }
21 
22         // egghunter
23         for(i=0; environ[i]; i++)
24                 memset(environ[i], 0, strlen(environ[i]));
25 
26         if(argv[1][47] != '\xbf')
27         {
28                 printf("stack is still your friend.\n");
29                 exit(0);
30         }
31 
32         strcpy(buffer, argv[1]);
33         printf("%s\n", buffer);
34 }

```

stack frame structure:

| i[4] |
| buffer[40] |
| Stack frame pointer |
| Return Address |
| argc |
| argv[0] |
| argv[1] |
| … |

environ을 memset시키기 때문에 환경변수를 이용한 공격은 사용할 수 없다. 그리고 argc가 2 이상이 되도록 하며, argv[1][47]이 ‘\xbf’여야 strcpy(buffer, argv[1])이 실행될 수 있다는 것을 확인할 수 있다. exploit을 위한 조건은 다음과 같다.
- argv[1]이 buffer에 그대로 들어갈 것이기 때문에 exploit을 위해서 길이를 48bytes로 만들 필요가 있다.
- argv[1][47]은 반드시 ‘\xbf’가 되어야 한다.

다음은 orc의 어셈블리어이다.

![orc]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-04/0.png)

![orc1]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-04/1.png)

argv[1]을 주었을 시 주소지를 알아볼 필요가 있다. 입력값의 길이를 48bytes로 맞추어 주었다. argv[2]를 활용할 경우도 생각하여 다음과 같이 입력값을 주었다.

![argv addr]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-04/2.png)

(중략)

![argv addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-04/3.png)

![argv addr3]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-04/4.png)

0xbfffbdc부터 0xbffffc0b에 argv[1]이 들어가 있는 것을 볼 수 있다. 0xbffffc0c부터는 argv[2]가 시작되고 있다. argv[2] 자리에 shellcode를 적재시킨다면 위의 조건을 모두 맞추면서 exploit이 성공할 것이다. 아래와 같이 공격을 시도하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-04/5.png)

권한 상승에 성공하였다.


my-pass: cantata