---
layout: single
title: "Webhacking.kr 1번"
description: "리뉴얼 기념 정주행""
date: 2019-11-21 16:00:00 -0400
# modified: 
tags: 
- WebHaking
- WarGame
- WriteUp
comments: true
share: true
---

![gate-01]({{site.url}}{{site.baseurl}}/assets/images/2019-11-21-WriteUp-Webhacking.kr-01/0.PNG)


```php
<?php
  include "../../config.php";
  if($_GET['view-source'] == 1){ view_source(); }
  if(!$_COOKIE['user_lv']){
    SetCookie("user_lv","1",time()+86400*30,"/challenge/web-01/");
    echo("<meta http-equiv=refresh content=0>");
  }
?>
<html>
<head>
<title>Challenge 1</title>
</head>
<body bgcolor=black>
<center>
<br><br><br><br><br>
<font color=white>
---------------------<br>
<?php
  if(!is_numeric($_COOKIE['user_lv'])) $_COOKIE['user_lv']=1;
  if($_COOKIE['user_lv']>=6) $_COOKIE['user_lv']=1;
  if($_COOKIE['user_lv']>5) solve(1);
  echo "<br>level : {$_COOKIE['user_lv']}";
?>
<br>
<a href=./?view-source=1>view-source</a>
</body>
</html>

```

user_lv 쿠키값이 6보다 같거나 크면 안되며
5보다 크면 solve된다.

쿠키값을 5.5로 맞추어 주었다.

![user_lv cookie]({{site.url}}{{site.baseurl}}/assets/images/2019-11-21-WriteUp-Webhacking.kr-01/1.PNG)

간단하게 1번문제를 풀었다.
![pwned!]({{site.url}}{{site.baseurl}}/assets/images/2019-11-21-WriteUp-Webhacking.kr-01/2.PNG)

![Congratz]({{site.url}}{{site.baseurl}}/assets/images/2019-11-21-WriteUp-Webhacking.kr-01/3.PNG)

※
나는 웹해킹 문제를 주로 Chrome에서 풀이했다.
쿠키값 조정은 [이 확장 프로그램](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?utm_source=chrome-ntp-icon)을 주로 사용했다.