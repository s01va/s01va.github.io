---
layout: single
title: "LOB 14번 (bugbear -> giant)"
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
3          - giant
4          - RTL2
5  */
6  
7  #include <stdio.h>
8  #include <stdlib.h>
9  #include <unistd.h>
10 
11 main(int argc, char *argv[])
12 {
13         char buffer[40];
14         FILE *fp;
15         char *lib_addr, *execve_offset, *execve_addr;
16         char *ret;
17 
18         if(argc < 2){
19                 printf("argv error\n");
20                 exit(0);
21         }
22 
23         // gain address of execve
24         fp = popen("/usr/bin/ldd /home/giant/assassin | /bin/grep libc | /bin/awk '{print $4}'", "r");
25         fgets(buffer, 255, fp);
26         sscanf(buffer, "(%x)", &lib_addr);
27         fclose(fp);
28 
29         fp = popen("/usr/bin/nm /lib/libc.so.6 | /bin/grep __execve | /bin/awk '{print $1}'", "r");
30         fgets(buffer, 255, fp);
31         sscanf(buffer, "%x", &execve_offset);
32         fclose(fp);
33 
34         execve_addr = lib_addr + (int)execve_offset;
35         // end
36 
37         memcpy(&ret, &(argv[1][44]), 4);
38         if(ret != execve_addr)
39         {
40                 printf("You must use execve!\n");
41                 exit(0);
42         }
43 
44         strcpy(buffer, argv[1]);
45         printf("%s\n", buffer);
46 }

```

Stack frame structure:

| buffer |
| SFP |
| RET |
| argc |
| argv |
| environ |

우선 길어진 소스코드 분석을 하자. argc가 2보다 작을 시 거르는 조건문과 argv[1]을 buffer로 복사하여 이를 사용하는 부분은 이전과 같다. argv[1]이 어떻게 처리되느냐를 중점적으로 보아야 한다.


```c

24         fp = popen("/usr/bin/ldd /home/giant/assassin | /bin/grep libc | /bin/awk '{print $4}'", "r");

```

24번째 줄이다. 명령어 ldd는 인자로 오는 프로그램이나 공유 라이브러리들이 요구하는 공유 라이브러리들을 출력해 준다. 
명령어 awk는 패턴 검색 및 처리 언어로, 위처럼 “... | /bin/awk ‘{print $4}’”라고 되어있으면 좌측에서 파이프로 넘어온 출력 중 네번째 필드값(주소값이 해당됨)만 출력한다.
즉 바이너리 파일인 assassin의 공유 라이브러리 중 libc 공유 라이브러리를 찾아 그의 주소값을 fp에 저장한다.

```c

25         fgets(buffer, 255, fp);
26         sscanf(buffer, "(%x)", &lib_addr);

```

24번째 줄에서 구한 assassin 파일이 의존하는 libc 공유라이브러리의 주소값을 buffer에 저장하고, 그 buffer를 16진수 형태로(%x) 포인터 execve_offset이 가리키는 곳에 저장한다.

```c

29         fp = popen("/usr/bin/nm /lib/libc.so.6 | /bin/grep __execve | /bin/awk '{print $1}'", "r");

```

명령어 nm은 인자로 오는 오브젝트 파일에 포함된 심볼들을 리스트화 시켜 보여준다.
/lib/libc.so.6에 포함된 심볼들을 리스트화 시킨 후 그 결과물 중에서 `__execve`가 포함된 것을 골라 그 첫번째 필드(주소값)를 fp에 저장하고 있다.

```c

30         fgets(buffer, 255, fp);
31         sscanf(buffer, "%x", &execve_offset);

```

30, 31번째 줄과 같은 동작을 하고 있다. libc의 execve함수의 주소를 execve_offset이 가리키는 곳에 저장한다.

```c

34         execve_addr = lib_addr + (int)execve_offset;
35         // end
36 
37         memcpy(&ret, &(argv[1][44]), 4);
38         if(ret != execve_addr)
39         {
40                 printf("You must use execve!\n");
41                 exit(0);
42         }

