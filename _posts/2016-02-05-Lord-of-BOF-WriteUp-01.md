---
layout: single
title: "LOB gate -> gremlin"
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

1  int main(int argc, char *argv[])
2  {
3      char buffer[256];
4      if(argc < 2){
5          printf("argv error\n");
6          exit(0);
7      }
8      strcpy(buffer, argv[1]);
9      printf("%s\n", buffer);
10 }


```

Stack frame structure:

| buffer[256] |
| Stack Frame Pointer[4] |
| Return address[4] |
| argc |
| argv |
| environ |


쉘코드를 삽입하기 위해서 몇 가지 방법을 생각해 낼 수 있다.
첫째, 변수 buffer를 활용한다. 입력값의 크기를 검사하지 않는 strcpy의 특성을 이용하여, buffer에 쉘코드를 넣고 buffer와 SFP를 넘치게 하여 return address에 쉘코드가 실행되는 buffer의 주소를 계산하여 삽입하는 계획을 세운다.
실행파일 gremlin은 소유주가 gremlin이므로 gate인 사용자는 디버깅을 할 수 없다. gate 소유의 디렉토리를 생성한 후 gremlin을 복사해 온 후 디버깅을 진행하도록 한다. 


![cp]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/0.png)


gdb로 gremlin의 어셈블리어를 확인한다.


![gdb disas main]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/1.png)


buffer에 값을 넣는 strcpy 이후인 main+59에 breadpoint를 걸어준 후, 임의의 입력값을 넣어 buffer의 시작 주소를 파악한다.


![mem]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/2.png)


buffer의 시작 주소가 0xbfff948임을 알 수 있다.
gdb에서 나와 원본 gremlin 파일로 BOF를 발생시킨다. buffer와 SFP가 총 260bytes이므로 nop로 200bytes, 쉘코드로 25bytes, 나머지 35bytes를 nop로 채운다. 그리고 return address에 buffer에서 쉘코드가 위치하기 전의 nop slide의 아무 지점의 주소를 넣어준다. 여기에서는 0xbfff950을 little endian을 감안해 삽입하였다.

