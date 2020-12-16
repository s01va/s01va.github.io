---
layout: single
title: "LOB 17번 (zombie_assassin -> succubus)"
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
        - succubus
        - calling functions continuously
*/

#include <stdio.h>
#include <stdlib.h>
#include <dumpcode.h>

// the inspector
int check = 0;

void MO(char *cmd)
{
        if(check != 4)
                exit(0);

        printf("welcome to the MO!\n");

        // olleh!
        system(cmd);
}

void YUT(void)
{
        if(check != 3)
                exit(0);

        printf("welcome to the YUT!\n");
        check = 4;
}

void GUL(void)
{
        if(check != 2)
                exit(0);

        printf("welcome to the GUL!\n");
        check = 3;
}

void GYE(void)
{
        if(check != 1)
                exit(0);

        printf("welcome to the GYE!\n");
        check = 2;
}

void DO(void)
{
        printf("welcome to the DO!\n");
        check = 1;
}

main(int argc, char *argv[])
{
        char buffer[40];
        char *addr;

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        // you cannot use library
        if(strchr(argv[1], '\x40')){
                printf("You cannot use library\n");
                exit(0);
        }

        // check address
        addr = (char *)&DO;
        if(memcmp(argv[1]+44, &addr, 4) != 0){
                printf("You must fall in love with DO\n");
                exit(0);
        }

        // overflow!
        strcpy(buffer, argv[1]);
        printf("%s\n", buffer);

        // stack destroyer
        // 100 : extra space for copied argv[1]
        memset(buffer, 0, 44);
        memset(buffer+48+100, 0, 0xbfffffff - (int)(buffer+48+100));

        // LD_* eraser
        // 40 : extra space for memset function
        memset(buffer-3000, 0, 3000-40);
}
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
