---
layout: single
title: "CodeEngn Basic 17"
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
---

Key 값이 BEDA-2F56-BC4F4368-8A71-870B 일때 Name은 무엇인가 
힌트 : Name은 한자리인데.. 알파벳일수도 있고 숫자일수도 있고.. 
정답인증은 Name의 MD5 해쉬값(대문자)

![crackme](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/0.png)

Name과 Key를 입력하는 프로그램이다.

![PEiD](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/1.png)

델파이로 작성되었으며, 패킹은 되어있지 않다. 그대로 분석을 진행한다.

![crackme inpug](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/2.png)

A와 12345를 입력하였더니 ‘Please Enter More Chars…’라는 문자열이 떴다. 이를 바탕으로 스트링을 검색하여 해당 주소지들을 찾았다. Name이 30자 이하가 되어야 한다는 것도 추가적으로 알 수 있다.

![string ascii](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/3.png)

다음은 정답 판별 부분이다.

![into good boy](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/4.png)

그리고 그 위에는 다음과 같은 부분들이 있다.

![up1](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/5.png)

![up2](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/6.png)

“Please Enter More Chars…” 파트를 넘기 위해서는 EAX가 3이어야 한다. 프로그램을 실행시켜 보며 분석한 결과 Name이 3글자 이상이어야 EAX가 3이 되는 것을 확인할 수 있었다. 문제에서 Name은 한글자라고도 하였으니 이 조건을 모두 만족시켜줄 Name의 조건을 찾아보려 하였으나 별다른 해결책을 찾지 못하였다. 간단하게 “CMP EAX,3” 부분을 “CMP EAX,1”로 코드패치 하여 덤프를 뜬 이후 진행하였다. 

![change eax](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/7.png)

EAX와 EDX 값을 비교하여 정답 여부를 확인하는 것을 볼 수 있다. 저 지점까지 도달하면 EDX에는 아래와 같이 정답 키 값이 들어가 있다.

![reg](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/8.png)

이제부터 Name에 무엇을 넣어야 키 값이 BEDA-2F56-BC4F4368-8A71-870B이 되는지를 추적해 보도록 하겠다.

![name](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/9.png)

재실행시켜 해당 지점까지 실행시켰을 때 이미 Name을 통해 만들어낸 키값은 LOCAL.5에 생성되어 있으며 이를 EDX로 MOV하고 있다.

![mov edx](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/10.png)

몇 줄 위에서 LEA에서 LOCAL.5의 주소지를 EDX로 받아오고 있고, 45B850 함수를 통과한 이후 제대로 된 키값을 받아오는 것을 볼 수 있었다. 함수 45B850의 내부로 들어가서 관찰하도록 한다.

![make key](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/11.png)

해당 함수 내부에서 한줄씩 실행시키다 보면 어떤 유사한 부분이 반복되며 키를 한 파트씩 생성해 내는 것을 볼 수 있었다. 모두 동일하게 4086C8 함수를 통과하면 특정 문자열을 로컬 변수에 저장하는 것을 볼 수 있었다.

![after loop](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/12.png)

반복되는 구간을 모두 지나오면 스택에 키값의 조각들이 쌓여있는 것을 볼 수 있다. 이 반복되는 부분을 분석해 보도록 하겠다.

![arg1](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/13.png)

Arg1 부분만 바뀌고 위와 같은 부분이 계속 반복되는 것을 확인할 수 있었다. Name에 “A”를 입력하고 다음과 같은 연산들을 반복했을 시 나타나는 최종 키값은 FFE3-2C73-0502A34C-8A48-E1CB이었다. 이 키값이 만들어지는 과정을 뜯어보면 다음과 같다.

![local.7](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/14.png)

LOCAL.7(== 주소지19F5FC)가 Arg1로 들어가서 ESI(==FFE374F0)를 기반으로 맨 앞의 문자열 “FFE3”을 만들어 낸다(함수 1이라 칭함).

