---
layout: post
title: "Windows Batch file 만들기"
description:
date: 2019-11-14 10:30:00 -0400
# modified: 
tags: 
- Windows
- cmd
- Batchfile
- Script
comments: true
share: true
---


자주 쓰이는 Batch shell 키워드 리스트:
- @ECHO off
- title
- set
- @REM
- %[SOMEVAR]%
- 2>&1
- start
- move
- 각종 strip


### @ECHO off

명령어의 복창을 방지한다. 배치파일 내에 여러가지 명령어들을 저장해 두었을 시, 그 명령어들의 결과만을 출력한다.


### title

배치파일이 실행되는 cmd 창의 제목을 지정한다.


### @REM

주석 처리. C계열 언어의 '//'나 파이썬의 '#'에 준함


### set

변수 설정.
ex) set VAR=15


### %[SOMEVAR]%

환경변수 또는 현재 batch파일 내에서 지정한 변수 불러오기


### 2>&1

2는 stderr, 1은 stdout이다. standard error를 standard output으로 돌리는 것.


### start

실행파일 실행.
자주쓰는 옵션 \b: 새 Window에서 실행하지 않고 현재 Window에서 바로 실행


### move

파일 이동 또는 파일이름 변경
move [원본] [변경후]


### 각종 strip

```
@ECHO OFF
set PREFIX=%DATE%
move log.txt log%PREFIX%.txt
```
![cmd batch 0](https://github.com/s01va/s01va.github.io/blob/master/_posts/2019-11-18-Windows-Batch-file/0.PNG)

![logfile1](https://github.com/s01va/s01va.github.io/blob/master/_posts/2019-11-18-Windows-Batch-file/1.PNG)

:~[number]
[number]~끝까지를 지정한다.
이미 생성해 놓은 log.txt파일의 이름을 변경하는 것으로 실험하였다.

```
@ECHO OFF
set PREFIX=%DATE%
@REM move log.txt log%PREFIX%.txt
set PREFIX2=%PREFIX:~2%
move log%PREFIX%.txt log%PREFIX2%.txt
```

![logfile2](https://github.com/s01va/s01va.github.io/blob/master/_posts/2019-11-18-Windows-Batch-file/2.PNG)

"2019-11-18"이라는 문자열의 index가 2인 자리부터 끝까지 지정되어 19-11-18이 된 것을 볼 수 있다.

:[]=
[]자리에 해당하는 문자열을 잘라낸다.
```
@ECHO OFF
set PREFIX=%DATE%
@REM move log.txt log%PREFIX%.txt
set PREFIX2=%PREFIX:~2%
@REM move log%PREFIX%.txt log%PREFIX2%.txt
set PREFIX3=%PREFIX2:-=%
move log%PREFIX2%.txt log%PREFIX3%.txt
```

![logfile3](https://github.com/s01va/s01va.github.io/blob/master/_posts/2019-11-18-Windows-Batch-file/3.PNG)

"19-11-18"에서 -가 사라진 191118이 된 것을 볼 수 있다.



기타 cmd창 커스터마이즈
- color
- mode con cols=[] lines=[]


### color

color [1][2]
[1]은 배경색, [2]는 글씨색이다.

|Code|Color|
|----|-----|
| 0 | Black |
| 8 | Gray |
| 1 | Blue |
| 9 | Light Blue |
| 2 | Green |
| A | Light Green |
| 3 | Aqua |
| B | Light Aqua |
| 4 | Red |
| C | Light Red |
| 5 | Purple |
| D | Light Purple |
| 6 | Yellow |
| E | Light Yellow |
| 7 | White |
| F | Bright White |


### mode con cols=[] lines=[]

창 크기를 조절하는 명령어이다.
mode con cols=[가로크기] lines=[세로크기]


참고한 곳: https://ss64.com/nt/