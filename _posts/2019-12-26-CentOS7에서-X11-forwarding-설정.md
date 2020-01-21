---
layout: single
title: "CentOS7에서 X11 forwarding 설정(X Window 설치)"
#description: ""
date: 2019-12-26 12:37:00 -0400
# modified: 
tags: 
- centos
- xwindow
- x11
comments: true
share: true
---

# 1. CentOS yum install xorg

CentOS에서 설치해야 할 패키지는 세가지이다.

```bash
yum install xorg-x11-apps.x86_64
yum install xorg-x11-xauth.x86_64
yum install xorg-x11-server-Xorg.x86_64
```

# 2. X11Forwarding yes

그리고 ```/etc/ssh/sshd_config```에서

```X11Forwarding yes``` 설정을 해준다.


# 3. Xming install

CentOS쪽으로 붙을 클라이언트 측(Windows)에서 [Xming을 설치](https://sourceforge.net/projects/xming/)해 준다.
기본설정대로 설치해 준다.

설치 이후 설정을 해 주어야 한다. Xming을 설치하면 XLaunch라는 것이 생긴다. 이걸 실행하면 아래같은 창이 뜬다.

![XLaunch]({{site.url}}{{site.baseurl}}/assets/images/2019-12-26-CentOS7-X11-forwarding/0.PNG)

계속 다음-다음-마침 눌러주면 된다.

그리고 Xming을 실행시켜 준다.


# 4. putty X11

putty를 실행하면 왼쪽 탭에서
Connection - SSH - X11에 들어가 Enable X11 forwarding에 체크해 준다.

![Enable X11]({{site.url}}{{site.baseurl}}/assets/images/2019-12-26-CentOS7-X11-forwarding/1.PNG)

세션에 저장해두면 편하다.


# 5. Test

![xclock]({{site.url}}{{site.baseurl}}/assets/images/2019-12-26-CentOS7-X11-forwarding/2.PNG)

xclock 명령어로 테스트할 수 있다.