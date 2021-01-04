---
layout: single
title: "repository 생성 후 git 초기세팅"
description: "자주 까먹어서 나를 위해 남겨둠"
date: 2020-12-29 13:37:00 -0400
# modified: 
tags:
- git
- troubleshooting
comments: true
share: true
---

for Windows 사용자

git repository  생성 이후

1. Repository 생성 직후 git이 안내하는 명령어 

   ![00](https://s01va.github.io/assets/images/2020-12-29-Git-Initiating/0.PNG)

   git으로 관리할 소스 or 문서들이 있는 곳의 홈 디렉토리로 이동 후 명령어 입력

   나는 아래와 같은 루틴으로 자주 사용한다.

   ```bash
   git init
   git config --global user.name “username”
   git config --global user.email "user@email.com"
   git remote add origin git@github.com:username/repository.git
   git config remote.origin.url git@github.com:username/repository.git
   echo "# test" >> README.md
   git add README.md
   git commit -m "first commit"
   git branch -M main
   git push -u origin main
   ```

   

2. 자동 로그인을 위한 ssh키 설정

   (git 계정당 1회만 해두면 된다)

   1. git bash를 열고 아래와 같이 입력한다.

      ```bash
      ssh-keygen -t rsa -b 4096 -C "user@email.com"
      ```

   2. 이후 암호 설정까지 해 준다.

      그러면 `%USERPROFILE%\.ssh` 경로에 파일들이 생성된다.

   3. 본인 git 웹페이지에서 ssh key 설정

      접속 후 오른쪽 상단 Settings 선택

      ![01](https://s01va.github.io/assets/images/2020-12-29-Git-Initiating/1.PNG)

      좌측 메뉴 중 SSH and GPG keys 선택

      ![02](https://s01va.github.io/assets/images/2020-12-29-Git-Initiating/2.PNG)

      New SSH key 클릭 후 `%USERPROFILE%\.ssh` 경로의 `id_rsa.pub`파일 내용 전부를 복사해서 붙여넣기한다.

   - 기존 Repository에서 자동로그인이 안될 경우:

     해당 Repository에서 다음과 같은 명령어를 입력한다.

     (해당 Repository에 맞는 git clone(ssh)를 찾아 입력해야 함)

     ```bash
     git config remote.origin.url git@github.com:username/repository.git
     ```

   해두면 앞으로 push할 때 2에서 설정한 암호만 입력하면 된다.

