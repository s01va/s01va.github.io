---
layout: single
title: "LOB orge -> troll"
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
3          - troll
4          - check argc + argv hunter
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
17         // here is changed
18         if(argc != 2){
19                 printf("argc must be two!\n");
20                 exit(0);
21         }
22 
23         // egghunter
24         for(i=0; environ[i]; i++)
25                 memset(environ[i], 0, strlen(environ[i]));
26 
27         if(argv[1][47] != '\xbf')
28         {
29                 printf("stack is still your friend.\n");
30                 exit(0);
31         }
32 
33         // check the length of argument
34         if(strlen(argv[1]) > 48){
35                 printf("argument is too long!\n");
36                 exit(0);
37         }
38 
39         strcpy(buffer, argv[1]);
40         printf("%s\n", buffer);
41 
42         // buffer hunter
43         memset(buffer, 0, 40);
44 
45         // one more!
46         memset(argv[1], 0, strlen(argv[1]));
47 }

```

Stack frame structure:

| i[4] |
| buffer[40] |
| Stack frame pointer |
| Return Address |
| argc |
| argv |
| environ |


stack frame은 이전 문제와 동일하다. 단 argument를 강제하는 분기문이 생겨서 이전처럼 argument를 여러 개 생성하여 공격하는 방식이 통하지 않게 되었다.
하지만 위의 코드는 argv[0] 값을 검사하지 않고 있다. 하드링크를 만들고 거기에 쉘코드를 적재하여 이를 호출해 보았다.

![mkdir]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-08/0.png)

디렉토리 생성을 목적으로 하였기 때문에 일부러 \x2f가 없는 쉘코드를 사용하였다. 그런데 위와 같이 생성한 디렉토리에 하드링크 생성이 되지 않기 때문에 동일한 길이의 이름을 가진 디렉토리를 생성한 후 이후에 이것의 이름을 바꾸기로 하였다.

![rename1]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-08/1.png)

![rename2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-08/2.png)

연속되는 Z(0x5a)가 시작되는, 즉 argv[0]의 시작 주소는 0xbffff9a8이다. 이 디렉토리의 이름을 쉘코드를 포함한 문자열로 바꾼 후 진입하여 위에서 구한 주소지를 응용해 페이로드를 다음과 같이 작성하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-08/0.png)


my-pass: aspirin
