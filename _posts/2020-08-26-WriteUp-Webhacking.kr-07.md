---
layout: single
title: "Webhacking.kr 6번"
description: "리뉴얼 기념 정주행"
date: 2020-02-08 12:37:00 -0400
# modified: 
tags:
- webhacking
- webhacking.kr
- wargame
- writeup
comments: true
share: true
---

![07](https://s01va.github.io/assets/images/2020-08-26-WriteUp-Webhacking.kr-07/0.PNG)

7번 문제는 이렇게 생겼다.

auth 버튼을 누르면 다음과 같은 경고창이 뜬다.

![after click auth](https://s01va.github.io/assets/images/2020-08-26-WriteUp-Webhacking.kr-07/1.PNG)

view-source는 아래와 같다.

```php
<?php
  include "../../config.php";
  if($_GET['view_source']) view_source();
?><html>
<head>
<title>Challenge 7</title>
</head>
<body>
<?php
$go=$_GET['val'];
if(!$go) { echo("<meta http-equiv=refresh content=0;url=index.php?val=1>"); }
echo("<html><head><title>admin page</title></head><body bgcolor='black'><font size=2 color=gray><b><h3>Admin page</h3></b><p>");
if(preg_match("/2|-|\+|from|_|=|\\s|\*|\//i",$go)) exit("Access Denied!");
$db = dbconnect();
$rand=rand(1,5);
if($rand==1){
  $result=mysqli_query($db,"select lv from chall7 where lv=($go)") or die("nice try!");
}
if($rand==2){
  $result=mysqli_query($db,"select lv from chall7 where lv=(($go))") or die("nice try!");
}
if($rand==3){
  $result=mysqli_query($db,"select lv from chall7 where lv=((($go)))") or die("nice try!");
}
if($rand==4){
  $result=mysqli_query($db,"select lv from chall7 where lv=(((($go))))") or die("nice try!");
}
if($rand==5){
  $result=mysqli_query($db,"select lv from chall7 where lv=((((($go)))))") or die("nice try!");
}
$data=mysqli_fetch_array($result);
if(!$data[0]) { echo("query error"); exit(); }
if($data[0]==1){
  echo("<input type=button style=border:0;bgcolor='gray' value='auth' onclick=\"alert('Access_Denied!')\"><p>");
}
elseif($data[0]==2){
  echo("<input type=button style=border:0;bgcolor='gray' value='auth' onclick=\"alert('Hello admin')\"><p>");
  solve(7);
}
?>
<a href=./?view_source=1>view-source</a>
</body>
</html>
```

~ 첫번째 조건문

```php
$go=$_GET['val'];
if(!$go) { echo("<meta http-equiv=refresh content=0;url=index.php?val=1>"); }
echo("<html><head><title>admin page</title></head><body bgcolor='black'><font size=2 color=gray><b><h3>Admin page</h3></b><p>");
```

val이라는 변수를 $\_GET해서 $go라는 변수에 넣고, $go라는 변수가 없으면 val=1로 생성한다.

그래서 초기 url이 `https://webhacking.kr/challenge/web-07/index.php?val=1`이었던 것으로 보인다.


두번째 조건문

```php
if(preg_match("/2|-|\+|from|_|=|\\s|\*|\//i",$go)) exit("Access Denied!");
```

preg_match라는 함수는 정규식을 사용하여 문자열을 검색이 가능하다.

$go 변수에 '2', '-', '+', 'from', '\_', '=', ' ', '\*', '/' 등이 검색되면 Access Denied라는 문구를 띄운다.

이 조건문을 우회하려면 변수 val에 어떤 값을 입력할 때 위에서 언급된 것들을 피해야 한다.


이 조건문을 우회하고 난 이후의 조건문들

```php
$db = dbconnect();
$rand=rand(1,5);
if($rand==1){
  $result=mysqli_query($db,"select lv from chall7 where lv=($go)") or die("nice try!");
}
if($rand==2){
  $result=mysqli_query($db,"select lv from chall7 where lv=(($go))") or die("nice try!");
}
if($rand==3){
  $result=mysqli_query($db,"select lv from chall7 where lv=((($go)))") or die("nice try!");
}
if($rand==4){
  $result=mysqli_query($db,"select lv from chall7 where lv=(((($go))))") or die("nice try!");
}
if($rand==5){
  $result=mysqli_query($db,"select lv from chall7 where lv=((((($go)))))") or die("nice try!");
}
```

dbconnect()를 한 후 위의 다섯 조건문들 중 하나에 랜덤하게 들어간다.

$go변수, 즉 val에 넣는 값이 그대로 where절에 들어가 쿼리를 실행하게 된다.

그리고 그 쿼리의 결과를 $result변수에 넣는다.

```php
$data=mysqli_fetch_array($result);
if(!$data[0]) { echo("query error"); exit(); }
if($data[0]==1){
  echo("<input type=button style=border:0;bgcolor='gray' value='auth' onclick=\"alert('Access_Denied!')\"><p>");
}
elseif($data[0]==2){
  echo("<input type=button style=border:0;bgcolor='gray' value='auth' onclick=\"alert('Hello admin')\"><p>");
  solve(7);
```

쿼리 결과가 담긴 $result를 array형태로 만들어 $data에 저장한다.

data 배열의 맨 첫번째 요소, 즉 lv가 2가 되어야 이 문제를 풀 수 있다.