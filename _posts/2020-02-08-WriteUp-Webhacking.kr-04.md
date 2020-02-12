---
layout: single
title: "Webhacking.kr 4번"
description: "리뉴얼 기념 정주행"
date: 2020-02-08 12:37:00 -0400
# modified: 
tags:
- webhacking
- webhacking.kr
- wargame
- writeup
- sha1
- sha1-crack
comments: true
share: true
---


![04]({{site.url}}{{site.baseurl}}/assets/images/2020-02-08-WriteUp-Webhacking.kr-04/0.PNG)

4번 문제의 첫 화면이다. 저 값은 새로고침을 할 때마다 바뀐다.

view-source를 누르면 아래와 같은 소스코드가 나온다.

```xml
<?php
  include "../../config.php";
  if($_GET['view-source'] == 1) view_source();
?><html>
<head>
<title>Challenge 4</title>
<style type="text/css">
body { background:black; color:white; font-size:9pt; }
table { color:white; font-size:10pt; }
</style>
</head>
<body><br><br>
<center>
<?php
  sleep(1); // anti brute force
  if((isset($_SESSION['chall4'])) && ($_POST['key'] == $_SESSION['chall4'])) solve(4);
  $hash = rand(10000000,99999999)."salt_for_you";
  $_SESSION['chall4'] = $hash;
  for($i=0;$i<500;$i++) $hash = sha1($hash);
?><br>
<form method=post>
<table border=0 align=center cellpadding=10>
<tr><td colspan=3 style=background:silver;color:green;><b><?=$hash?></b></td></tr>
<tr align=center><td>Password</td><td><input name=key type=text size=30></td><td><input type=submit></td></tr>
</table>
</form>
<a href=?view-source=1>[view-source]</a>
</center>
</body>
</html>
```

아래의 조건만 충족하면 4번 문제를 풀 수 있다.

```php
  if((isset($_SESSION['chall4'])) && ($_POST['key'] == $_SESSION['chall4'])) solve(4);
```

isset 함수는 해당 함수가 존재하는지를 확인하는 함수이다.
'chall4'라는 세션 변수가 존재하는지를 확인하고, 'key'라는 변수가 'chall4'라는 세션 변수와 일치하면 된다.

```php
  $hash = rand(10000000,99999999)."salt_for_you";
  $_SESSION['chall4'] = $hash;
```

여기서 $hash는 12345678salt_for_you 와 같은 형태로 만들어진다.
그리고 그 값이 그대로 chall4에 담긴다.


```php
  for($i=0;$i<500;$i++) $hash = sha1($hash);
```

그렇게 만들어진 $hash 값을 sha1으로 500번 암호화시킨다.


이 문제를 풀기 위해서 레인보우 테이블을 떠올릴 수 있다.
단, 10000000salt_for_you부터 99999999salt_for_you까지의 모든 값을 500번 sha1 hash 암호화 시킨 값을 모두 받아두기에는 시간도 오래 걸리고 cpu에 부하도 많이 주게 된다.

이 문제를 풀기 위한 효율적인 방법을 구상하였다.

1. 10000000salt_for_you 부터 20000000salt_for_you까지 sha1으로 500번 암호화시킨 사전을 미리 만들어둔다.
2. 문제 페이지에 있는 값을 미리 생성해둔 사전에서 찾는다. (찾을 확률 10%)
3. 미리 생성해둔 사전에서 key를 찾을 수 없으면 문제 페이지를 새로고침하고 2번으로 되돌아간다.


이를 자동으로 찾기 위한 파이썬 스크립트를 작성하였다.


1번 과정:

```python

import hashlib, csv


chall4 = ""
f = open('rainbow.csv', 'a', newline='')
writer = csv.writer(f)

for i in range(10000000, 20000000):
  chall4 = str(i) + "salt_for_you"
  hash = ""

  for j in range(0, 500):
    tmphash = hashlib.sha1(chall4.encode('utf-8'))
    hash = tmphash.hexdigest()
    
  writer.writerow([chall4, hash])
  print(chall4 + " : " + hash)

f.close()

```

2번 과정:

```python

import hashlib, csv


f = open('rainbow.csv', 'r', newline='')
reader = csv.reader(f)
hash = "" # 문제 페이지의 hash값을 여기에 입력한다.

for line in reader:
  if line[1] == hash:
    print("I found the key! : " + line[0])

f.close()

```