```

![p_execve]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/0.png)

![exploit_test]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/1.png)

여기서 주의해야 할 점이 있다. bash2에 \0a를 \00으로 인식하는 오류가 있어 위와 같이 입력하면 \x9d까지를 인자로 인식한다. `~~~` 부분을 아래와 같이 “”로 감싸주어야 한다.

![exploit_test2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/2.png)

“You must use execve!”가 뜨지 않는 것을 보아 무사히 execve의 주소값이 입력이 된 것을 알 수 있다.
execve 함수는 세 가지 인자를 갖는다.

```c

int execve (const char *filename, char *const argv [], char *const envp[]);

```

/bin/sh을 실행시키기 위해서 아래와 같이 인자가 들어가야 할 것이다.

```c

execve(“/bin/sh”, {“/bin/sh”, NULL}, NULL);

```

문제는 execve의 두번째 인자값으로 오는 {“/bin/sh”, NULL}을 어떻게 처리하느냐이다. 이를 확인하기 위해 다음과 같은 프로그램을 작성하고 이를 gdb로 확인해 보았다.

![testargv.c]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/3.png)

![gdb]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/4.png)

보통 함수가 실행되기 직전에 인자를 eax로 받으므로 bp를 0x80483eb에 걸고 이 때의 eax를 조사해 보았다.

![memory]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/5.png)

eax는 0xbffffb00이라는 주소지를 담고 있으며, 이 주소지는 다시 0x80484a0이라는 주소지를 담고 있고, 0x80484a0으로 가야 비로소 문자열들을 발견할 수 있다. 이번에는 tmp[1]의 “BBBBBBBB” 대신 NULL을 넣고 위의 과정을 반복해 보았다.

![testargv.c_2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/6.png)

![testargv]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/7.png)

![memory2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/8.png)

gdb에서 0x80484a8자리가 null이기 때문에 gdb에서는 문자열로 잡지 못하나, 위에서 프로그램을 실행시켰을 시 null이라고 뜨는 것을 보아 프로그램은 null을 분명히 인식하는 것을 알 수 있다. 쉘코드를 환경변수로 준 후, 주소지를 확인해 보았다.

![printenv]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/9.png)

![memory3]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/10.png)

“/bin/sh”이라는 문자열이 막 끝나는 지점인 0xbffffef6이 NULL인 것을 볼 수 있다. 이제 execve함수의 두번째 인자({“/bin/sh”, NULL})의 NULL은 따로 주지 않아도 되며, “/bin/sh”을 담고 있는 주소지인 0xbffffeef를 가리키는 주소지를 따로 만들어서 이를 execve함수의 두번째 인자로 넘겨주면 된다는 결론을 내릴 수 있다.
하지만 여기에는 한가지 문제가 있다. 이전의 문제에서 확인했듯 우리는 예측했던 주소지를 넣고 공격을 시도했을 시, 종종 예상했던 주소지가 맞지 않았던 경험을 하였다. 만약 “/bin/sh”의 문자열을 어딘가에 넣고, 그 주소지를 가리키는 또다른 환경변수 등을 지정했을 시, 예상했던 “/bin/sh”이 미묘하게 다른 곳에 있을 수도 있고, 여기에 맞추어 “/bin/sh”의 주소지를 가리키던 환경변수까지 바꾸어 주어야 할 것이다. 브루트 포스 코드를 짜서 공격하는 방법도 있겠지만, 조금 더 실패할 가능성이 적은 쉬운 아이디어를 떠올렸다.

| NULL |
| “/bin/sh” |
| exit |
| system |
| execve |

execve를 호출하자마자 exit함수를 인자로 넣어 종료시킨 후, 바로 system함수를 호출하여 이전의 darkknight문제를 풀었듯 system으로 하여금 “/bin/sh”을 실행시키게 하는 방법이다. 
이미 구한 execve함수의 주소(0x400a9d48), 이전 문제에서 찾은 system 함수의 주소(0x40058ae0), system 함수 내에 존재하는 “/bin/sh” 문자열의 주소(0x400fbff9), 메모리에 끝자락에 항상 NULL로 존재하는 주소지(0xbffffffc) 등을 알고 있다. exit함수의 주소를 찾았다.

![p_exit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/11.png)

exit 함수의 주소는 0x40039130이다. 이 정보들을 취합하여 공격을 시도하였다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-14/12.png)


my-pass: one step closer