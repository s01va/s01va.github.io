---
layout: single
title: "LOB 18번 (succubus -> nightmare)"
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
/*
        The Lord of the BOF : The Fellowship of the BOF
        - nightmare
        - PLT
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dumpcode.h>

main(int argc, char *argv[])
{
        char buffer[40];
        char *addr;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        // check address
        addr = (char *)&strcpy;
        if(memcmp(argv[1]+44, &addr, 4) != 0){
                printf("You must fall in love with strcpy()\n");
                exit(0);
        }

        // overflow!
        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // dangerous waterfall
        memset(buffer+40+8, 'A', 4);
}
```

우선 24번째 줄의 조건문을 우회해야 하기 때문에 이전 문제에서 ret를 DO 함수로 덮어씌웠듯이 strcpy 함수의 주소를 찾아 ret를 채울 것이다.

![readelf](https://s01va.github.io/assets/images/2016-02-05-LOB-18/0.png)

![run_nightmare](https://s01va.github.io/assets/images/2016-02-05-LOB-18/1.png)

우회에 성공하였다(You must fall in love with strcpy()이라는 문구가 뜨지 않음).
소스코드에 따르면 원래 스택은 아래와 같이 구성될 것이다.

| buffer[40] | SFP[4] | Ret[4] | AAAA[4] | ... |

이를 strcpy 함수로 ret를 우회하면 아래와 같이 구성될 것이다.

| A * 44 | strcpy (0x08048410) | AAAA | ... |

strcpy 뒤에 memset으로 인해 만들어지는 AAAA는 strcpy가 호출된 이후 돌아오는 ret가함수된다. 그리고 함수의 인자가 어떤 방식으로 삽입되는지는 이전에 execve를 조작하면서 알아본 바 있다(bugbear -> giant 문제). 아래는 이를 확인하기 위해 BBBB와 CCCC를 추가적으로 삽입해 보는 과정이다.

![disas](https://s01va.github.io/assets/images/2016-02-05-LOB-18/2.png)

leave 부분에 breakpoint를 걸고 다음과 같은 페이로드를 만들어 삽입해 보았다.

![r](https://s01va.github.io/assets/images/2016-02-05-LOB-18/3.png)

src, dest를 마음대로 조작할 수 있다는 것을 알 수 있다.

| A * 44 | strcpy(0x08048410) | \x90\x90\x90\x90 | BBBB | CCCC | ... |

쉘코드를 환경변수로 만들었다.

![export](https://s01va.github.io/assets/images/2016-02-05-LOB-18/4.png)

leave 하는 지점에 breakpoint를 만든 후, strcpy의 ret, strcpy의 인자가 어느 주소에 위치하는지를 확인하였다.

![memory](https://s01va.github.io/assets/images/2016-02-05-LOB-18/5.png)

또한 환경변수가 위치하는 주소를 알아보았다.

![memory_env](https://s01va.github.io/assets/images/2016-02-05-LOB-18/6.png)

 환경변수로 입력해둔 쉘코드의 위치는 0xbfffff60임을 확인하였다. 이 주소를 다시한번 환경변수로 만들어 두었다.

![export2](https://s01va.github.io/assets/images/2016-02-05-LOB-18/7.png)

쉘코드의 주소를 입력한 환경변수의 주소를 확인하였다.

![memory_env2](https://s01va.github.io/assets/images/2016-02-05-LOB-18/8.png)

![memory](https://s01va.github.io/assets/images/2016-02-05-LOB-18/9.png)

쉘코드의 주소는 0xbfffff60, 쉘코드의 주소가 입력된 주소는 0xbffffca2이다. 이것들을 가지고 공격을 시도해 보았다.

![exploit](https://s01va.github.io/assets/images/2016-02-05-LOB-18/10.png)

| A * 44 | strcpy | AAAA | 0xbffffa90 | 0xbffffca2 | ... |
| --- | --- | --- |
| dummy |  | Strcpy의 ret | Strcpy의 dest | Strcpy의 src |  |

쉘코드의 주소가 입력되어있는 주소를 strcpy가 실행된 후 돌아오는 return address(AAAA)의 위치인 0xbffffa90에 입력하겠다는 의미이다. 하지만 seg fault가 발생하여 core dump를 분석해 보았다. 

![memory2](https://s01va.github.io/assets/images/2016-02-05-LOB-18/11.png)

strcpy의 ret의 위치가 0xbffffa90에서 0xbffffa80으로 바뀌어 있음을 알 수 있다. 환경변수의 주소지들도 바뀌어 있을 것을 우려하여 다시한번 확인해 보았다.

![memory_env3](https://s01va.github.io/assets/images/2016-02-05-LOB-18/12.png)

쉘코드의 위치가 0xbfffff60에서 0xbfffff65로 바뀌어 있는 것을 확인하였다.

![memory_env4](https://s01va.github.io/assets/images/2016-02-05-LOB-18/13.png)

쉘코드의 주소를 입력해둔 환경변수 shelladdr의 위치 또한 0xbffffca2에서 0xbffffc91로 바뀌어 있다. 이를 다시 입력하고 바뀐 주소지로 공격을 시도해 보았다.

![exploit2](https://s01va.github.io/assets/images/2016-02-05-LOB-18/14.png)

잘 적용되는 것을 확인할 수 있다. 현재의 위치에서 원본 실행파일 nightmare에 공격을 하기 위해 심볼릭 링크를 생성한 후 그대로 공격을 시도하였다.

![exploit3](https://s01va.github.io/assets/images/2016-02-05-LOB-18/15.png)


my-pass: beg for me
