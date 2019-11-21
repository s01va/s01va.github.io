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

![Oracle Weblogic]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/0.PNG)

![Oracle Weblogic]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/1.PNG)


다음과 같은 압축파일이 다운받아진다

![Oracle Weblogic zipfile]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/2.PNG)


# WebLogic 설치

아래와 같은 명령어로 jar파일을 실행시킨다.
관리자로 실행

``` java -jar -d64 fmw_12.2.1.4.0_wls.jar ```

![Oracle Weblogic java jar]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/3.PNG)

아래는 설치 과정.

![Oracle Weblogic install 1/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/4.PNG)

![Oracle Weblogic install 2/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/5.PNG)


D:\Oracle\Middleware\Oracle_Home 이었던 경로를 아래와 같이 바꾸었다.
어차피 단일 디렉토리임

![Oracle Weblogic install 3/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/6.PNG)

![Oracle Weblogic install 4/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/7.PNG)

![Oracle Weblogic install 5/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/8.PNG)

![Oracle Weblogic install 6/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/9.PNG)

그대로 설치

![Oracle Weblogic install 7/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/10.PNG)

![Oracle Weblogic install 8/8]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/11.PNG)


# 도메인 생성 및 Admin Server 생성

완료버튼을 누르면 그대로 도메인 생성과 Admin server 생성 과정이 시작된다.
도메인 경로는 기본적으로 D:\WAS\WebLogic12.2.1.4.0\user_projects\domains\base_domain라 뜨지만
용도별로 base_domain 이름을 바꿔주는 것이 좋다.
나는 연습용이라 prac으로 명명함

![Oracle Weblogic Domain install 1/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/12.PNG)

![Oracle Weblogic Domain install 2/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/13.PNG)

![Oracle Weblogic Domain install 3/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/14.PNG)

![Oracle Weblogic Domain install 4/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/15.PNG)
운영 목적이기 때문에 운영에 체크하였다. JDK가 다른 드라이브에 잡혀 있다면 새로 위치를 잡아주도록 한다.

![Oracle Weblogic Domain install 5/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/16.PNG)
관리 서버에 체크.

![Oracle Weblogic Domain install 6/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/17.PNG)
수신 포트는 회사마다 바꾸는 곳도 있을 것이니 유의. 나는 연습용이라 그대로

![Oracle Weblogic Domain install 7/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/18.PNG)
그대로 생성한다

![Oracle Weblogic Domain install 8/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/19.PNG)

![Oracle Weblogic Domain install 9/9]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/20.PNG)
설치가 완료되었다. 관리 서버 URL 잘 봐두기

http://localhost:7001/console
http://[host]:[port]/console


cmd 창에서 접근의 용이함을 위해 환경변수를 추가하였다.

![Oracle Weblogic DOMAIN_HOME]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/21.PNG)

![Oracle Weblogic DOMAIN_HOME]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/22.PNG)

bin에도 명령어가 있지만 DOMAIN_HOME에도 있다. 웹로직 기동을 위해 이것을 실행시킨다.
![Oracle Weblogic startWebLogic.cmd1]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/23.PNG)

![Oracle Weblogic startWebLogic.cmd2]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/24.PNG)
설치 시에 입력했던 username과 패스워드를 입력한다.

이후 Running이 뜨면 잘 기동이 된 것이다.
![Oracle Weblogic startWebLogic.cmd RUNNING]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/25.PNG)


# Managed Server 생성

이전에 봐 두었던 콘솔 창 url로 접속한다.
http://[host]:[port]/console


![Oracle Weblogic console]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/26.PNG)
콘솔 창이 정상적으로 뜨면 문제없이 기동된 것. 아까 입력한 username과 패스워드로 로그인한다.


![Oracle Weblogic console]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/27.PNG)
환경 > 서버로 들어간다.

![Oracle Weblogic console]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/28.PNG)
잠금 및 편집으로 lock을 풀어준다.

![Oracle Weblogic console]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/29.PNG)
새로 만들기

![Oracle Weblogic console]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/30.PNG)
매니지드 서버를 이와 같은 조건으로 생성하였다.

![Oracle Weblogic console]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/31.PNG)
변경 내용 활성화를 눌러준다.

매니지드 서버가 생성되었지만 기동되지 않은 상태이다.
%DOMAIN_HOME%\bin에서 다음과 같은 명령어를 실행시켜 준다.

``` startManagedWebLogic.cmd [Managed Server Name] t3://[AdminServer Host]:[AdminServer Port] ```

![Oracle Weblogic startManagedWebLogic.cmd]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/32.PNG)

startWebLogic.cmd때 처럼 username과 password를 입력해 준다.

![Oracle Weblogic startManagedWebLogic.cmd Login]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/33.PNG)

![Oracle Weblogic startManagedWebLogic.cmd RUNNING]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/34.PNG)
위와 같이 RUNNING이 뜨고

![Oracle Weblogic console]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/35.PNG)
Managed01 서버의 상태가 RUNNING으로 바뀐 것을 볼 수 있다.


# WebLogic 구동시 자동 로그인을 위한 boot.properties 생성

startWebLogic.cmd로 웹로직을 실행시킬 때마다 일일히 로그인을 해야 한다.
이를 %DOMAIN_HOME%/servers/[adminserver]/security/boot.properties를 생성하여 자동 로그인을 하게 할 수 있다.

%DOMAIN_HOME%/servers/[adminserver]에 본애 security 디렉토리는 없다. 이를 만들어 준 후 boot.properties를 아래와 같이 작성한다.

![boot.properties]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/36.PNG)

