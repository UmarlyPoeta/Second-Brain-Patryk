# ⚡ gRPC - Google Remote Procedure Call

## 📖 Definicja

**gRPC** to nowoczesny, open-source RPC framework rozwinięty przez Google. Wykorzystuje Protocol Buffers (protobuf) i HTTP/2 do szybkiej, wydajnej komunikacji między serwisami.

## 🆚 gRPC vs REST

| Aspekt | gRPC | REST |
|--------|------|------|
| **Protokół** | HTTP/2 | HTTP/1.1 |
| **Format** | Protocol Buffers (binary) | JSON (text) |
| **API Contract** | .proto files (strict) | OpenAPI (optional) |
| **Performance** | Bardzo szybki | Dobry |
| **Streaming** | Built-in (4 typy) | Trudny |
| **Browser Support** | Limited (gRPC-Web) | Native |
| **Code Generation** | Automatyczny | Optional |
| **Use Case** | Microservices, internal | Public APIs |

## 📦 Protocol Buffers

### Definicja .proto
```protobuf
// user.proto
syntax = "proto3";

package user;

option java_package = "com.example.user";
option java_multiple_files = true;

// Message definition
message User {
  int64 id = 1;
  string name = 2;
  string email = 3;
  repeated string roles = 4;
  google.protobuf.Timestamp created_at = 5;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
  string password = 3;
}

message CreateUserResponse {
  User user = 1;
  string message = 2;
}

message GetUserRequest {
  int64 id = 1;
}

message ListUsersRequest {
  int32 page = 1;
  int32 limit = 2;
}

message ListUsersResponse {
  repeated User users = 1;
  int32 total = 2;
}

message DeleteUserRequest {
  int64 id = 1;
}

message DeleteUserResponse {
  bool success = 1;
}

// Service definition
service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
  
  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream User);
  
  // Client streaming
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUserResponse);
  
  // Bidirectional streaming
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
}

message ChatMessage {
  string user_id = 1;
  string text = 2;
  int64 timestamp = 3;
}
```

## 🔄 Typy Komunikacji

### 1. Unary RPC (Standardowy)
```
Client → Request → Server
Client ← Response ← Server

Jak zwykłe wywołanie funkcji
```

### 2. Server Streaming
```
Client → Request → Server
Client ← Stream  ← Server
Client ← Stream  ← Server
Client ← Stream  ← Server

Przykład: Pobieranie dużej listy danych
```

### 3. Client Streaming
```
Client → Stream  → Server
Client → Stream  → Server
Client → Stream  → Server
Client ← Response ← Server

Przykład: Upload wielu plików
```

### 4. Bidirectional Streaming
```
Client ↔ Stream ↔ Server
       ↔ Stream ↔
       ↔ Stream ↔

Przykład: Chat, real-time collaboration
```

## 💻 Implementacja

### Java (Spring Boot)

**1. Dodaj dependencies:**
```xml
<dependency>
    <groupId>net.devh</groupId>
    <artifactId>grpc-spring-boot-starter</artifactId>
    <version>2.15.0.RELEASE</version>
</dependency>
<dependency>
    <groupId>io.grpc</groupId>
    <artifactId>grpc-protobuf</artifactId>
    <version>1.58.0</version>
</dependency>
<dependency>
    <groupId>io.grpc</groupId>
    <artifactId>grpc-stub</artifactId>
    <version>1.58.0</version>
</dependency>
```

