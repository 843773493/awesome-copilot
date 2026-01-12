

---
agent: 'agent'
description: '创建Spring Boot Java项目骨架'
---

# 创建Spring Boot Java项目提示

- 请确保您的系统已安装以下软件：

  - Java 21
  - Docker
  - Docker Compose

- 如果需要自定义项目名称，请在[download-spring-boot-project-template](./create-spring-boot-java-project.prompt.md#download-spring-boot-project-template)中修改`artifactId`和`packageName`

- 如果需要更新Spring Boot版本，请在[download-spring-boot-project-template](./create-spring-boot-java-project.prompt.md#download-spring-boot-project-template)中修改`bootVersion`

## 检查Java版本

- 在终端中运行以下命令以检查Java版本

```shell
java -version
```

## 下载Spring Boot项目模板

- 在终端中运行以下命令以下载Spring Boot项目模板

```shell
curl https://start.spring.io/starter.zip \
  -d artifactId=${input:projectName:demo-java} \
  -d bootVersion=3.4.5 \
  -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,data-redis,data-mongodb,validation,cache,testcontainers \
  -d javaVersion=21 \
  -d packageName=com.example \
  -d packaging=jar \
  -d type=maven-project \
  -o starter.zip
```

## 解压下载的文件

- 在终端中运行以下命令以解压下载的文件

```shell
unzip starter.zip -d ./${input:projectName:demo-java}
```

## 删除下载的zip文件

- 在终端中运行以下命令以删除下载的zip文件

```shell
rm -f starter.zip
```

## 切换到项目根目录

- 在终端中运行以下命令以切换到项目根目录

```shell
cd ${input:projectName:demo-java}
```

## 添加额外依赖

- 将`springdoc-openapi-starter-webmvc-ui`和`archunit-junit5`依赖项插入到`pom.xml`文件中

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
  <version>2.8.6</version>
</dependency>
<dependency>
  <groupId>com.tngtech.archunit</groupId>
  <artifactId>archunit-junit5</artifactId>
  <version>1.2.1</version>
  <scope>test</scope>
</dependency>
```

## 添加SpringDoc、Redis、JPA和MongoDB配置

- 将SpringDoc配置插入到`application.properties`文件中

```properties
# SpringDoc配置
springdoc.swagger-ui.doc-expansion=none
springdoc.swagger-ui.operations-sorter=alpha
springdoc.swagger-ui.tags-sorter=alpha
```

- 将Redis配置插入到`application.properties`文件中

```properties
# Redis配置
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.password=rootroot
```

- 将JPA配置插入到`application.properties`文件中

```properties
# JPA配置
spring.datasource.driver-class-name=org.postgresql.Driver
spring.datasource.url=jdbc:postgresql://localhost:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=rootroot
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
```

- 将MongoDB配置插入到`application.properties`文件中

```properties
# MongoDB配置
spring.data.mongodb.host=localhost
spring.data.mongodb.port=27017
spring.data.mongodb.authentication-database=admin
spring.data.mongodb.username=root
spring.data.mongodb.password=rootroot
spring.data.mongodb.database=test
```

## 在docker-compose.yaml中添加Redis、PostgreSQL和MongoDB服务

- 在项目根目录创建`docker-compose.yaml`文件，并添加以下服务：`redis:6`、`postgresql:17`和`mongo:8`。

  - Redis服务应包含：
    - 密码`rootroot`
    - 映射端口6379到6379
    - 挂载卷`./redis_data`到`/data`
  - PostgreSQL服务应包含：
    - 密码`rootroot`
    - 映射端口5432到5432
    - 挂载卷`./postgres_data`到`/var/lib/postgresql/data`
  - MongoDB服务应包含：
    - 初始化数据库的root用户名`root`
    - 初始化数据库的root密码`rootroot`
    - 映射端口27017到27017
    - 挂载卷`./mongo_data`到`/data/db`

## 添加.gitignore文件

- 将`redis_data`、`postgres_data`和`mongo_data`目录添加到`.gitignore`文件中

## 运行Maven测试命令

- 运行Maven clean test命令以检查项目是否正常运行

```shell
./mvnw clean test
```

## 运行Maven运行命令（可选）

- （可选）使用`docker-compose up -d`启动服务，`./mvnw spring-boot:run`运行Spring Boot项目，`docker-compose rm -sf`停止服务。

## 让我们逐步进行这些步骤