= 뒤에 본인이 설정했던 username과 패스워드를 입력한다. 일단 평문으로 저장해 주면, 이후에 웹로직을 기동할 때 암호화된다.
boot.properties를 저장한 후 startWebLogic.cmd로 웹로직을 재기동시키면 username과 패스워드를 요구하지 않고 RUNNING이 뜨는 것을 볼 수 있다.
재기동 후 boot.properties를 열어보면 암호화가 되어 저장되어진 것을 볼 수 있다.

![encrypted boot.properties]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/37.PNG)

%DOMAIN_HOME%/servers/[managedserver]에도 같은 식으로 생성해 준다.



# 편의를 위한 실행 배치파일 생성 + 배치파일 기본 작성법 작성 후 링크걸기

[배치파일 만들기](https://s01va.github.io/Windows-Batch-file-%EB%A7%8C%EB%93%A4%EA%B8%B0/)

아래와 같이 두 스크립트를 만들었다.

Admin Server 구동 스크립트

```batch
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

```batch
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

Log_DIR에 추가적으로 생성해야 하는 폴더(AdminServer, Managed01)는 직접 만들어 주어야 한다.
위의 두 스크립트를 runAdminServer.cmd, runManaged01.cmd로 이름을 붙이고 %DOMAIN_HOME%에 위치시켰다.


※
tail은 로그를 모니터링할 때 편리한 프로그램이다. 파일에 로그가 쌓일 때마다 실시간으로 콘솔에 띄워준다.
리눅스에서 기본적으로 제공되는 프로그램인데 윈도우에서는 기본제공이 되지 않는다.
tail 프로그램은 종류도 다양하고 많으니 마음에 드는 것을 다운받아 %DOMAIN_HOME%으로 옮겨주면 위의 스크립트에서 사용할 수 있다.

![runAdminServer.cmd]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/38.PNG)


![runManaged01.cmd]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/39.PNG)


두 스크립트가 잘 실행된 것을 볼 수 있다.



# 웹 어플리케이션 배포(Deploy)하기

[여기](https://s01va.github.io/WAS-%ED%85%8C%EC%8A%A4%ED%8A%B8%EC%9A%A9-%EC%9B%B9-%EC%96%B4%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%A7%8C%EB%93%A4%EA%B8%B0/)에서 만든 테스트용 웹 어플리케이션을 배포하려 한다.

.war파일을 배포할 수도 있고, 여러가지 방법이 있지만 폴더째로 배포하는 방법이 있다.

내가 테스트용으로 만든 웹 어플리케이션 webtest의 내부는 이렇게 생겼다.

![webtest]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/40.PNG)

![webtest-WebContent]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/41.PNG)

WebContent 내부에는 META-INF, WEB-INF 등이 필히 존재하는데, 이 구조는 war파일 구조와 다르지 않다. 그리고 WEB-INF에 web.xml이 적절한 형태로 존재하면 배포시 war파일로 인식시킬 수 있다.

이 WebContent 폴더를 WAS를 실행시키는 D드라이브로 복사하고 webtest로 폴더명을 바꾸었다.

![webtest-WebContent]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/42.PNG)

이제부터 이 폴더를 WebLogic에 배포해볼 것이다.

웹로직 콘솔에 들어간다.

![WebLogic Console - Domain Structure]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/43.PNG)

잠금 및 편집을 누른 후 배치 - 설치를 누른다.

![WebLogic Console - Deploy - Install]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/44.PNG)

Deploy할 웹 어플리케이션을 폴더로 지정해 준다.

![WebLogic Console - Deploy - Install2]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/45.PNG)

다음을 누른다.

![WebLogic Console - Deploy - Install3]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/46.PNG)

다음

![WebLogic Console - Deploy - Install4]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/47.PNG)

다음

![WebLogic Console - Deploy - Install5]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/48.PNG)

나머지 설정은 기본으로 두고 소스 접근성 설정만 위와 같이 바꾸었다.

완료

![WebLogic Console - Deploy Complete]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/49.PNG)

성공적으로 Deploy했다. 변경 내용 활성화를 눌러준다.

![WebLogic Console - application ready]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/50.PNG)

배포한 어플리케이션의 상태가 "준비됨"으로 바뀌었다. 이를 실행시키려면 콘트롤 탭으로 가야한다.

![WebLogic Console - application ready2]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/51.PNG)

잠금 및 편집을 누르고 해당 어플리케이션을 선택 후 시작을 누른다.

![WebLogic Console - application deploy]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/52.PNG)

배치 관련 Summury가 뜬다. 예를 눌러준다.

![WebLogic Console - application deploy complete]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/53.PNG)

어플리케이션의 상태가 Running으로 바뀐 것을 볼 수 있다.

아래와 같은 URL로 접속하여 배포 성공 여부를 확인한다.

localhost:[ManagedServerPort]/[DeployedAppContextroot]

ManagedServerPort는 좌측의 도메인 구조 - 환경 - 서버에서도 확인할 수 있다.

![ManagedServerPort]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/54.PNG)

DeployedAppContextroot는 도메인 구조 - 배치 - 배포항 어플리케이션을 선택하면 볼 수 있다.

![DeployedAppContextroot]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/55.PNG)

자동으로 어플리케이션 이름으로 컨텍스트 루트를 설정하는 것으로 보인다.
(루트로 설정하는법 아시는분..)

나의 경우엔 localhost:8001/webtest로 들어가면 서비스 성공 여부를 확인할 수 있다.

![All Complete!]({{site.url}}{{site.baseurl}}/assets/images/2019-11-18-Windows10-WebLogic12c/56.PNG)