**2. Server Implementation:**
```java
@GrpcService
public class UserServiceImpl extends UserServiceGrpc.UserServiceImplBase {
    
    @Autowired
    private UserRepository userRepository;
    
    // Unary RPC
    @Override
    public void getUser(GetUserRequest request, 
                       StreamObserver<User> responseObserver) {
        User user = userRepository.findById(request.getId())
            .map(this::toProto)
            .orElseThrow(() -> new StatusException(Status.NOT_FOUND));
        
        responseObserver.onNext(user);
        responseObserver.onCompleted();
    }
    
    @Override
    public void createUser(CreateUserRequest request,
                          StreamObserver<CreateUserResponse> responseObserver) {
        try {
            com.example.entity.User entity = new com.example.entity.User();
            entity.setName(request.getName());
            entity.setEmail(request.getEmail());
            
            entity = userRepository.save(entity);
            
            CreateUserResponse response = CreateUserResponse.newBuilder()
                .setUser(toProto(entity))
                .setMessage("User created successfully")
                .build();
            
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        } catch (Exception e) {
            responseObserver.onError(
                Status.INTERNAL
                    .withDescription(e.getMessage())
                    .asException()
            );
        }
    }
    
    // Server Streaming
    @Override
    public void listUsers(ListUsersRequest request,
                         StreamObserver<User> responseObserver) {
        Pageable pageable = PageRequest.of(
            request.getPage(), 
            request.getLimit()
        );
        
        Page<com.example.entity.User> users = 
            userRepository.findAll(pageable);
        
        users.forEach(user -> {
            responseObserver.onNext(toProto(user));
        });
        
        responseObserver.onCompleted();
    }
    
    // Client Streaming
    @Override
    public StreamObserver<CreateUserRequest> createUsers(
            StreamObserver<CreateUserResponse> responseObserver) {
        
        return new StreamObserver<CreateUserRequest>() {
            private final List<com.example.entity.User> users = 
                new ArrayList<>();
            
            @Override
            public void onNext(CreateUserRequest request) {
                com.example.entity.User user = 
                    new com.example.entity.User();
                user.setName(request.getName());
                user.setEmail(request.getEmail());
                users.add(user);
            }
            
            @Override
            public void onError(Throwable t) {
                log.error("Error in client streaming", t);
            }
            
            @Override
            public void onCompleted() {
                List<com.example.entity.User> savedUsers = 
                    userRepository.saveAll(users);
                
                CreateUserResponse response = 
                    CreateUserResponse.newBuilder()
                        .setMessage(savedUsers.size() + " users created")
                        .build();
                
                responseObserver.onNext(response);
                responseObserver.onCompleted();
            }
        };
    }
    
    // Bidirectional Streaming
    @Override
    public StreamObserver<ChatMessage> chat(
            StreamObserver<ChatMessage> responseObserver) {
        
        return new StreamObserver<ChatMessage>() {
            @Override
            public void onNext(ChatMessage message) {
                // Broadcast do wszystkich
                ChatMessage response = ChatMessage.newBuilder()
                    .setUserId(message.getUserId())
                    .setText("Echo: " + message.getText())
                    .setTimestamp(System.currentTimeMillis())
                    .build();
                
                responseObserver.onNext(response);
            }
            
            @Override
            public void onError(Throwable t) {
                log.error("Chat error", t);
            }
            
            @Override
            public void onCompleted() {
                responseObserver.onCompleted();
            }
        };
    }
    
    private User toProto(com.example.entity.User entity) {
        return User.newBuilder()
            .setId(entity.getId())
            .setName(entity.getName())
            .setEmail(entity.getEmail())
            .build();
    }
}
```

**3. Client:**
```java
@Service
public class UserGrpcClient {
    
    @GrpcClient("user-service")
    private UserServiceGrpc.UserServiceBlockingStub blockingStub;
    
    @GrpcClient("user-service")
    private UserServiceGrpc.UserServiceStub asyncStub;
    
    // Unary call
    public User getUser(long id) {
        GetUserRequest request = GetUserRequest.newBuilder()
            .setId(id)
            .build();
        
        return blockingStub.getUser(request);
    }
    
    // Server streaming
    public void listUsers(int page, int limit) {
        ListUsersRequest request = ListUsersRequest.newBuilder()
            .setPage(page)
            .setLimit(limit)
            .build();
        
        Iterator<User> users = blockingStub.listUsers(request);
        
        while (users.hasNext()) {
            User user = users.next();
            System.out.println("User: " + user.getName());
        }
    }
    
    // Async call
    public void getUserAsync(long id, StreamObserver<User> observer) {
        GetUserRequest request = GetUserRequest.newBuilder()
            .setId(id)
            .build();
        
        asyncStub.getUser(request, observer);
    }
}
```

