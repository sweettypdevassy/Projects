# GraphQL API with Spring Boot

This project demonstrates how to build a comprehensive GraphQL API using Spring Boot, JPA, and MySQL.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Steps to Set Up](#steps-to-set-up)
- [Detailed Implementation](#detailed-implementation)
- [Example GraphQL Queries](#example-graphql-queries)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)

## Prerequisites
- Java 17 or higher
- Maven 3.6+ or Gradle 7.0+
- MySQL 8.0+
- IDE (IntelliJ IDEA, Eclipse, or VS Code)

## Steps to Set Up

### 1. Create a Spring Boot Project
Use [Spring Initializr](https://start.spring.io/) and add these dependencies:
   * `spring-boot-starter-data-jpa`
   * `spring-boot-starter-graphql`
   * `spring-boot-starter-web`
   * `mysql-connector-j`
   * `lombok` (optional, for reducing boilerplate code)

### 2. Define Entities
Create `User` and `Order` entities with JPA annotations.

### 3. Create Repositories
Use `JpaRepository` to manage entities:

```java
public interface UserRepository extends JpaRepository<User, Long> {}
public interface OrderRepository extends JpaRepository<Order, Long> {}
```

### 4. Implement Services
Add business logic in service classes like `UserService`.

### 5. Add GraphQL Controllers
Use `@QueryMapping` and `@MutationMapping` annotations in `UserController`.

### 6. Define Schema
Add `schema.graphqls` in `src/main/resources`.

### 7. Configure Application
Enable GraphQL UI in `application.properties`:

```properties
spring.graphql.graphiql.enabled=true
```

### 8. Run and Test
   * Start the application: `mvn spring-boot:run`.
   * Test GraphQL queries at `/graphiql`.

## Detailed Implementation

### Step 1: Project Setup
1. Go to [Spring Initializr](https://start.spring.io/)
2. Set the following:
   - Project: Maven
   - Language: Java
   - Spring Boot: 3.1.0 or newer
   - Group: com.example
   - Artifact: graphql-api
   - Name: graphql-api
   - Package name: com.example.graphqlapi
   - Java: 17
3. Add dependencies:
   - Spring Web
   - Spring Data JPA
   - Spring for GraphQL
   - MySQL Driver
   - Lombok (optional)
4. Click "Generate" to download the project
5. Extract the ZIP file and open in your IDE

### Step 2: Configure Database
Create `application.properties` in `src/main/resources`:

```properties
# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/graphql_demo
spring.datasource.username=root
spring.datasource.password=your_password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA Configuration
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect

# GraphQL Configuration
spring.graphql.graphiql.enabled=true
spring.graphql.graphiql.path=/graphiql
spring.graphql.schema.printer.enabled=true
spring.graphql.cors.allowed-origins=*
```
### Step 3: Create Entity Classes
Create `User.java` in `src/main/java/com/example/graphqlapi/entity`:

```java
package com.example.graphqlapi.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.util.List;

@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long userId;
    
    private String name;
    
    @Column(unique = true)
    private String email;
    
    private String password;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Order> orders;
}
```

Create `Order.java` in the same package:

```java
package com.example.graphqlapi.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "orders")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long orderId;
    
    private String productName;
    
    private Double price;
    
    private LocalDateTime orderDate;
    
    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;
}
```

### Step 4: Create Repository Interfaces
Create `UserRepository.java` in `src/main/java/com/example/graphqlapi/repository`:

```java
package com.example.graphqlapi.repository;

import com.example.graphqlapi.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
}
```

Create `OrderRepository.java` in the same package:

```java
package com.example.graphqlapi.repository;

import com.example.graphqlapi.entity.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByUserUserId(Long userId);
}
```
