---
layout: single
title: "LOB 1번 (gate -> gremlin)"
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
int main(int argc, char *argv[])
{
    char buffer[256];
    if(argc < 2){
        printf("argv error\n");
        exit(0);
    }
    strcpy(buffer, argv[1]);
    printf("%s\n", buffer);
}
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


![buffer addr]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/2.png)


buffer의 시작 주소가 0xbfff948임을 알 수 있다.
gdb에서 나와 원본 gremlin 파일로 BOF를 발생시킨다. buffer와 SFP가 총 260bytes이므로 nop로 200bytes, 쉘코드로 25bytes, 나머지 35bytes를 nop로 채운다. 그리고 return address에 buffer에서 쉘코드가 위치하기 전의 nop slide의 아무 지점의 주소를 넣어준다. 여기에서는 0xbfff950을 little endian을 감안해 삽입하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/3.png)

쉘을 획득한 모습을 확인할 수 있고, euid가 gremlin인 것을 확인하여 권한을 성공적으로 상승시켰음을 볼 수 있다.

![mypass]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/4.png)


my-pass: hello bof world


+ 또 다른 방법 1: 인자를 활용한다.
이는 프로그램이 인자의 개수를 검사하지 않기 때문에 가능하다. argv는 프로그램 시작과 동시에 가져오므로, gdb에서 main+3부분에 breakpoint를 걸고 python을 이용해 buffer, return address, argv[2]를 확인하기 위한 인자들을 입력한다.

![argv2 addr]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/5.png)

(중략)

![argv2 addr2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/6.png)

A(\x41)이 들어간 곳이 buffer + SFP, B(\x42)가 들어간 곳이 return address의 자리, 그리고 C(\x43)가 들어간 곳으로 argv[2]의 시작 주소가 0xbffffc06임을 알 수 있다. 이제 이를 통해 exploit을 진행한다. argv[1]에는 쓰레기 값으로 260bytes를 채우고 return address 자리에 argv[2]의 어떤 부분을 주소로 입력한다. 그리고 argv[2]는 앞부분을 어느정도 nop으로 채워준 후 쉘코드를 로드한다.

![exploit2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/7.png)


권한상승에 성공하였음을 볼 수 있다.



+ 또 다른 방법 2: 환경변수 활용
환경변수에 shellcode를 적재하고 return address에 이 환경변수의 주소지를 떨어뜨려 실행시키는 풀이도 가능하다.

![exploit3]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/8.png)

shellcode를 환경변수에 적재시킨 모습이다. 이후 환경변수 shellcode가 어느 주소에 위치하는지 확인하는 코드를 작성하였다.

![envaddr.c]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/9.png)

![envaddr]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/10.png)


환경변수 shellcode가 위치한 주소를 알아냈다. 이를 이용하여 공격을 진행하였다.

![exploit4]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-01/11.png)

