---
layout: single
title: "iptables port forwarding"
description: "for me"
date: 2020-03-08 17:30:00 -0400
# modified: 
tags: 
- iptables
- port-forwarding
comments: true
share: true
---

iptables를 쉽게 사용하기 위한 도구들이 생겼지만

불가피하게 iptables를 통해서 설정해야 할 일이 종종 생겨 왔다.

iptables로 포트포워딩 하는 방법:


1. 포트를 열어준다.

(filter 테이블의 INPUT, OUTPUT 체인에 규칙을 추가시킴)

```bash
sudo iptables -I INPUT -p tcp --dport [PORT_NUM] -j ACCEPT
sudo iptables -I OUTPUT -p tcp --dport [PORT_NUM] -j ACCEPT
```


2. FORWARD 체인에 규칙을 추가시킨다.

(NAT의 규칙 이전에 FORWARD 체인을 먼저 통과하기 때문)

```bash
sudo iptables -I FORWARD -p tcp --dport [PORT_NUM] -d [DESTINATION_IP] -j ACCEPT
```


3. NAT 테이블의 PREROUTING 체인에 규칙을 추가시킨다.

```bash
sudo iptables -t nat -A PREROUTING -p tcp --dport [PORT_NUM] -j DNAT --to [DESTINATION_IP:PORT]
```

