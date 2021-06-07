---
layout: single
title: "로그파일 정리 커맨드"
description: "리눅스/윈도우 로그파일 정기삭제 명령어"
date: 2021-05-14 13:00:00 -0400
# modified: 
tags:
- script
- cheatingsheet
comments: true
share: true
---

리눅스/윈도우 로그파일 정기삭제 명령어

가장 자주 사용하는 커맨드

- Linux

  ```bash
  find [path] -name *.log* -mtime +90 -exec rm {} \;
  find [path] -name *.log* -mtime +7 ! -name *.gz -exec gzip {} \;
  ```

  1. `[path]`에서 파일명이 `*.log*`이며 마지막 수정한 일자가 90일 이상일 시 find 결과물을 삭제

  2. `[path]`에서 파일명이 `*.log*`이며 마지막 수정한 일자가 7일 이상이지만 파일명에 `*.gz`가 없을 시 find 결과물을 모두 gzip

     

  위 내용으로 `.sh` 파일 만들어서 crontab 처리함

- Windows

  ```powershell
  forfiles /p "[path]" /m [pattern] /d -30 /c "cmd /c del @path"
  ```

  `[path]` 내에 `[pattern]`에 해당되는 파일명을 찾아 30일 이상 된 파일에 대해 `cmd /c del @path`를 실행한다.

  `[pattern]`의 예시: `*.log*`



