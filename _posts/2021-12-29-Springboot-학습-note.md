---
layout: single
title: "Springboot 학습 note"
description: "개념적 이해와 정리가 필요한 것들 주로 노트"
date: 2021-12-29 12:00:00 -0400
# modified: 
tags: 
- springboot
- jpa
comments: true
share: true
toc_sticky: true

---



학습중인 서적: [스프링 부트와 AWS로 혼자 구현하는 웹 서비스](http://www.kyobobook.co.kr/product/detailViewKor.laf?ejkGb=KOR&mallGb=KOR&barcode=9788965402602)

Java로 웹을 전부 다 만들어본게 처음이라 러닝커브는 조금 있었다.

예전엔 어떻게 썼었다는 바탕이 거의 없는 상태였으나 따라하고 익히기에 무리는 없었음

과거의 개발 방식 등의 지식이 있는 사람은 훨씬 더 쉽게 익힐 것 같다.

굳

-------------

## JPA를 왜 사용하는가

*객체 지향의 Java와 관계형 데이터베이스의 패러다임 불일치를 해소하기 위해*

== SQL에 종속적이지 않기 위해

개발자는 개발자대로 객체지향적인 프로그래밍을 하고, 저런 패러다임 간극을 메꾸는 일은 JPA에게 맡긴다.

운영중에 쿼리문에 잡아먹힌 소스를 많이 보긴 했었다. 웹개발 하러 들어갔다가 쿼리짜는 기계가 되어서 나왔다는 친구들도 있고... 괜찮은 선택지인 것 같다



## Domain

도메인이란, 소프트웨어에 대한 요구사항 혹은 문제 영역을 의미

ex) 게시글, 회원, 정산, 결제 등



## Entity

DB 테이블에 직접적으로 링크될 클래스

테이블 설계==Entity 설계

참고: [DAO, DTO, VO, Entity 차이](https://velog.io/@ha0kim/DAO-DTO-VO-%EC%B0%A8%EC%9D%B4)

Entity 클래스를 Request/Response 클래스로 사용하지 않기 -> DTO로 뺀다.

Request/Response용 클래스는 **View를 위한 것**.

그리고 DTO는 getter/~~setter~~builder 역할만 한다.

**View Layer와 DB Layer는 철저히 분리되어야 한다**



## Getter/Setter/Builder

Entity 클래스 작성 시, getter는 어노테이션 하나로 자동 생성(`@Getter`)

**Setter는 절대 사용하지 않고**, 대신 builder를 사용

setter는 해당 entity 클래스의 인스턴스 값들이 **언제 어떻게 DB 테이블로 들어가는지 명확하게 알기 힘들게 한다**.

builder를 사용하면 어느 필드에 어떤 값이 들어가는지 명확해진다.

- Setter 예시 코드

  ```java
  // Setter 사용 시
  public Example(String a, String b) {
      this.a = a;
      this.b = b;
  }
  ```

  `Example(b, a)` 이런 식으로 사용하면 뭐가 문제인지 알기 힘듬

  클래스를 쓸 때 테이블 컬럼에 값을 넣는 게 명시되어있지 않아서 값 입력 순서에만 의존해야 함

- Builder 예시 코드

  ```java
  // Builder 사용 시
  Example.builder()
      .a(a)	// a 컬럼에 a 값을 넣고
      .b(b)	// b 컬럼에 b 값을 넣고
      .build();
  // 명확하다!
  ```



## Repository

여기서는 인터페이스로 생성하는 **JPA Repository**. 舊 DAO. DB 레이어 접근자

JpaRepository를 상속하면 CRUD 메소드가 자동으로 생성됨



## Spring Web Layer

![final spring web layer](https://www.petrikainulainen.net/wp-content/uploads/spring-web-app-architecture.png)

Service는 트랜잭션, 도메인 간 순서 보장만 한다. **여기서 비즈니스 로직을 처리하지 않는다.**

비즈니스 로직 처리는 domain이 한다.


