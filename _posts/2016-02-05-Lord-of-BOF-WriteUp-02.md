---
layout: single
title: "LOB gremlin -> cobolt"
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
3          - cobolt
4          - small buffer
5  */
6  
7  int main(int argc, char *argv[])
8  {
9      char buffer[16];
10     if(argc < 2){
11         printf("argv error\n");
12         exit(0);
13     }
14     strcpy(buffer, argv[1]);
15     printf("%s\n", buffer);
16 }


```

stack frame structure:

| buffer[16] |
| Stack Frame Pointer[4] |
| Return Address[4] |
| argc |
| argv |
| environ |

이제 앞서 사용했던 직접 buffer에 삽입하는 방법은 사용할 수 없음을 알 수 있다. 쉘코드의 크기가 buffer의 크기를 넘어버리기 때문이다. 그렇기 때문에 argument를 활용하는 방식으로 권한 상승을 시도한다. gremlin의 경우처럼 디버깅을 가능하게 하기 위해 gremlin 소유의 디렉토리를 생성한 후 cobolt 실행파일을 복사한 후 디버깅을 진행한다. 다음은 gdb로 확인한 cobolt의 어셈블리어 코드이다. 

![disas]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-02/0.png)

앞과 동일하게 main+3에 breakpoint를 걸어준 후 두 개의 argument를 python으로 입력하여 buffer의 주소와 argv[2]의 주소를 찾도록 한다.

![argv addr1]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-02/1.png)

(중략)

![argv addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-02/2.png)

argv[2]의 시작 주소가 0xbffffc01인 것을 알 수 있다. 이제 원본 cobolt에서 gremlin의 경우와 같이 exploit을 진행한다.

![argv addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-02/3.png)

![argv addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-02/4.png)


my-pass: hacking exposed