![local.9](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/15.png)

LOCAL.9(== 주소지19F5F4)가 Arg1로 들어가서 LOCAL.4(==02C733B4)를 기반으로 두 번째 문자열 “2C73”을 만들어 낸다(함수 2라 칭함).

![local.11](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/16.png)

LOCAL.11(== 주소지 19F5EC)가 Arg1로 들어가서 LOCAL.2(== 0502A34CDF1251DEE5DC2EC8D 3FC7510) 를 기반으로 세번째 문자열 “0502A34C”를 만들어 낸다(함수 3이라 칭함).

![local.12, local.14](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/17.png)

네 번째, 다섯 번째 문자열은 첫 번째, 두번째 문자열을 만드는 과정과 동일하다(함수 4,5라 칭함). 단 Arg1값과 최종적으로 만들어질 문자열이 참고하는 지점이 다르다. 이와 같은 과정을 표로 정리하면 다음과 같다.

| Arg1 | 참고 지점 | 최종 문자열 |
| -- | -- | -- |
| LOCAL.7(==19F5F8) | ESI(==FFE374F0) | FFE3 |
| LOCAL.9(==19F5F0) | LOCAL.4(==02C733B4) | 2CF3 |
| LOCAL.11(==19F5E8) | LOCAL.2(==0502A34CD…) | 0502A34C |
| LOCAL.12(==19F5E4) | EDI(==08A48A32) | 8A48 |
| LOCAL.14(==19F5DC) | EBX(==E1CBC640) | E1CB |


다음은 문자열 “B”를 넣었을 때를 관찰한 결과이다.


| Arg1 | 참고 지점 | 최종 문자열 |
| -- | -- | -- |
| LOCAL.7(==19F5F8) | ESI(==A27E1920) | A27E |
| LOCAL.9(==19F5F0) | LOCAL.4(==02D07038) | 2D07 |
| LOCAL.11(==19F5E8) | LOCAL.2(==BA91EB0637…) | BA91EB06 |
| LOCAL.12(==19F5E4) | EDI(==08A50DC4) | 8A50 |
| LOCAL.14(==19F5DC) | EBX(==A5D4EC81) | A5D4 |


Arg1과 참고 지점은 같으나, 참고 지점에 들어가는 문자열이 다름으로 인해 최종 결과 키값이 달라지는 것을 확인할 수 있었다. 이를 통해 미리 해당 키값들이 저장되어 있고, Name에 따라 미리 저장된 키값을 찾아가서 조합하는 것이 아니라, Name에 들어오는 문자열을 바탕으로 연산을 수행해서 스택에 저장하는 것임을 짐작할 수 있다. 다음으로는 위의 키 값이 만들어지는 다섯 파트의 바깥 부분을 관찰하였다.

![first stack](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/18.png)

이 45B850함수의 첫 부분과 스택을 쌓는 부분이다. PUSH 0을 반복하여 LOCAL.1부터 LOCAL.14까지 쌓는 것을 볼 수 있다.

![all stack](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/19.png)

위의 PUSH를 반복하는 부분을 모두 지나고 나서 쌓인 스택의 모습이다. 19F614부터 LOCAL.1이다. 스택을 쌓은 후, ESI, EDI, EBX를 생성한다.

![ESI](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/20.png)

![EDI](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/21.png)

![EBX](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/22.png)

위에서부터 ESI, EDI, EBX의 값이 결정되는 부분이다. ESI 값이 생성되는 과정부터 분석해 보겠다.

![making ESI 1](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/23.png)

![making ESI 2](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/24.png)

ESI 생성 과정과 그 시작 부분의 레지스터 값들이다. LOCAL.1에는 23350E8이 들어 있다. 다음은 각 어셈블리어 코드 한줄 한줄 진행 과정에 따른 분석이다.

