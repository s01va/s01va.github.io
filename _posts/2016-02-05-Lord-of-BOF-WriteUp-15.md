---
layout: single
title: "LOB giant -> assassin"
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

1  /*
2          The Lord of the BOF : The Fellowship of the BOF
3          - assassin
4          - no stack, no RTL
5  */
6  
7  #include <stdio.h>
8  #include <stdlib.h>
9  
10 main(int argc, char *argv[])
11 {
12         char buffer[40];
13 
14         if(argc < 2){
15                 printf("argv error\n");
16                 exit(0);
17         }
18 
19         if(argv[1][47] == '\xbf')
20         {
21                 printf("stack retbayed you!\n");
22                 exit(0);
23         }
24 
25         if(argv[1][47] == '\x40')
26         {
27                 printf("library retbayed you, too!!\n");
28                 exit(0);
29         }
30 
31         strcpy(buffer, argv[1]);
32         printf("%s\n", buffer);
33 
34         // buffer+sfp hunter
35         memset(buffer, 0, 44);
36 }

```

Stack frame structure:

| buffer[40] |
| SFP |
| RET |
| argc |
| argv |
| environ |

19번째 줄에서 스택 사용을 방지하고 있고, 25번째 줄에서 argv[1][47]의 값을 검사함으로써 라이브러리 사용을 막고 있고, 32번째 줄에서 buffer와 sfp를 모두 0으로 지워버리고 있다. 이번엔 RET sled라는 공격기법을 적용해 보았다.
RET sled는 간단하다. 함수가 끝날 때 호출되는 ret에 ret 주소를 입력하면, 그 다음에 오는 주소로 리턴되는 원리를 사용한 것이다. 이전까지는 ret 자리에 shell의 주소를 입력했다면, 이번에는 ret 자리에 ret 주소를 쓰고 바로 뒤이어서 shell 주소를 입력하는 것이다.

![disas]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-15/0.png)

ret의 주소를 확인하였다. 0x0804851e이다. 여기에 breakpoint를 걸고 아래와 같이 입력하여 확인하였다.

![memory]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-15/1.png)

![memory2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-15/2.png)

우선 ‘if(argv[1][47] == '\xbf')’ 조건을 성공적으로 우회한 것을 볼 수 있다. buffer 영역은 memset되어서 활용하지 못하고, argv 영역은 사용할 수 있다. argv에서 B(\x42)를 입력한 부분은 0xbffffc20 즈음으로 생각하고 아래와 같은 페이로드를 입력하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-15/3.png)


my-pass: pushing me away