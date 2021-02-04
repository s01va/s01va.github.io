---
layout: single
title: "AWS 접속설정"
description:
date: 2021-01-29 10:17:00 -0400
# modified: 
tags:
- aws
- putty
comments: true
share: true
---

1. AWS 인스턴스 생성 시 만든 .pem 파일을 저장한다.
2. putty, puttygen [다운로드](https://www.puttygen.com/download-puttyputtygen )
3. 실행
4. Load
   ![0](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/0.png)
5. 파일 형식 ‘All Files’ 설정 후 다운로드해서 저장해 둔 .pem파일 선택
   ![1](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/1.png)
6. 확인
   ![2](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/2.png)
7. 'Save private key' 선택
   ![3](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/3.png)
8. 패스워드를 따로 설정하지 않는지 물어본다.
   만들고 싶으면 Key passphrase/Coonfirm passphrase 폼을 채워 제출한다.
   그래도 예를 누르면 패스워드를 따로 설정하지 않는다.
   ![4](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/4.png)
9. 저장해준다. 파일명은 아무거나 상관없음
   ![5](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/5.png)
10. private 키 설정이 끝났으니 puttygen은 종료해도 된다.
    서버와의 연결을 위해 putty를 실행한다.
11. 접속할 ip, port를 지정 후 왼쪽 카테고리에서 다음 경로로 들어간다.
    Connection > SSH > Auth 선택 후 Private key file for authentication > Browse
    ![6](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/6.png)
12. 방금 생성한 private key를 넣어준다.
    ![7](https://s01va.github.io/assets/images/2021-01-28-AWS-access-setting/7.png)
13. 이후 Session 카테고리로 돌아가 위의 설정을 모두 저장한다.



- 최초접속시 User name
  Ubuntu의 경우: ubuntu
  Red hat의 경우: ec2-user



