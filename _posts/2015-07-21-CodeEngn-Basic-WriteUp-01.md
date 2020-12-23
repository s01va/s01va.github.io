---
layout: single
title: "CodeEngn Basic 01"
#description: ""
date: 2015-07-21 12:00:00 -0400
# modified: 
tags: 
- wargame
- writeup
- reversing
- codeengn-basic
comments: true
share: true
toc: true
toc_sticky: true
---

HDD를 CD-Rom으로 인식시키기 위해서는 GetDriveTypeA의 리턴값이 무엇이 되어야 하는가


![cp]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-01/0.png)

JE 파트를 보면, EAX와 ESI가 같을 시, HDD를 CD-Rom으로 인식하겠다는 창이 뜬다. 이 EAX와 ESI값은 위에서 GetDriveTypeA함수를 지나면서 결정된다.

![reg]({{site.url}}{{site.baseurl}}/assets/images/2015-07-21-CodeEngn-Basic-01/1.png)

GetDriveTypeA를 지나고 나면 EAX값이 3으로 되어있는데, CMP를 할 때 ESI값이 401003이다. GetDriveTypeA를 지난 이후 EAX는 2만큼 감소, ESI는 3만큼 증가한다. 즉 GetDriveTypeA 함수를 지난 직후 ESI는 401000이며, EAX는 그것보다 5만큼 큰 401005가 되어야 할 것이다. 그리고 함수의 리턴값은 EAX에 저장되므로, HDD를 CD-Rom으로 인식시키기 위한 GetDriveTypeA의 리턴값은 401005가 되어야 한다.
그러나 답이 맞지 않는 경우가 발생하는데, 그렇지 않아도 Entry point alert가 뜬다.. PSAPI의 entry point가 코드 외부에 있다는 것. 진짜 API를 사용하는 것으로 보이는데, 컴퓨터의 버전을 타는 것으로 추정된다. 답이 다를 수밖에 없는 문제라고 판단을 내림.

정답은 5


| Return code/value	Description |
| -- | -- |
| DRIVE_UNKNOWN 0	| The drive type cannot be determined. |
| DRIVE_NO_ROOT_DIR 1	| The root path is invalid; for example, there is no volume mounted at the specified path. |
| DRIVE_REMOVABLE 2	| The drive has removable media; for example, a floppy drive, thumb drive, or flash card | reader. |
| DRIVE_FIXED 3	| The drive has fixed media; for example, a hard disk drive or flash drive. |
| DRIVE_REMOTE 4	| The drive is a remote (network) drive. |
| DRIVE_CDROM 5	| The drive is a CD-ROM drive. |
| DRIVE_RAMDISK 6	| The drive is a RAM disk. |


출처: https://msdn.microsoft.com/ko-kr/library/windows/desktop/aa364939(v=vs.85).aspx
