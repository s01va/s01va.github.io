---
layout: single
title: "git 명령어 cheating sheat"
description: "자주 까먹어서 나를 위해 남겨둠"
date: 2021-05-12 11:00:00 -0400
# modified: 
tags:
- git
comments: true
share: true
---



## git 확인

git 명령어 cheating sheat



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

- 파일을 untracked 상태에서 track 상태로 전환(add)

  ```bash
  git add [file_name]
  ```

- commit

  ```bash
  git commit -m "[commit_message]"
  ```

- push

  ```bash
  git push
  ```

파일 수정 후 반영 시에도 위와 같은 과정을 동일하게 거쳐야 함

(마지막 커밋 이후 untracked 상태가 됨)

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

  

