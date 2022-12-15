---
layout: single
title: "Docker <none> <none> 이미지 삭제"
description: ""
date: 2022-12-15 11:00:00 -0400
# modified: 
tags: 
- docker
comments: true
share: true
toc_sticky: true
---





도커 사용중에 생겨서 쌓이는 Repository \<none\> tag \<none\> 이미지들 한번에 삭제하기

```bash
docker rmi $(docker images -f "dangling=true" -q)
```

