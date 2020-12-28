---
layout: single
title: "Ansible 설치 with troubleshooting"
description:
date: 2020-04-11 12:37:00 -0400
# modified: 
tags: 
- centos
- devops
- ansible
- docker
comments: true
share: true
---

참고한 곳:

[프로비저닝 자동화를 위한 Ansible AWX, 설치부터 엔터프라이즈 환경 적용까지 – 1](https://engineering.linecorp.com/ko/blog/ansible-awx-for-provisioning-1/)

[간단한 AWX 설치 및 기본 사용방법](https://tech.osci.kr/2019/05/24/77138487/)


위와 같이 설치하다 보면 특정 오류에 직면하게 된다.

`ansible-playbook -i inventory install.yml` 이후

![failed=1](https://s01va.github.io/assets/images/2020-04-11-Install-Ansible-with-troubleshooting/0.PNG)

docker관련 python 모듈 사이에 충돌이 나는 듯 하다.

아래의 명령어로 해결한다.

```sh
pip uninstall docker docker-py docker-compose
pip install docker-compose --ignore-installed
```

![failed=0](https://s01va.github.io/assets/images/2020-04-11-Install-Ansible-with-troubleshooting/1.PNG)

