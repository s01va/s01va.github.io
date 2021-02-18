---
layout: single
title: "Nginx-Tomcat install & setting"
description:
date: 2021-02-16 10:17:00 -0400
# modified: 
tags:
- was
- nginx
- tomcat
- middleware
comments: true
share: true
---

모두 AWS 환경에서 설정하였다.

OS: Red Hat Ent 8.3.0

[구성도 추가하기]



- 모든 과정을 sudo 사용 대신 sudo su 이후 root로 진행

  (AWS서버에 접속 시 아예 keypair를 이용해서 로그인하므로 sudo 사용시 패스워드 입력이 어렵다.)

- 실제 운영환경 구성 전 연습 구성이므로, 실제로 컴파일 설치를 진행하였다.

  설치 경로는 모두 `/app/`




-------------------------------------------------------------

# WEB

## Nginx 설치

나는 컴파일 설치를 적용하였다.

redhat OS 설치 직후, 다음 유틸리티가 없을 수 있다. 설치해준다.

```shell
yum install -y vim
yum install -y wget
yum install -y gcc
yum install -y make
```

### 컴파일 설치

[Nginx download link](https://nginx.org/en/download.html)

1. stable 버전 중 최신 버전 링크를 사용하였다.

   ```shell
   wget https://nginx.org/download/nginx-1.18.0.tar.gz
   ```

   압축 해제 후 디렉토리명 변경

   기존 디렉토리명을 -source로 변경하고 nginx-1.18.0을 새로 만든다.

   nginx-1.18.0에 컴파일 결과물이 들어갈 예정

   ```shell
   tar -xvf nginx-1.18.0.tar.gz
   mv nginx-1.18.0/ nginx-1.18.0-source
   cd nginx-1.18.0-source
   ```

2. 설치 디렉토리 생성

   ```shell
   mkdir nginx-1.18.0
   ```

   

3. configure

   configure 하면서 여러가지 옵션을 넣어줄 수 있다.

   설치 경로도 지정할 수 있는데, 이렇게 지정해줄 수 있다.

   ```shell
   ./configure --prefix=/app/nginx-1.18.0
   ```

   

   이대로 그냥 configure를 시도하면 다음과 같은 경고문이 뜬다.

   ```
   ...
   checking for PCRE library ... not found
   checking for PCRE library in /usr/local/ ... not found
   checking for PCRE library in /usr/include/pcre/ ... not found
   checking for PCRE library in /usr/pkg/ ... not found
   checking for PCRE library in /opt/local/ ... not found
   
   ./configure: error: the HTTP rewrite module requires the PCRE library.
   You can either disable the module by using --without-http_rewrite_module
   option, or install the PCRE library into the system, or build the PCRE library
   statically from the source with nginx by using --with-pcre=<path> option.
   ```

   pcre 라이브러리를 연결해 주어야 한다. 다음과 같은 명령어로 pcre 라이브러리의 존재 유무를 확인하고 이의 경로를 확인한다.

   ```shell
   rpm -qa pcre # 라이브러리 존재 확인
   rpm -ql pcre # 경로 확인
   ```

   so 파일은 있으나 이를 활용할 수는 없다.

   pcre-devel을 설치한다.

   ```shell
   yum install -y pcre-devel
   ```

   설치 이후 `./configure --prefix=/app/nginx`를 시도하면 알아서 pcre를 잘 찾는 것을 볼 수 있다. 하지만 zlib에 대해 위와 동일한 현상이 발생한다.

   이 라이브러리도 so파일만 존재하여 devel을 설치했다.

   ```shell
   yum install -y zlib-devel
   ```

   

   ```shell
   ./configure --prefix=/app/nginx-1.18.0
   ```

   이제 문제없이 진행된다.

   ```
   ...
   Configuration summary
     + using system PCRE library
     + OpenSSL library is not used
     + using system zlib library
   ...
   ```

   

   configure가 완료되어 뜨는 summary중 이런 것이 있다.

   openssl도 설치하고 다시 configure를 진행하였다.

   ```shell
   yum install -y openssl-devel
   ./configure --prefix=/app/nginx-1.18.0 --with-http_ssl_module
   ```

   나중에 https를 사용할 수도 있으니 `--with-http_ssl_module` 옵션을 추가하였다.

   

4. make

   ```shell
   make
   make install
   ```

   이미 make를 많이 시도했다면, `make clean` 후 다시 make해 준다.

   ```shell
   make && make install
   ```

   이렇게 해도 됨

### 명령어만 총 정리

```shell
wget https://nginx.org/download/nginx-1.18.0.tar.gz
tar -xvf nginx-1.18.0.tar.gz
mv nginx-1.18.0/ nginx-1.18.0-source
mkdir nginx-1.18.0
cd nginx-1.18.0-source

yum install -y pcre-devel
yum install -y zlib-devel
yum install -y openssl-devel

./configure --prefix=/app/nginx-1.18.0 --with-http_ssl_module
make && make install
```



## 기동

```shell
cd /app/nginx/sbin
./nginx
```

AWS에서 해당 인스턴스 보안 그룹 설정-인바운드 규칙에서 80포트를 추가한다.

이제 해당 서버 DNS를 브라우저 주소창에 치면 nginx가 구동되어 있는 것을 볼 수 있다.

![0](https://s01va.github.io/assets/images/2021-01-28-Nginx-Tomcat-Kafka/0.png)

포트는 `/conf/nginx.conf`에서 변경할 수 있다.

## 종료

```shell
./nginx -s stop
```



### + yum 설치

[Nginx 공식 install 문서](https://www.nginx.com/resources/wiki/start/topics/tutorials/install/)

1. Yum repository에 nginx가 없어, repository 설정을 따로 해준다.

   `/etc/yum.repos.d/`에서 `nginx.repo`를 생성하고 아래와 같이 작성한다.

   ```shell
   vi /etc/yum.repos.d/nginx.repo
   ```
   
   ```
   [nginx]
   name=nginx repo
   baseurl=https://nginx.org/packages/rhel/8/x86_64/
   gpgcheck=0
   enabled=1
   ```
   
   
   
   공식문서의 `$releasever`, `$basearch` 부분은 자신의 설정 환경에 맞게 입력하였다.  

2. Nginx 설치

   ```shell
   yum install -y nginx
   ```

-------------------------------------

# WAS

## Tomcat 설치

자바 설치가 선행되어야 한다.

```shell
yum install -y java-1.8.0-openjdk
```

openjdk로 1.8을 설치하였다.

## 컴파일 설치

정해진 설치 경로 생성 및 이동

```shell
mkdir /app
cd /app
```

Tomcat 9버전 링크를 사용하였다.

```shell
wget https://downloads.apache.org/tomcat/tomcat-9/v9.0.43/bin/apache-tomcat-9.0.43.tar.gz
```

압축 해제 및 디렉토리명 변경

```shell
tar -xvf apache-tomcat-9.0.43.tar.gz
mv apache-tomcat-9.0.43/ tomcat9.0.43
```

정상 구동 여부 확인을 위해 `version.sh`로 확인한다.

(.bat 파일은 레드햇에서 필요 없어서 모두 삭제했다)

```shell
cd tomcat9.0.43/bin
./version.sh
```

구동!

```shell
./startup.sh
```



포트를 변경하지 않았다면 8080포트로 tomcat 기동을 확인할 수 있다.

![1](https://s01va.github.io/assets/images/2021-01-28-Nginx-Tomcat-Kafka/1.PNG)



## 배포

[여기](https://s01va.github.io/WAS-%ED%85%8C%EC%8A%A4%ED%8A%B8%EC%9A%A9-%EC%9B%B9-%EC%96%B4%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%A7%8C%EB%93%A4%EA%B8%B0/)에서 만든 웹 어플리케이션을 사용

디렉토리 째로 `$TOMCAT_HOME/webapps`에 이동시킨다.

배포 소스 디렉토리명이 webtest인데, tomcat 기동 이후 `[해당 host ip]:8080/webtest`로 접속하면 배포된 결과를 볼 수 있다.



--------------------------------------------------

# WEB-WAS 연동

## Nginx 설정

수정할 설정파일: `$NGINX_HOME/conf/nginx.conf`

나는 `[해당 host ip]/webtest`로 접속했을 때 webtest가 보이게 하고싶어서 아래와 같이 설정했다.

```shell
...
http {
	...
	server {
		...
		location /webtest {
			proxy_pass http://localhost:8080/webtest;
			proxy_set_header X-Forwarded-FOr $proxy_add_x_forwarded_for;
		}
		...
	}
	...
}
```

context root를 `/`로 설정하고 싶으면 `location / {}` 안에 설정해 준다.

## Tomcat 내 로그 설정

따로 설정을 고쳐주지 않으면, nginx를 통해 접속했을 시 로그가 nginx 웹서버의 로그로 남는다.

실제 클라이언트의 ip가 기록되도록 아래와 같이 설정을 바꾸어 준다.

수정할 설정 파일: `$TOMCAT_HOME/conf/server.xml`

수정할 원본 부분:

```xml
<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs" prefix="localhost_access_log" suffix=".txt" pattern="%h %l %u %t &quot;%r&quot; %s %b" />
```

`%h`에 ip값이 들어간다. 여기를 `%{x-forwarded-for}i`로 수정해 준다.

```xml
<Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs" prefix="localhost_access_log" suffix=".txt" pattern="%{x-forwarded-for}i %l %u %t &quot;%r&quot; %s %b" />
```

이제 로그에 클라이언트의 실제 ip가 기록된다.

----------------------

# Clustering

## Tomcat 설정

[참고 링크](https://shonm.tistory.com/m/641)

각 `<Engind>` 태그 하위에 아래와 같은 내용을 입력한다.

```xml
<Cluster 
    channelSendOptions="8" 
    channelStartOptions="3" 
    className="org.apache.catalina.ha.tcp.SimpleTcpCluster">
    <Manager 
        className="org.apache.catalina.ha.session.DeltaManager" 
        expireSessionsOnShutdown="false" 
        notifyListenersOnReplication="true"
    />
    <Channel className="org.apache.catalina.tribes.group.GroupChannel">
        <Sender className="org.apache.catalina.tribes.transport.ReplicationTransmitter">
            <Transport className="org.apache.catalina.tribes.transport.nio.PooledParallelSender" />
        </Sender>
        <Receiver 
            address=""
            autoBind="0" 
            className="org.apache.catalina.tribes.transport.nio.NioReceiver" 
            maxThreads="6" 
            port="3100" 
            selectorTimeout="5000"
        /> <!-- server1 information -->
        <!-- <Interceptor className="com.dm.tomcat.interceptor.DisableMulticastInterceptor" /> -->
        <Interceptor className="org.apache.catalina.tribes.group.interceptors.TcpPingInterceptor" staticOnly="true"/>
        <Interceptor className="org.apache.catalina.tribes.group.interceptors.TcpFailureDetector" />
        <Interceptor className="org.apache.catalina.tribes.group.interceptors.StaticMembershipInterceptor">
            <Member 
                className="org.apache.catalina.tribes.membership.StaticMember" 
                port="3100" 
                host="" 
                uniqueId="{0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1}" 
            /> <!-- server2 -->
            <Member 
                className="org.apache.catalina.tribes.membership.StaticMember" 
                port="3100" 
                host="" 
                uniqueId="{0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2}" 
            /> <!-- server3 -->
        </Interceptor>
        <Interceptor className="org.apache.catalina.tribes.group.interceptors.MessageDispatchInterceptor" />
    </Channel>
    <Valve 
        className="org.apache.catalina.ha.tcp.ReplicationValve" 
        filter=".*\.gif;.*\.js;.*\.jpg;.*\.png;.*\.htm;.*\.html;.*\.css;.*\.txt;" 
    />
    <ClusterListener className="org.apache.catalina.ha.session.ClusterSessionListener" />
</Cluster>
```

`<Receiver>`, `<Member>` 태그 안의 정보를 고쳐주어야 한다.

각 세 서버에 아래와 같이 입력하였다.

편의상 1, 2, 3으로 기입함

|                               |       Web/WAS 1       |       Web/WAS 2       |       Web/WAS 3       |
| :---------------------------: | :-------------------: | :-------------------: | :-------------------: |
|    `<Receiver address="">`    |         1 ip          |         2 ip          |         3 ip          |
|   first `<Member host="">`    |         2 ip          |         3 ip          |         1 ip          |
| first `<Member uniqueId="">`  | {0, 0, ... , 0, 1, 2} | {0, 0, ... , 0, 1, 3} | {0, 0, ... , 0, 1, 1} |
|   second `<Member host="">`   |         3 ip          |         1 ip          |         2 ip          |
| second `<Member uniqueId="">` | {0, 0, ... , 0, 1, 3} | {0, 0, ... , 0, 1, 1} | {0, 0, ... , 0, 1, 2} |



모두 포트는 3100으로 통일했고(다른 포트도 무방)

aws내 보안그룹 인바운드 규칙 설정에서 해당 포트를 열어주면 된다.

소스는 서로의 보안그룹으로 설정해줌(최소한에게 포트를 오픈하기 위함)



## Clustering된 Tomcat과 Nginx 연동 설정

수정할 Nginx 설정 파일: `$NGINX_HOME/conf/nginx.conf`

`http` 하위 블록으로 `upstream`을 만들어 주고, 연동시킬 tomcat cluster 정보를 입력한다.

- upstream 뒤에 붙는 이름은 자유

- load balancing 방법을 기입

  [참고](http://nginx.org/en/docs/http/load_balancing.html)

  round robin, least connection, ip hash 셋 중 하나를 선택할 수 있다. 중복 안됨

  sticky session 기능은 nginx plus에서만 제공한다.

  nginx에서는 이를 ip_hash로 대신함

- server 뒤에 tomcat 서버들 정보를 하나씩 입력한다.

`server` 하위 블록의 `location [/context_root]`에 썼던 내용을 일부 수정한다.

- proxy_pass http://[tomcat cluter 이름];
- `proxy_set_header Host $host;` 추가
- `proxy_set_header X-Real-IP $remote_addr;` 추가

위의 proxy_set_header 설정을 추가하지 않으면 header값을 제대로 전달하지 못해서 tomcat cluster와 연동에 지대로 되지 않는다.

```shell
...
http {
	...
	upstream [tomcat cluter 이름] {
		ip_hash;
		server [web/was 1번서버 ip]:[tomcat_port(8080)];
		server [web/was 2번서버 ip]:[tomcat_port(8080)];
		server [web/was 3번서버 ip]:[tomcat_port(8080)];
	}
	server {
		...
		location /webtest {
			proxy_pass http://[tomcat cluter 이름];
			proxy_set_header X-Forwarded-FOr $proxy_add_x_forwarded_for;
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
		}
		...
	}
	...
}
```

이제 1번 서버 nginx(http://[web/WAS IP]:80)로 접속 테스트를 하면, 2번 3번 서버의 tomcat을 연결해서 보여주기도 하는 것을 볼 수 있다.

