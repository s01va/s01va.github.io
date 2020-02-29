---
layout: single
title: "Webhacking.kr 5번"
description: "리뉴얼 기념 정주행"
date: 2020-02-11 12:37:00 -0400
# modified: 
tags:
- webhacking
- webhacking.kr
- wargame
- writeup
comments: true
share: true
---

![05]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/0.PNG)

login / join이 있다.

![join_denied]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/1.PNG)

join은 접근이 되지 않는다.

![login]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/2.PNG)

login 화면은 위와 같이 뜬다.

![try_login]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/3.PNG)

![login failed]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/4.PNG)

위처럼 입력했더니 wrong password라고 뜬다. html 코드나 쿠키 등은 별 특이사항이 없었다.

URL이 기존 문제들처럼 /web-[문제번호]/ 뒤에 /mem/ + login.php의 형태로 이루어져 있어
login.php를 지운 /web-05/mem/으로 접속을 시도해 보았다.

![mem]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/5.PNG)

접속이 가능한 것을 볼 수 있다. 여기에서 join.php를 열어보는 시도를 해 보았다.

![bye]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/6.PNG)

이전과는 다르게 bye라는 알림창을 띄운다. 여기에서 html을 확인해 보았다.

![html]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/7.PNG)

위의 코드 중 `<script>` 파트만 가져와서 보면 아래와 같다.

```js

l='a';
ll='b';
lll='c';
llll='d';
lllll='e';
llllll='f';
lllllll='g';
llllllll='h';
lllllllll='i';
llllllllll='j';
lllllllllll='k';
llllllllllll='l';
lllllllllllll='m';
llllllllllllll='n';
lllllllllllllll='o';
llllllllllllllll='p';
lllllllllllllllll='q';
llllllllllllllllll='r';
lllllllllllllllllll='s';
llllllllllllllllllll='t';
lllllllllllllllllllll='u';
llllllllllllllllllllll='v';
lllllllllllllllllllllll='w';
llllllllllllllllllllllll='x';
lllllllllllllllllllllllll='y';
llllllllllllllllllllllllll='z';
I='1';
II='2';
III='3';
IIII='4';
IIIII='5';
IIIIII='6';
IIIIIII='7';
IIIIIIII='8';
IIIIIIIII='9';
IIIIIIIIII='0';
li='.';
ii='<';
iii='>';
lIllIllIllIllIllIllIllIllIllIl=lllllllllllllll+llllllllllll+llll+llllllllllllllllllllllllll+lllllllllllllll+lllllllllllll+ll+lllllllll+lllll;

lIIIIIIIIIIIIIIIIIIl=llll+lllllllllllllll+lll+lllllllllllllllllllll+lllllllllllll+lllll+llllllllllllll+llllllllllllllllllll+li+lll+lllllllllllllll+lllllllllllllll+lllllllllll+lllllllll+lllll;

if(eval(lIIIIIIIIIIIIIIIIIIl).indexOf(lIllIllIllIllIllIllIllIllIllIl)==-1) {
	alert('bye');
	throw "stop";
}

if(eval(llll+lllllllllllllll+lll+lllllllllllllllllllll+lllllllllllll+lllll+llllllllllllll+llllllllllllllllllll+li+'U'+'R'+'L').indexOf(lllllllllllll+lllllllllllllll+llll+lllll+'='+I)==-1){
	alert('access_denied');
	throw "stop";
}
else{
	document.write('<font size=2 color=white>Join</font><p>');
	document.write('.<p>.<p>.<p>.<p>.<p>');
	document.write('<form method=post action='+llllllllll+lllllllllllllll+lllllllll+llllllllllllll+li+llllllllllllllll+llllllll+llllllllllllllll
+'>');
	document.write('<table border=1><tr><td><font color=gray>id</font></td><td><input type=text name='+lllllllll+llll+' maxlength=20></td></tr>');
	document.write('<tr><td><font color=gray>pass</font></td><td><input type=text name='+llllllllllllllll+lllllllllllllllllllllll+'></td></tr>');
	document.write('<tr align=center><td colspan=2><input type=submit></td></tr></form></table>');
}

```

이 코드를 보고 bye나 access_denied가 아닌 pass를 띄우기 위해 맞춰주어야 할 조건들이 위에 명시되어 있다.

첫번째 조건:

```js
if(eval(lIIIIIIIIIIIIIIIIIIl).indexOf(lIllIllIllIllIllIllIllIllIllIl)==-1)
```

두번째 조건:

```js
if(eval(llll+lllllllllllllll+lll+lllllllllllllllllllll+lllllllllllll+lllll+llllllllllllll+llllllllllllllllllll+li+'U'+'R'+'L').indexOf(lllllllllllll+lllllllllllllll+llll+lllll+'='+I)==-1)
````

이 두 조건을 피해주면 된다.

`eval()` 함수는 문자열을 코드화 시켜주는 함수이다.
웹 브라우저의 개발자 도구에서 콘솔 기능을 사용하여 위의 코드를 분석한다.

![var]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/8.PNG)

먼저 변수와 관련된 모든 부분을 입력해 준다.
그리고 첫번째 조건 속 문자들이 무엇인지 조사했다.

`eval(lIIIIIIIIIIIIIIIIIIl)`의 `lIIIIIIIIIIIIIIIIIIl`

![document.cookie]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/9.PNG)

`indexOf(lIllIllIllIllIllIllIllIllIllIl)`의 `lIllIllIllIllIllIllIllIllIllIl`

![oldzombie]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/10.PNG)

쿠키 중 oldzombie라는 이름을 가진 쿠키가 있으면 첫번째 조건을 우회할 수 있다.

![make_cookie_oldzombie]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/11.PNG)

첫번째 조건을 우회하여 bye가 아닌 access_denied가 뜨는 것을 볼 수 있다.

![access_denied]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/12.PNG)

두번째 조건 속 문자들이 무엇인지 조사했다.

`eval(llll+lllllllllllllll+lll+lllllllllllllllllllll+lllllllllllll+lllll+llllllllllllll+llllllllllllllllllll+li+'U'+'R'+'L')`의
`llll+lllllllllllllll+lll+lllllllllllllllllllll+lllllllllllll+lllll+llllllllllllll+llllllllllllllllllll+li+'U'+'R'+'L'`

![document.URL]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/13.PNG)

`indexOf(lllllllllllll+lllllllllllllll+llll+lllll+'='+I)==-1)`의 `lllllllllllll+lllllllllllllll+llll+lllll+'='+I)==-1`

![mode=1]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/14.PNG)

URL에 mode라는 변수를 넣으면 두번째 조건을 우회할 수 있다.

![Join]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/15.PNG)

두 조건을 모두 우회하여 Join이라는 문자열과 함께 가입 양식을 받을 수 있다.

![Join2]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/16.PNG)

아무 값이나 입력했다.(admin라고 입력하면 이미 존재하는 id라고 한다.)

![signup]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/17.PNG)

![login]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/18.PNG)

로그인 페이지로 돌아가 join에서 입력했던 id와 패스워드를 입력하면 admin으로 로그인 할 수 있는 권한이 주어진다.

join 페이지로 돌아가 admin 앞에 공백을 추가하고 가입을 시도해 보았다.

![join  admin]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/19.PNG)

![success]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/20.PNG)

공백+admin으로 sign up하는데 성공했다.

![login s01va]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/21.PNG)

s01va로 로그인한 후 공백+admin으로 로그인을 시도했다.

![login success]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/22.PNG)

![pwned]({{site.url}}{{site.baseurl}}/assets/images/2020-02-11-WriteUp-Webhacking.kr-05/23.PNG)

