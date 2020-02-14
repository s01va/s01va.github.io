---
layout: single
title: "LOB 10번 (vampire -> skeleton)"
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

1  ﻿/*
2          The Lord of the BOF : The Fellowship of the BOF
3          - skeleton
4          - argv hunter
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
15         int i, saved_argc;
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
38         // argc saver
39         saved_argc = argc;
40 
41         strcpy(buffer, argv[1]);
42         printf("%s\n", buffer);
43 
44         // buffer hunter
45         memset(buffer, 0, 40);
46 
47         // ultra argv hunter!
48         for(i=0; i<saved_argc; i++)
49                 memset(argv[i], 0, strlen(argv[i]));
50 }

```

Stack frame structure:

| i[4] |
| saved_argc[4] |
| buffer[40] |
| Stack frame pointer |
| Return address |
| argc |
| argv |
| environ |


환경변수부터 buffer 40바이트, argv[0]까지 모두 0으로 초기화시키고 있다. 초기화가 이루어진 후 스택에 남아있는 부분이 있는지 gdb를 통해 알아보았다.

![disas]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/0.png)

(중략)

![disas2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/1.png)

main+368에서 leave하고 있다. 이 지점까지 실행시킨 후 스택에 남은 공간이 있는지의 여부를 보았다.

![stack mem]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/2.png)

(중략)

![stack mem2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/3.png)

메모리 끝에서 경로가 남아있는 부분을 찾았다. argv[0]부분이 이 주소지에 아직 남아있는 것을 발견하였다. B가 250번 반복되는 이름을 가진 디렉토리를 생성하고 실행파일 skeleton을 복사하여 위와 같은 실험을 반복하였다.

![mkdir]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/4.png)

![mem: argv[0]]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/5.png)

동일하게 메모리 끝쪽에 argv[0]이 남아있는 것을 발견하였다. 이것을 이용하여 다음과 같은 익스플로잇을 진행하였다.

![mkdir ln]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/6.png)

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-10/7.png)


my-pass: shellcoder
