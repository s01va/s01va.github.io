---
layout: single
title: "Git: RPC failed 해결방법"
description: ""
date: 2022-06-23 12:00:00 -0400
# modified: 
tags: 
- git
- troubleshooting
- wsl
comments: true
share: true
toc_sticky: true

---



vscode를 wsl 터미널로 사용하면서 git pull을 받을 때 발생하는 문제

![0](https://s01va.github.io/assets/images/2022-06-23-RPC-failed-해결/0.PNG)

mtu 값을 조정해주면 해결된다.



wsl에서 default mtu 값: 1500

![1](https://s01va.github.io/assets/images/2022-06-23-RPC-failed-해결/1.PNG)



1000 정도로 줄여준다.

```bash
sudo ifconfig eth0 mtu 1000
```