**application.properties:**
```properties
# Server
grpc.server.port=9090

# Client
grpc.client.user-service.address=static://localhost:9090
grpc.client.user-service.negotiationType=PLAINTEXT
```

### Python

**Server:**
```python
import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

class UserServicer(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        # Database lookup
        user = get_user_from_db(request.id)
        
        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_pb2.User()
        
        return user_pb2.User(
            id=user['id'],
            name=user['name'],
            email=user['email']
        )
    
    def ListUsers(self, request, context):
        users = get_users_from_db(request.page, request.limit)
        
        for user in users:
            yield user_pb2.User(
                id=user['id'],
                name=user['name'],
                email=user['email']
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserServicer(), server
    )
    server.add_insecure_port('[::]:9090')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

**Client:**
```python
import grpc
import user_pb2
import user_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:9090') as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        
        # Unary call
        response = stub.GetUser(user_pb2.GetUserRequest(id=1))
        print(f"User: {response.name}")
        
        # Server streaming
        responses = stub.ListUsers(
            user_pb2.ListUsersRequest(page=1, limit=10)
        )
        
        for user in responses:
            print(f"User: {user.name}")

if __name__ == '__main__':
    run()
```

## 🔐 Security

### TLS/SSL
```java
// Server z TLS
@Bean
public GrpcServerFactoryConfigurer serverConfigurer() {
    return serverFactory -> {
        File certChain = new File("cert.pem");
        File privateKey = new File("key.pem");
        
        serverFactory.setSecurity(
            GrpcSslContexts.forServer(certChain, privateKey)
                .build()
        );
    };
}

// Client z TLS
grpc.client.user-service.negotiationType=TLS
grpc.client.user-service.security.trustCertCollection=classpath:ca.pem
```

### Authentication (Metadata)
```java
// Client - dodanie token
Metadata metadata = new Metadata();
metadata.put(
    Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER),
    "Bearer " + token
);

UserServiceGrpc.UserServiceBlockingStub stub = 
    blockingStub.withInterceptors(
        MetadataUtils.newAttachHeadersInterceptor(metadata)
    );

// Server - walidacja token
@Component
public class AuthInterceptor implements ServerInterceptor {
    @Override
    public <ReqT, RespT> ServerCall.Listener<ReqT> interceptCall(
            ServerCall<ReqT, RespT> call,
            Metadata headers,
            ServerCallHandler<ReqT, RespT> next) {
        
        String token = headers.get(
            Metadata.Key.of("authorization", Metadata.ASCII_STRING_MARSHALLER)
        );
        
        if (!validateToken(token)) {
            call.close(Status.UNAUTHENTICATED, new Metadata());
            return new ServerCall.Listener<>() {};
        }
        
        return next.startCall(call, headers);
    }
}
```

## ⚡ Zalety i Wady

### Zalety
```
✅ Bardzo wydajny (binary protocol)
✅ Automatyczne generowanie kodu
✅ Silna typizacja
✅ Streaming built-in
✅ HTTP/2 multiplexing
✅ Language-agnostic
✅ Load balancing
✅ Deadlines/timeouts
```

### Wady
```
❌ Limited browser support
❌ Not human-readable (binary)
❌ Steeper learning curve
❌ Less tooling niż REST
❌ Debugging trudniejszy
❌ Not cache-friendly
```

## 🎯 Use Cases

```
✅ Microservices communication
✅ Mobile apps (bandwidth efficient)
✅ IoT devices
✅ Real-time applications
✅ High-performance systems
✅ Polyglot systems
❌ Public APIs (używaj REST)
❌ Browser-only apps
```

## 🔗 Powiązane Tematy

- [[REST vs SOAP vs GraphQL|⚖️ Protokoły]]
- [[WebSockets|🔌 WebSockets]]
- [[Microservices i API|🔷 Microservices]]
- [[API Gateway Pattern|🚪 API Gateway]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~12 minut*

#grpc #protobuf #rpc #microservices #http2
