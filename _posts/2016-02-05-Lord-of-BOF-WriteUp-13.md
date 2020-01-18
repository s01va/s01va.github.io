---
layout: single
title: "LOB darkknight -> bugbear"
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
3          - bugbear
4          - RTL1
5  */
6  
7  #include <stdio.h>
8  #include <stdlib.h>
9  
10 main(int argc, char *argv[])
11 {
12         char buffer[40];
13         int i;
14 
15         if(argc < 2){
16                 printf("argv error\n");
17                 exit(0);
18         }
19 
20         if(argv[1][47] == '\xbf')
21         {
22                 printf("stack betrayed you!!\n");
23                 exit(0);
24         }
25 
26         strcpy(buffer, argv[1]);
27         printf("%s\n", buffer);
28 }

```

Stack frame structure:

| i[4] |
| buffer[40] |
| SFP |
| RET |
| argc |
| argv |
| environ |

두번째 if문에 argv[1][47] == ‘/xbf’일 시 프로그램을 종료하게 함으로써 스택에 오버플로우 시키는 방법을 사용하지 못하게 하고 있다. 문제에서 RTL을 힌트로 주었으니 이를 활용해 보려 한다.

앞의 LD_PRELOAD를 이용하는 skeleton 문제에서 라이브러리 관련 설명과 함께 풀이를 한 바 있다. RTL은 Return To Library로, 링킹된 라이브러리의 또다른 함수로 리턴시켜 실행시키는 기법이다. 쉘을 실행시키는 것이 목적인데, 가장 쉬운 방법으로 system(“/bin/sh”)가 있다. argument로 “/bin/sh”를 주고, ret 자리에 system함수의 주소를 준 후, 크기가 4만큼의 패딩을 준 후 해당 함수의 인자로 들어가야 할 “/bin/sh”의 주소를 줄 것이다. 보통 함수의 인자가 ebp+4의 자리에 위치하기 때문이다. 

![disas]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/0.png)

인자로 준 “A” * 44는 buffer의 패딩, “BBBB”는 ret에 넣을 system 함수의 주소 자리, “CCCC”는 인자를 주기 전의 패딩이며 “DDDD”는 “/bin/sh”문자열의 주소 자리이다. system 함수의 주소는 0x40058ae0이므로 argv[1][47]==’/xbf’의 조건문에도 걸리지 않을 것이다.

![memory1]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/1.png)

(중략)

![memory2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/2.png)

![memory3]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/3.png)

“/bin/sh” 문자열이 시작하는 지점은 0xbffffc44이다. 이를 바탕으로 공격을 진행하였다.

![exploit1]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/4.png)

공격에 실패하였으나 경로명이 보이는 것을 보아 “/bin/sh” 문자열이 bugbear의 복사본 파일에서는 0xbffffc44에 위치하였으나, 원본 파일에서 0xbffffc44는 “/bin/sh”의 약간 뒤에 위치하고 있음을 추측해 낼 수 있었다.

![exploit2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/5.png)

“/bin/sh”의 주소지를 0xbffffc3a로 설정하니 공격에 성공하였다.

![mypass]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/6.png)


my-pass: new divide


+ system 함수에 “/bin/sh”이라는 문자열이 이미 포함되어 있다는 것을 알게 되었다.
 문자열을 찾기 위해 아래와 같은 코드를 작성하였다.

```c

1  #include <stdio.h>
2  
3  int main(){
4          long fsystem = 0x400391e0;
5          long shell = fsystem;
6  
7          while (memcmp((void *)shell, "/bin/sh", 8)){
8                  shell++;
9          }
10 
11         printf("/bin/sh = 0x%x\n", shell);
12 
13         return 0;
14 }

```

![ps]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-13/7.png)


system함수 내에서 “/bin/sh”이라는 문자열이 있는 주소는 0x400fbff9이다.