| MOV EBX,DWORD PTR SS:[LOCAL.1] | EBX에 23350E8을 넣는다. |
MOVZX ESI,BYTE PTR DS:[ECX+EBX-1] | ESI에 ECX+EBX-1 주소지에 들어있는 값을 넣는다. ECX가 1이므로 EBX 주소지에 있는 값을 그대로 ESI에 넣게 된다. 이 주소지에는 41이라는 값이 들어 있으므로, | ESI는 41이 된다. |
| ADD ESI,EDX | ESI와 EDX를 더해서 ESI에 넣는다. EDX는 0이므로 ESI는 그대로 41이 된다. |
| IMUL ESI,ESI,772 | ESI와 772를 곱한 결과를 ESI에 넣는다. ESI에는 1E3F2가 담긴다. |
| MOV EDX,ESI | EDX에 ESI에 있는 1E3F2를 넣는다. |
IMUL EDX,ESI | EDX와 ESI를 곱한 결과를 EDX에 넣는다. 1E3F2의 제곱인  392DB10C4가 들어가야 | 하지만 3이 잘리므로 결과적으로 92DB10C4가 EDX에 들어가게 된다. |
ADD ESI,EDX | ESI와 EDX를 더한 결과를 ESI에 넣는다. 1E3F2와 92DB10C4를 더하므로 ESI에는 | 92DCF4B6이 들어가게 된다. |
| OR ESI,ESI | ESI와 ESI를 OR연산을 하면 값이 그대로 유지된다. |
IMUL ESI,ESI,474 | ESI와 474를 곱한 값이 ESI에 담긴다. 92DCF4B6과 474를 곱하면 28DFFF1BA78이 | 되지만 28D가 잘리므로 FFF1BA78이 ESI에 담기게 된다. |
ADD ESI,ESI | FFF1BA78의 두 배인 값이 ESI에 담긴다. 1FFE374F0이 결과이나 1이 잘려 FFE374F0이 | ESI에 담긴다. |
| MOV EDX,ESI | EDX에 ESI값을 넣는다. EDX에 FFE374F0이 담긴다. |
| INC ECX | ECX에 1을 더한다. 2가 ECX에 담긴다. |
| DEC EAX | EAX에 1을 뺀다. 0이 EAX에 담긴다. |


이렇게 ESI에 담긴 FFE374F0의 앞 4자리는 그대로 시리얼 키의 맨 앞인 FFE3이 된다. 위의 알고리즘을 보면 결국 LOCAL.1에 담겨 있는 주소지, 즉 23350E8에 어떤 수가 들어 있느냐에 따라 최종 시리얼 키의 맨 앞자리 값이 바뀐다는 결론을 내릴 수 있다. Name에 넣은 A는 아스키코드로 65, 16진수로 41이다. 시험삼아 Name에 B를 넣고 23350E8를 확인해 보니 42가 담겨 있었다. 즉, Name에 들어간 아스키 코드에 따라 최종 시리얼 키의 맨 앞자리 값이 결정된다. 위의 루틴에 따라 아래와 같은 파이썬 코드를 작성하였다.

```python
namecode = 0x21
while (namecode < 0x7f):
	esi = namecode
	esi = esi * 0x772
	edx = esi
	edx = edx * esi
	if (edx > 0xffffffff):
		edx = edx % 0x100000000
	esi = edx + esi
	esi = esi * 0x474
	if (esi > 0xffffffff):
		esi = esi % 0x100000000
	esi = 2 * esi
	if (esi > 0xffffffff):
		esi = esi % 0x100000000
	print hex(esi)
	if (esi >= 0xbeda0000 and esi < 0xbedb0000):
		print "Find it!"
		print hex(esi)
		print "Name is " + chr(namecode)
		break;
	namecode = namecode + 1
```

Name은 F가 나왔다. 이를 확인해 보았다.

![well done](https://s01va.github.io/assets/images/2015-07-21-CodeEngn-Basic-17/25.png)

정답은 Name의 md5 hash값이다.

정답: 800618943025315f869e4e1f09471012