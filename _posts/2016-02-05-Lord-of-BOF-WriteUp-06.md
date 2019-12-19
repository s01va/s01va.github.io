---
layout: single
title: "LOB wolfman -> darkelf"
#description: ""
date: 2016-02-05 12:00:00 -0400
# modified: 
tags: 
- WarGame
- WriteUp
- Pwnable
comments: true
share: true
---

source code:

```c

1  ﻿/*
2          The Lord of the BOF : The Fellowship of the BOF
3          - darkelf
4          - egghunter + buffer hunter + check length of argv[1]
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
32         // check the length of argument
33         if(strlen(argv[1]) > 48){
34                 printf("argument is too long!\n");
35                 exit(0);
36         }
37 
38         strcpy(buffer, argv[1]);
39         printf("%s\n", buffer);
40 
41         // buffer hunter
42         memset(buffer, 0, 40);
43 }

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

![argv addr]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-06/0.png)

(중략)

![argv addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-06/1.png)

argv[2]는 0xbffffb0c부터 위치하는 것을 확인할 수 있다. 이를 바탕으로 아래와 같이 공격을 진행하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-06/2.png)

![my-pass]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-06/3.png)


my-pass: kernel crashed