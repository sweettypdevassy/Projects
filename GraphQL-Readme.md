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
### Step 5: Create DTO Classes
Create DTO classes for input and output operations. Start with `src/main/java/com/example/graphqlapi/dto/UserInput.java`:

```java
package com.example.graphqlapi.dto;

import lombok.Data;

@Data
public class UserInput {
    private String name;
    private String email;
    private String password;
}
```

Create `OrderInput.java` in the same package:

```java
package com.example.graphqlapi.dto;

import lombok.Data;

@Data
public class OrderInput {
    private String productName;
    private Double price;
    private Long userId;
}
```

### Step 6: Create Service Classes
Create `UserService.java` in `src/main/java/com/example/graphqlapi/service`:

```java
package com.example.graphqlapi.service;

import com.example.graphqlapi.dto.UserInput;
import com.example.graphqlapi.entity.User;
import com.example.graphqlapi.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }
    
    public User createUser(UserInput userInput) {
        User user = new User();
        user.setName(userInput.getName());
        user.setEmail(userInput.getEmail());
        user.setPassword(userInput.getPassword()); // In production, use password encoder
        
        return userRepository.save(user);
    }
    
    public boolean deleteUser(Long id) {
        if (userRepository.existsById(id)) {
            userRepository.deleteById(id);
            return true;
        }
        return false;
    }
    
    public Optional<User> updateUser(Long id, UserInput userInput) {
        Optional<User> existingUser = userRepository.findById(id);
        
        if (existingUser.isPresent()) {
            User user = existingUser.get();
            
            if (userInput.getName() != null) {
                user.setName(userInput.getName());
            }
            
            if (userInput.getEmail() != null) {
                user.setEmail(userInput.getEmail());
            }
            
            if (userInput.getPassword() != null) {
                user.setPassword(userInput.getPassword()); // In production, use password encoder
            }
            
            return Optional.of(userRepository.save(user));
        }
        
        return Optional.empty();
    }
}
```

Create `OrderService.java` in the same package:

```java
package com.example.graphqlapi.service;

import com.example.graphqlapi.dto.OrderInput;
import com.example.graphqlapi.entity.Order;
import com.example.graphqlapi.entity.User;
import com.example.graphqlapi.repository.OrderRepository;
import com.example.graphqlapi.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class OrderService {
    
    @Autowired
    private OrderRepository orderRepository;
    
    @Autowired
    private UserRepository userRepository;
    
    public List<Order> getAllOrders() {
        return orderRepository.findAll();
    }
    
    public Optional<Order> getOrderById(Long id) {
        return orderRepository.findById(id);
    }
    
    public List<Order> getOrdersByUserId(Long userId) {
        return orderRepository.findByUserUserId(userId);
    }
    
    public Optional<Order> createOrder(OrderInput orderInput) {
        Optional<User> user = userRepository.findById(orderInput.getUserId());
        
        if (user.isPresent()) {
            Order order = new Order();
            order.setProductName(orderInput.getProductName());
            order.setPrice(orderInput.getPrice());
            order.setOrderDate(LocalDateTime.now());
            order.setUser(user.get());
            
            return Optional.of(orderRepository.save(order));
        }
        
        return Optional.empty();
    }
    
    public boolean deleteOrder(Long id) {
        if (orderRepository.existsById(id)) {
            orderRepository.deleteById(id);
            return true;
        }
        return false;
    }
}
```
### Step 7: Define GraphQL Schema
Create `schema.graphqls` in `src/main/resources/graphql`:

```graphql
type User {
    userId: ID!
    name: String!
    email: String!
    orders: [Order]
}

type Order {
    orderId: ID!
    productName: String!
    price: Float!
    orderDate: String!
    user: User!
}
input UserInput {
    name: String!
    email: String!
    password: String!
}

input OrderInput {
    productName: String!
    price: Float!
    userId: ID!
}
type Query {
    # User queries
    getUsers: [User]!
    getUser(userId: ID!): User
    
    # Order queries
    getOrders: [Order]!
    getOrder(orderId: ID!): Order
    getUserOrders(userId: ID!): [Order]!
}
type Mutation {
    # User mutations
    createUser(input: UserInput!): User!
    updateUser(userId: ID!, input: UserInput!): User
    deleteUser(userId: ID!): Boolean!
    
    # Order mutations
    createOrder(input: OrderInput!): Order
    deleteOrder(orderId: ID!): Boolean!
}
```
### Step 8: Create GraphQL Controllers
Create `UserController.java` in `src/main/java/com/example/graphqlapi/controller`:

```java
package com.example.graphqlapi.controller;

import com.example.graphqlapi.dto.UserInput;
import com.example.graphqlapi.entity.User;
import com.example.graphqlapi.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;
import java.util.Optional;

@Controller
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @QueryMapping
    public List<User> getUsers() {
        return userService.getAllUsers();
    }
    
    @QueryMapping
    public Optional<User> getUser(@Argument Long userId) {
        return userService.getUserById(userId);
    }
        @MutationMapping
    public User createUser(@Argument UserInput input) {
        return userService.createUser(input);
    }
    
    @MutationMapping
    public Optional<User> updateUser(@Argument Long userId, @Argument UserInput input) {
        return userService.updateUser(userId, input);
    }
    
    @MutationMapping
    public boolean deleteUser(@Argument Long userId) {
        return userService.deleteUser(userId);
    }
}
```
Create `OrderController.java` in the same package:

```java
package com.example.graphqlapi.controller;

import com.example.graphqlapi.dto.OrderInput;
import com.example.graphqlapi.entity.Order;
import com.example.graphqlapi.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;
import java.util.Optional;

@Controller
public class OrderController {
    
    @Autowired
    private OrderService orderService;
    
    @QueryMapping
    public List<Order> getOrders() {
        return orderService.getAllOrders();
    }
    
    @QueryMapping
    public Optional<Order> getOrder(@Argument Long orderId) {
        return orderService.getOrderById(orderId);
    }
    
    @QueryMapping
    public List<Order> getUserOrders(@Argument Long userId) {
        return orderService.getOrdersByUserId(userId);
    }
    
    @MutationMapping
    public Optional<Order> createOrder(@Argument OrderInput input) {
        return orderService.createOrder(input);
    }
    
    @MutationMapping
    public boolean deleteOrder(@Argument Long orderId) {
        return orderService.deleteOrder(orderId);
    }
}
```
### Step 9: Create DataFetchers (Optional for complex relationships)
If you need to customize how related entities are fetched, you can implement DataFetchers. Create `UserDataFetcher.java`:

```java
package com.example.graphqlapi.datafetcher;

import com.example.graphqlapi.entity.Order;
import com.example.graphqlapi.entity.User;
import com.example.graphqlapi.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.BatchMapping;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Component
public class UserDataFetcher {

    @Autowired
    private OrderService orderService;

    @BatchMapping
    public Map<User, List<Order>> orders(List<User> users) {
        return users.stream()
                .collect(Collectors.toMap(
                        user -> user,
                        user -> orderService.getOrdersByUserId(user.getUserId())
                ));
    }
}
```

### Step 10: Configure Main Application
Update `GraphqlApiApplication.java`:
