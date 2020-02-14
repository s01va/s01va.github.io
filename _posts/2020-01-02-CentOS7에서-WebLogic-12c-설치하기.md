---
layout: single
title: "CentOS7에서 WebLogic 12c 설치하기"
description: "WebLogic 12.2.1.4.0"
date: 2019-12-26 12:37:00 -0400
# modified: 
tags: 
- centos
- was
- weblogic
- middleware
comments: true
share: true
---

선수 요구사항:
Oracle 계정
Java HotSpot(TM) 1.8.0_241
앞으로 CentOS7에서 모든 WAS 테스트는 /was 경로에서 진행할 것이다.

폐쇄망이라고 가정한다.


# 선수 요구사항을 위한 세팅

java를 설치한다.

[여기](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)에서 리눅스용 자바를 다운받고 해당 CentOS로 옮겼다.

<center>![oracle java download]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/0.PNG)</center>

<center>![oracle java download]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/1.PNG)</center>

내려받은 rpm 파일로 java를 설치한다.

<center>![rpm]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/2.PNG)</center>

root로 진행해야 한다.
참고로 위에서 사용한 rpm 명령어의 옵션값은 아래와 같은 의미를 가진다.

| Option | 의미 |
| -- | -- |
| -i | Install(설치) |
| -v | Verbose(상세) |
| -h | Header(헤더를 표시) |
| --prefix | 설치경로 |

설치경로는 따로 설정하지 않아도 좋지만 따로 설정하지 않으면 /usr/경로 아래에 패키지가 설치될 것이다.
위에서 prefix옵션 뒤의 경로는 미리 생성해둔 경로이다.

설치 후 환경변수에 JAVA_HOME을 추가해 주어야 한다. 홈 경로의 .bash_profile을 아래와 같이 수정해 준다.
(.bashrc에서 설정한 것들은 재접속하면 날아간다.)

<center>![.bash_profile]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/3.PNG)</center>

그리고 아래와 같은 명령어로 수정된 .bash_profile 파일을 적용해 준다.

```bash
. .bash_profile
```


[CentOS7에서 X11 forwarding 설정(X Window 설치)](https://s01va.github.io/CentOS7%EC%97%90%EC%84%9C-X11-forwarding-%EC%84%A4%EC%A0%95/)를 해두면 이후 과정은 [이 페이지](https://s01va.github.io/Windows-10%EC%97%90%EC%84%9C-WebLogic-12c-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0/)를 그대로 따라해도 좋다.


하지만 폐쇄망 환경이라면 의존성 문제 등으로 Xwindow는 설치하기 까다로울 수 있다.
콘솔 모드로 설치하는 것을 생각할 수 있는데, 12c 버전부터는 콘솔 모드를 지원하지 않는다.
(`-mode=console`로 설치를 시도하면, 부적합한 인수라고 함..)

대신 사일런트 모드를 사용할 수 있으므로, 사일런트 모드 설치과정을 기재하였다.


# 설치파일 다운로드

[Oracle](https://www.oracle.com/middleware/technologies/fusionmiddleware-downloads.html)에서 Generic Installer 다운로드

<center>![Oracle Weblogic]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/4.PNG)</center>

<center>![Oracle Weblogic]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/5.PNG)</center>


다음과 같은 압축파일이 다운받아진다

<center>![Oracle Weblogic zipfile]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/6.PNG)</center>


다운로드 받은 파일을 CentOS로 옮겨준다.

<center>![zip file in CentOS]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/7.PNG)</center>


# WebLogic 설치

압축을 풀어준다.

<center>![unzip]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/8.PNG)</center>

사일런트 모드가 아니라면 바로 설치를 진행할 수 있지만
사일런트 모드로 설치하기 위해서는 사전에 생성해야 할 파일이 두 개가 있다.
(사일런트 모드 설치 명령어는 다음과 같이 이루어진다.)

```bash
java -jar fmw_12.2.1.4.0_wls.jar -silent -responseFile [response 포인터 파일 절대경로] -invPtrLoc [인벤토리 포인터 파일 절대경로]
```



## Response file 생성

`-responseFile` 옵션에 들어갈 파일을 생성해 주어야 한다.

여기서 중요한 것은 ORACLE_HOME, INSTALL_TYPE, SECURITY_UPDATES_VIA_MYORACLESUPPORT 세가지 정도.
각자의 환경에 맞게 써준다.

출처: [오라클](https://docs.oracle.com/middleware/1212/core/OUIRF/response_file.htm#OUIRF392)

```sh
[ENGINE]
 
#DO NOT CHANGE THIS.
Response File Version=1.0.0.0.0
 
[GENERIC]
 
#The oracle home location. This can be an existing Oracle Home or a new Oracle Home
ORACLE_HOME=/was/weblogic12c
 
#Set this variable value to the Installation Type selected. e.g. Fusion Middleware Infrastructure, Fusion Middleware Infrastructure With Examples.
INSTALL_TYPE=WebLogic Server
 
#Provide the My Oracle Support Username. If you wish to ignore Oracle Configuration Manager configuration provide empty string for user name.
MYORACLESUPPORT_USERNAME=
 
#Provide the My Oracle Support Password
MYORACLESUPPORT_PASSWORD=<SECURE VALUE>
 
#Set this to true if you wish to decline the security updates. Setting this to true and providing empty string for My Oracle Support username will ignore the Oracle Configuration Manager configuration
DECLINE_SECURITY_UPDATES=true
 
#Set this to true if My Oracle Support Password is specified
SECURITY_UPDATES_VIA_MYORACLESUPPORT=false
 
#Provide the Proxy Host
PROXY_HOST=
 
#Provide the Proxy Port
PROXY_PORT=
 
#Provide the Proxy Username
PROXY_USER=
 
#Provide the Proxy Password
PROXY_PWD=<SECURE VALUE>
 
#Type String (URL format) Indicates the OCM Repeater URL which should be of the format [scheme[Http/Https]]://[repeater host]:[repeater port]
COLLECTOR_SUPPORTHUB_URL=
```

ORACLE_HOME에 해당되는 디렉토리는 따로 직접 생성해 준다.

.rsp 형태로 파일명을 지정해준다.

<center>![naming rsp file]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/9.PNG)</center>

<center>![making rsp file]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/10.PNG)</center>

<center>![making oracle_home]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/11.PNG)</center>


## 인벤토리 포인터 파일 생성

`-invPtrLoc` 옵션에 들어갈 파일도 필요하다.
이 파일의 이름은 oraInst.loc이어야 한다.
이를 아래와 같이 작성해 준다.

```sh
inventory_loc=/was/oraInventory
inst_group=weblogic
```
oraInventory는 오라클 제품군 설치 시 필요한 파일들이 들어 있는 디렉토리이다.
설치 시 디렉토리 째로 생성된다. 위의 inventory_loc 뒤에 이 oraInventory가 생성될 경로를 입력해 준다.

<center>![naming loc file]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/12.PNG)</center>

<center>![making loc file]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/13.PNG)</center>



이제 설치해 준다.

<center>![Install silent mode]({{site.url}}{{site.baseurl}}/assets/images/2020-01-02-in-CentOS7-WebLogic12c-Install/14.PNG)</center>


---------------------------------------------------------------------------------

# 도메인 구성


[작성중]