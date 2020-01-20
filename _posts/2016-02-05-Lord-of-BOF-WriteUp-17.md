---
layout: single
title: "LOB zombie_assassin -> succubus"
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

1  /*
2          The Lord of the BOF : The Fellowship of the BOF
3          - succubus
4          - calling functions continuously
5  */
6  
7  #include <stdio.h>
8  #include <stdlib.h>
9  #include <dumpcode.h>
10 
11 // the inspector
12 int check = 0;
13 
14 void MO(char *cmd)
15 {
16         if(check != 4)
17                 exit(0);
18 
19         printf("welcome to the MO!\n");
20 
21         // olleh!
22         system(cmd);
23 }
24 
25 void YUT(void)
26 {
27         if(check != 3)
28                 exit(0);
29 
30         printf("welcome to the YUT!\n");
31         check = 4;
32 }
33 
34 void GUL(void)
35 {
36         if(check != 2)
37                 exit(0);
38 
39         printf("welcome to the GUL!\n");
40         check = 3;
41 }
42 
43 void GYE(void)
44 {
45         if(check != 1)
46                 exit(0);
47 
48         printf("welcome to the GYE!\n");
49         check = 2;
50 }
51 
52 void DO(void)
53 {
54         printf("welcome to the DO!\n");
55         check = 1;
56 }
57 
58 main(int argc, char *argv[])
59 {
60         char buffer[40];
61         char *addr;
62 
63         if(argc < 2){
64                 printf("argv error\n");
65                 exit(0);
66         }
67 
68         // you cannot use library
69         if(strchr(argv[1], '\x40')){
70                 printf("You cannot use library\n");
71                 exit(0);
72         }
73 
74         // check address
75         addr = (char *)&DO;
76         if(memcmp(argv[1]+44, &addr, 4) != 0){
77                 printf("You must fall in love with DO\n");
78                 exit(0);
79         }
80 
81         // overflow!
82         strcpy(buffer, argv[1]);
83         printf("%s\n", buffer);
84 
85         // stack destroyer
86         // 100 : extra space for copied argv[1]
87         memset(buffer, 0, 44);
88         memset(buffer+48+100, 0, 0xbfffffff - (int)(buffer+48+100));
89 
90         // LD_* eraser
91         // 40 : extra space for memset function
92         memset(buffer-3000, 0, 3000-40);
93 }

```

우선 76번째 줄의 조건을 반드시 충족시켜야 한다. argv[1]+44의 주소를 addr에 들어있는 값인 DO함수의 주소와 일치시켜야 한다.

![disas_DO]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/0.png)

DO함수의 시작지점은 0x80487ec이다. 해당 조건문을 우회하는지 다음을 통해 알아보았다.

![succubus1]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/1.png)

성공적으로 우회하였다. 이 상태에서 쉘을 띄우는 가장 좋은 방법은 system 함수를 포함하고 있는 MO함수를 활용하는 것으로 보인다. 하지만 MO 함수를 포함한 모든 함수에 check 조건문을 우회시키기 위해 다음과 같이 함수 주소를 쌓는다.

| buffer[40] |
| SFP |
| DO address |
| GYE address |
| GUL address |
| YUT address |
| MO address |
| ... |

이러한 스택은 다음과 같은 과정을 거쳐 만들어지게 된다. 만약 페이로드를 패딩 44byte + DO함수 주소로만 설정하게 되면 이러한 과정을 거친다.

| buffer[40] |
| SFP |
| DO address |
| ... |

DO 함수를 실행시킨 후에는 이렇게 바뀌게 된다.

| buffer[40] |
| SFP |
| SFP |
| ... |

DO 함수가 끝난 후에는 SFP 다음 내용이 eip에 들어가게 된다.

| buffer[40] |
| SFP |
| DO address |
| GYE address |
| GUL address |
| YUT address |
| MO address |
| ... |

그렇기 때문에 위와 같은 스택을 구성하는 것이다.
함수의 주소들은 gdb에서 ‘disas [함수명]’ 명령어로도 찾을 수 있지만 다른 방법으로도 찾을 수 있다.

- nm: 파일 심볼 검색
- readelf: ELF 파일에 대한 정보를 보여줌

nm 명령어를 통해 필요한 모든 함수의 주소지를 찾았다.

![nm_succubus]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/2.png)

이를 활용해 보았다.

![succubus2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/3.png)

이제 MO 함수에 인자로 shell을 주면 된다.

![disas_MO]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/4.png)

![memory]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/5.png)

![memory2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/6.png)

/bin/sh 문자열의 주소를 알아내었다. 이 주소를 이용해 보았으나 잘 되지 않아 근처의 주소지를 써서 공격에 성공하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-17/7.png)


my-pass: here to stay
