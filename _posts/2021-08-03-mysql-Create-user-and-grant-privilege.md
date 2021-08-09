---
layout: single
title: "mysql 초기세팅 중 신규 user 생성 및 권한 할당"
description: ""
date: 2021-08-03 13:20:00 -0400
# modified: 
tags:
- mysql
- mariadb
comments: true
share: true

---



최초 설치 후 설정 시 필요했던 과정들 중 신규 user 생성 및 권한 과정



1. root에게 권한을 할당하는 권한 주기

   ```mysql
   create user 'root'@'localhost';
   # 패스워드 변경 시: create user 'root'@'localhost' identified by '[password]';
   grant all privileges on *.* to 'root'@'localhost' with grant option;
   flush privileges;
   ```

   

2. 신규 user 생성 및 권한 할당

   ```mysql
   create user '[newuser]'@'[specific IP]';
   # 패스워드 변경 시: create user '[newuser]'@'[specific IP]' identified by '[newuser_pw]';
   
   # create database [DBname] default character set utf8;
   grant all privileges on [DBname].[tablename] to '[newuser]'@'[specific IP]';
   flush privileges;
   ```

   

- `flush privileges;`까지 해야 적용된다.
- `'[specific IP]'` 대신 모든 IP로 권한을 열어주고 싶을 경우 `'%'` 입력

