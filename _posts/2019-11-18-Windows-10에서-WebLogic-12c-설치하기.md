---
layout: single
title: "Windows 10에서 WebLogic 12c 설치하기"
description:
date: 2019-10-23 16:00:00 -0400
# modified: 
tags: 
- WAS
- WebLogic
- Middleware
comments: true
share: true
---

환경:
Windows 10
WAS 환경을 D드라이브에 별도로 구성하고자 함


선수 요구사항:
Oracle 계정
Java HotSpot(TM) 1.8.0_221
본인은 D드라이브에 있는 WAS만을 위한 Java를 따로 설치하였다.


# 설치파일 다운로드

https://www.oracle.com/middleware/technologies/fusionmiddleware-downloads.html 에서 Generic Installer 다운로드

![Oracle Weblogic](https://s01va.github.io/../../../0.png)

![Oracle Weblogic](https://s01va.github.io/../../../1.png)


다음과 같은 압축파일이 다운받아진다

![Oracle Weblogic zipfile](https://s01va.github.io/../../../2.png)


# WebLogic 설치

아래와 같은 명령어로 jar파일을 실행시킨다.
관리자로 실행

``` java -jar -d64 fmw_12.2.1.4.0_wls.jar ```

![Oracle Weblogic java jar](https://s01va.github.io/../../../3.png)

아래는 설치 과정.

![Oracle Weblogic install 1/8](https://s01va.github.io/../../../4.png)

![Oracle Weblogic install 2/8](https://s01va.github.io/../../../5.png)


D:\Oracle\Middleware\Oracle_Home 이었던 경로를 아래와 같이 바꾸었다.
어차피 단일 디렉토리임

![Oracle Weblogic install 3/8](https://s01va.github.io/../../../6.png)

![Oracle Weblogic install 4/8](https://s01va.github.io/../../../7.png)

![Oracle Weblogic install 5/8](https://s01va.github.io/../../../8.png)

![Oracle Weblogic install 6/8](https://s01va.github.io/../../../9.png)

그대로 설치

![Oracle Weblogic install 7/8](https://s01va.github.io/../../../10.png)

![Oracle Weblogic install 8/8](https://s01va.github.io/../../../11.png)


# 도메인 생성 및 Admin Server 생성

완료버튼을 누르면 그대로 도메인 생성과 Admin server 생성 과정이 시작된다.
도메인 경로는 기본적으로 D:\WAS\WebLogic12.2.1.4.0\user_projects\domains\base_domain라 뜨지만
용도별로 base_domain 이름을 바꿔주는 것이 좋다.
나는 연습용이라 prac으로 명명함

![Oracle Weblogic Domain install 1/9](https://s01va.github.io/../../../12.png)

![Oracle Weblogic Domain install 2/9](https://s01va.github.io/../../../13.png)

![Oracle Weblogic Domain install 3/9](https://s01va.github.io/../../../14.png)

![Oracle Weblogic Domain install 4/9](https://s01va.github.io/../../../15.png)
운영 목적이기 때문에 운영에 체크하였다. JDK가 다른 드라이브에 잡혀 있다면 새로 위치를 잡아주도록 한다.

![Oracle Weblogic Domain install 5/9](https://s01va.github.io/../../../16.png)
관리 서버에 체크.

![Oracle Weblogic Domain install 6/9](https://s01va.github.io/../../../17.png)
수신 포트는 회사마다 바꾸는 곳도 있을 것이니 유의. 나는 연습용이라 그대로

![Oracle Weblogic Domain install 7/9](https://s01va.github.io/../../../18.png)
그대로 생성한다

![Oracle Weblogic Domain install 8/9](https://s01va.github.io/../../../19.png)

![Oracle Weblogic Domain install 9/9](https://s01va.github.io/../../../20.png)
설치가 완료되었다. 관리 서버 URL 잘 봐두기

http://localhost:7001/console
http://[host]:[port]/console


cmd 창에서 접근의 용이함을 위해 환경변수를 추가하였다.

![Oracle Weblogic DOMAIN_HOME](https://s01va.github.io/../../../21.png)

![Oracle Weblogic DOMAIN_HOME](https://s01va.github.io/../../../22.png)

bin에도 명령어가 있지만 DOMAIN_HOME에도 있다. 웹로직 기동을 위해 이것을 실행시킨다.
![Oracle Weblogic startWebLogic.cmd1](https://s01va.github.io/../../../23.png)

![Oracle Weblogic startWebLogic.cmd2](https://s01va.github.io/../../../24.png)
설치 시에 입력했던 username과 패스워드를 입력한다.

이후 Running이 뜨면 잘 기동이 된 것이다.
![Oracle Weblogic startWebLogic.cmd RUNNING](https://s01va.github.io/../../../25.png)


# Managed Server 생성

이전에 봐 두었던 콘솔 창 url로 접속한다.
http://[host]:[port]/console


![Oracle Weblogic console](https://s01va.github.io/../../../26.png)
콘솔 창이 정상적으로 뜨면 문제없이 기동된 것. 아까 입력한 username과 패스워드로 로그인한다.


![Oracle Weblogic console](https://s01va.github.io/../../../27.png)
환경 > 서버로 들어간다.

![Oracle Weblogic console](https://s01va.github.io/../../../28.png)
잠금 및 편집으로 lock을 풀어준다.

![Oracle Weblogic console](https://s01va.github.io/../../../29.png)
새로 만들기

![Oracle Weblogic console](https://s01va.github.io/../../../30.png)
매니지드 서버를 이와 같은 조건으로 생성하였다.

![Oracle Weblogic console](https://s01va.github.io/../../../31.png)
변경 내용 활성화를 눌러준다.

매니지드 서버가 생성되었지만 기동되지 않은 상태이다.
%DOMAIN_HOME%\bin에서 다음과 같은 명령어를 실행시켜 준다.

``` startManagedWebLogic.cmd [Managed Server Name] t3://[AdminServer Host]:[AdminServer Port] ```

![Oracle Weblogic startManagedWebLogic.cmd](https://s01va.github.io/../../../32.png)

startWebLogic.cmd때 처럼 username과 password를 입력해 준다.

![Oracle Weblogic startManagedWebLogic.cmd Login](https://s01va.github.io/../../../33.png)

![Oracle Weblogic startManagedWebLogic.cmd RUNNING](https://s01va.github.io/../../../34.png)
위와 같이 RUNNING이 뜨고

![Oracle Weblogic console](https://s01va.github.io/../../../35.png)
Managed01 서버의 상태가 RUNNING으로 바뀐 것을 볼 수 있다.


# WebLogic 구동시 자동 로그인을 위한 boot.properties 생성

startWebLogic.cmd로 웹로직을 실행시킬 때마다 일일히 로그인을 해야 한다.
이를 %DOMAIN_HOME%/servers/[adminserver]/security/boot.properties를 생성하여 자동 로그인을 하게 할 수 있다.

%DOMAIN_HOME%/servers/[adminserver]에 본애 security 디렉토리는 없다. 이를 만들어 준 후 boot.properties를 아래와 같이 작성한다.

![boot.properties](https://s01va.github.io/../../../36.png)

= 뒤에 본인이 설정했던 username과 패스워드를 입력한다. 일단 평문으로 저장해 주면, 이후에 웹로직을 기동할 때 암호화된다.
boot.properties를 저장한 후 startWebLogic.cmd로 웹로직을 재기동시키면 username과 패스워드를 요구하지 않고 RUNNING이 뜨는 것을 볼 수 있다.
재기동 후 boot.properties를 열어보면 암호화가 되어 저장되어진 것을 볼 수 있다.


# 편의를 위한 실행 배치파일 생성 + 배치파일 기본 작성법 작성 후 링크걸기

배치파일 만들기 -> [링크]

아래와 같이 두 스크립트를 만들었다.

Admin Server 구동 스크립트

```
@ECHO OFF
set SERVER_NAME=AdminServer
 
title WebLogic_%SERVER_NAME%
set DOMAIN_HOME=D:\WAS\WebLogic12.2.1.4.0\user_projects\domains\prac
set LOG_DIR=D:\WAS\Log\WebLogicLog\AdminServer

cd %DOMAIN_HOME%

@REM for log backup
set PREFIX=%DATE:~2%_%TIME:~0,-3%
set PREFIX=%PREFIX::=%
set PREFIX=%PREFIX:-=%
set PREFIX=%PREFIX: =0%
set PREFIX=%PREFIX:/=%
 
@REM ren %LOG_DIR%\%SERVER_NAME%.out %LOG_DIR%\%SERVER_NAME%.out.%PREFIX%

move %LOG_DIR%\%SERVER_NAME%.out %LOG_DIR%\%SERVER_NAME%.out.%PREFIX%
 
set USER_MEM_ARGS=-Xms512m -Xmx512m -verbosegc

start /B %DOMAIN_HOME%\startWebLogic.cmd > %LOG_DIR%\%SERVER_NAME%.out 2>&1
 
tail -f %LOG_DIR%\%SERVER_NAME%.out
```

Managed Server 구동 스크립트
```
@ECHO OFF
 
set SERVER_NAME=Managed01

title WebLogic_%SERVER_NAME%
set DOMAIN_HOME=D:\WAS\WebLogic12.2.1.4.0\user_projects\domains\prac
set LOG_DIR=D:\WAS\Log\WebLogicLog\Managed01
set ADM_URL="t3://127.0.0.1:7001"

cd %DOMAIN_HOME%

@REM ######### WebLogic log backup #########
set PREFIX=%DATE:~2%_%TIME:~0,-3
set PREFIX=%PREFIX::=%
set PREFIX=%PREFIX:-=%
set PREFIX=%PREFIX: =0%
set PREFIX=%PREFIX:/=%
 
@REM ren %LOG_DIR%\%SERVER_NAME%.out %LOG_DIR%\%SERVER_NAME%.out.%PREFIX%
move %LOG_DIR%\%SERVER_NAME%.out %LOG_DIR%\%SERVER_NAME%.out.%PREFIX%
 
set USER_MEM_ARGS=-Xms1024m -Xmx1024m
set USER_MEM_ARGS=%USER_MEM_ARGS% -XX:+HeapDumpOnOutOfMemoryError
set USER_MEM_ARGS=%USER_MEM_ARGS% -verbosegc -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -Xloggc:%LOG_DIR%\%SERVER_NAME%.gc
start /B %DOMAIN_HOME%\bin\startManagedWebLogic.cmd %SERVER_NAME% %ADM_URL% > %LOG_DIR%\%SERVER_NAME%.out 2>&1
 
tail -f %LOG_DIR%\%SERVER_NAME%.out
```



# 웹 어플리케이션 배포하기

[테스트용 어플리케이션 만들기 포스트 링크]

