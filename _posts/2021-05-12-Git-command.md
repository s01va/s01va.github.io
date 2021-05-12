---
layout: single
title: "git 명령어 cheating sheat"
description: "자주 까먹어서 나를 위해 남겨둠"
date: 2020-12-29 13:37:00 -0400
# modified: 
tags:
- git
comments: true
share: true
---



## git 확인



## 일반 확인

- 일반 상태확인

  ```bash
  git status
  ```

- 로그 확인

  ```bash
  git log
  ```

- branch graph 확인

  ```bash
  git log --graph
  ```

---------------------------

## commit-push

- dd

  ```bash
  git add [file_name]
  ```

- dd

  ```bash
  git commit -m "[commit_message]"
  ```

- dd

  ```bash
  git push
  ```

  

-------------------------------

## Branch 관련

- Branch 확인

  ```bash
  git branch
  git branch -a
  ```

- Branch 생성

  ```bash
  git branch [branch_name]
  ```

- Branch 삭제

  ```bash
  git branch -d [branch_name]
  ```

- 잡고 있는 Branch 바꾸기

  ```bash
  git checkout [branch_name]
  ```

- Branch 합치기

  ```bash
  git merge [bransh_name]
  ```

  

