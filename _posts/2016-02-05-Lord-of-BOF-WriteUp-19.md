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

1  /*
2          The Lord of the BOF : The Fellowship of the BOF
3          - xavius
4          - arg
5  */
6  
7  #include <stdio.h>
8  #include <stdlib.h>
9  #include <dumpcode.h>
10 
11 main()
12 {
13         char buffer[40];
14         char *ret_addr;
15 
16         // overflow!
17         fgets(buffer, 256, stdin);
18         printf("%s\n", buffer);
19 
20         if(*(buffer+47) == '\xbf')
21         {
22                 printf("stack retbayed you!\n");
23                 exit(0);
24         }
25 
26         if(*(buffer+47) == '\x08')
27         {
28                 printf("binary image retbayed you, too!!\n");
29                 exit(0);
30         }
31 
32         // check if the ret_addr is library function or not
33         memcpy(&ret_addr, buffer+44, 4);
34         while(memcmp(ret_addr, "\x90\x90", 2) != 0)     // end point of function
35         {
36                 if(*ret_addr == '\xc9'){                // leave
37                         if(*(ret_addr+1) == '\xc3'){    // ret
38                                 printf("You cannot use library function!\n");
39                                 exit(0);
40                         }
41                 }
42                 ret_addr++;
43         }
44 
45         // stack destroyer
46         memset(buffer, 0, 44);
47         memset(buffer+48, 0, 0xbfffffff - (int)(buffer+48));
48 
49         // LD_* eraser
50         // 40 : extra space for memset function
51         memset(buffer-3000, 0, 3000-40);
52 }

```

가장 먼저 여태까지 대부분 argv로 입력값을 받고 있던 것을 stdin으로 받고 있다.
그리고 buffer+47에 있는 값, 즉 return address의 주소지 맨 앞부분이 \xbf이거나 \x08인지 체크하고 있다(20번째, 26번째줄).
또한 buffer + 44, buffer+45가 각각 \x90와 같지 않으면 while문을 돌게 하고 있다(33 ~ 34번째줄).
fgets는 stdin으로 입력을 받는다. 우선 입력받는 stdin이 어느 주소지에 위치해 있는지를 알아볼 필요가 있다고 생각했다.

![disas]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-19/0.png)

어떤 함수에 인자로 들어가는 값과 리턴되는 값은 eax를 통한다. fgets에 들어가기 전 eax에 마지막으로 담기는 값은 0x8049a3c에 들어있는 값이다(main+6).

![memory_stdin]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-19/1.png)

stdin값이 맞다. 그리고 해당 주소지에 들어있는 값은 0x401068c0이다. 이전의 문제들에서는 buffer+47의 값이 \x40와 같은지를 확인했었는데 이 문제에서는 확인하고 있지 않는 이유는 이를 활용하는 문제이기 때문일 것이라고 추측하였다. 다시한번 fgets가 끝나는 시점인 main+26에 breakpoint를 걸고 stdin에 입력값을 넣은 후 이의 주소지를 확인해 보았다.

![memory]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-19/2.png)

stdin에 반복적으로 나타나는 0x40015000 주소지를 확인해 보았다.

![memory2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-19/3.png)

stdin 입력값은 0x40015000에 들어있음을 확인하였다. 이제 main함수가 다 끝나고 leave-ret을 하기까지 stdin에 입력값이 남아있는지 확인해 보았다.

![memory3]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-19/4.png)

stdin에 값이 남아있음을 확인하였다. 이 위치에 쉘코드를 입력하면 공격이 성공할 것이다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-19/5.png)


my-pass: throw me away
