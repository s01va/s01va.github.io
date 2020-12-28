---
layout: single
title: "Windows 10 IIS와 WebLogic 12c 연동하기"
description:
date: 2020-02-21 11:00:00 -0400
modified: 2019-11-21 15:38:23 -0400
tags: 
- was
- webserver
- weblogic
- iis
- middleware
comments: true
share: true
---

[WebLogic 설치](https://s01va.github.io/Windows-10%EC%97%90%EC%84%9C-WebLogic-12c-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0/) 이후 과정이다.


## IIS 설치


제어판 - 모든 제어판 항목 - 프로그램 및 기능으로 들어간다.

![controlpannel-program](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/0.PNG)

좌측 상단에 있는 Windows 기능 켜기/끄기를 눌러 Windows 기능 창을 연다.

![IIS start](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/1.PNG)

![IIS start2](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/2.PNG)

![IIS start3](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/3.PNG)

스크롤을 쭉쭉 내리면 '인터넷 정보 서비스'를 발견할 수 있다. 이를 체크해 준다.
설치가 완료되면 IIS를 실행시켜 준다.
(윈도우 시작 창에서 IIS를 검색하면 찾을 수 있다)

![IIS](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/4.PNG)

IIS의 첫 화면이다. 사이트에 우클릭해서 웹 사이트 추가를 눌러준다.

![add website](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/5.PNG)

사이트 추가를 해준다.
80번 포트를 사용하고 싶으면 Default Web Site를 지우거나 정지시킨다.
정지시킬 때는 응용 프로그램 풀에서도 정지시켜 주어야 한다.

![virtual directory](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/6.PNG)

생성한 웹사이트를 우클릭해서 가상 디렉토리를 생성한다.

### ★주의할 점

예를 들어 기존에 http://localhost/webtest로 접속해야 하는 서비스라면
가상 디렉토리를 webtest로 생성해 주어야 한다.
혼동을 피하기 위해 IIS 전용으로 생성한 폴더 내부에 webtest라는 폴더를 새로 생성하여 실제 경로로 지정하였다.


## WebLogic - IIS Plugin 다운로드

[여기](https://www.oracle.com/middleware/technologies/webtier-downloads.html#server3)에서 플러그인을 다운받는다.

![plugin download](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/7.PNG)

![plugin download2](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/8.PNG)

이후 오라클 로그인을 하면 한 압축파일이 다운받아진다.

![zip](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/9.PNG)

압축파일의 내부이다. 모든 웹서버에 대한 플러그인이 모두 들어있다. 이 중 IIS-Win64에 해당되는 플러그인을 선택해 압축을 해제한다.

![dlls](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/10.PNG)

플러그인 폴더의 lib 내부에 아래와 같은 dll 파일들이 존재하는 것을 확인할 수 있다.


## WebLogic - IIS 연동

이전 단계에서 다운받은 dll 파일들을 전부 가져온다.

![wlplugin](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/11.PNG)

IIS 전용으로 생성한 폴더 내에 연동 플러그인 전용 폴더를 생성하여 dll들을 전부 복붙해 주었다.

![처리기 매핑](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/12.PNG)

IIS로 돌아가서 이전에 만든 가상 디렉토리 창에서 처리기 매핑을 찾는다.

![script mapping](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/13.PNG)

스크립트 매핑을 클릭한다.

![add dll](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/14.PNG)

위와 같이 입력해 준다. 실행 파일은 복붙해온 dll 파일들 중에서 찾는다.

그리고 요청 제한을 클린한다.

![mapping](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/15.PNG)

![verb](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/16.PNG)

![access](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/17.PNG)

위와 같이 설정해 준다. 그대로 확인-확인-예 해준다. 

![add iisproxy](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/18.PNG)

성공적으로 추가한 것을 볼 수 있다.

이외에도 생성해야 할 파일이 있다. dll파일을 복붙한 폴더로 이동한 후 아래와 같은 이름의 파일을 생성한다.

![make iisproxy.ini](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/19.PNG)

아래와 같은 형식으로 작성한다.

```bash
WebLogicCluster=[Host]:[Port]
```

![iisproxy.ini](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/20.PNG)

다음은 위에서 생성한 가상 디렉토리에 대응하는 실제 디렉토리로 들어가서 index.html을 생성해 준다.

![index.html](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/21.PNG)

```html
<html>
	<head>
	</head>
	<body>
		<script>location.href="/webtest";</script>
	</body>
</html>
```

생성한 index.html에 위의 내용을 작성하였다. /webtest 부분은 각자 설정에 맞게 바꾼다.

![](https://s01va.github.io/assets/images/2020-02-21-Windows-10-IIS-with-WebLogic-12c/22.PNG)

성공적으로 연동된 것을 볼 수 있다.


## 추가

컴퓨터에 따라 간혹 오류코드 0x8007007e(500번 오류)가 뜨기도 한다.

이럴 때는 [마이크로소프트 페이지](https://www.microsoft.com/en-us/download/details.aspx?id=30679)에서 vc++ 런타임을 다운로드 받고 설치해 주면 해결된다.
