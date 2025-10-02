# 🔌 WebSockets

## 📖 Definicja

**WebSocket** to protokół komunikacji dwukierunkowej (full-duplex) przez pojedyncze połączenie TCP. Umożliwia real-time komunikację między klientem a serwerem.

## 🔄 HTTP vs WebSocket

### HTTP (Request-Response)
```
Client → Request  → Server
Client ← Response ← Server

Każde połączenie:
1. TCP handshake
2. HTTP request
3. HTTP response
4. Zamknięcie połączenia
```

### WebSocket (Persistent Connection)
```
Client → Handshake → Server
       ← Upgrade   ←
       ↕ Messages  ↕  (Dwukierunkowo)
       ↕           ↕
       ← Close     ←
```

## 🚀 WebSocket Handshake

### 1. Client wysyła Upgrade Request
```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
Origin: http://example.com
```

### 2. Server odpowiada
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### 3. Połączenie WebSocket Active
```
Teraz obydwie strony mogą wysyłać wiadomości
```

## 💻 Implementacja Client (JavaScript)

### Podstawowe Użycie
```javascript
// Utworzenie połączenia
const ws = new WebSocket('ws://localhost:8080/chat');

// Event: połączenie otwarte
ws.onopen = (event) => {
  console.log('Connected to WebSocket');
  ws.send('Hello Server!');
};

// Event: otrzymano wiadomość
ws.onmessage = (event) => {
  console.log('Message from server:', event.data);
  
  // Jeśli JSON
  const data = JSON.parse(event.data);
  console.log('Parsed:', data);
};

// Event: błąd
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Event: zamknięcie połączenia
ws.onclose = (event) => {
  console.log('Disconnected:', event.code, event.reason);
  
  if (event.wasClean) {
    console.log('Connection closed cleanly');
  } else {
    console.log('Connection died');
  }
};

// Wysyłanie wiadomości
ws.send('Text message');
ws.send(JSON.stringify({ type: 'chat', message: 'Hello!' }));

// Zamykanie połączenia
ws.close(1000, 'Normal closure');

// Sprawdzenie stanu
console.log(ws.readyState);
// 0 = CONNECTING, 1 = OPEN, 2 = CLOSING, 3 = CLOSED
```

### Klasa WebSocket Manager
```javascript
class WebSocketManager {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.messageQueue = [];
  }
  
  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('Connected');
      this.reconnectAttempts = 0;
      this.flushMessageQueue();
    };
    
    this.ws.onmessage = (event) => {
      this.handleMessage(JSON.parse(event.data));
    };
    
    this.ws.onerror = (error) => {
      console.error('Error:', error);
    };
    
    this.ws.onclose = () => {
      console.log('Disconnected');
      this.reconnect();
    };
  }
  
  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = this.reconnectDelay * this.reconnectAttempts;
      
      console.log(`Reconnecting in ${delay}ms...`);
      setTimeout(() => this.connect(), delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }
  
  send(data) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      this.messageQueue.push(data);
    }
  }
  
  flushMessageQueue() {
    while (this.messageQueue.length > 0) {
      const data = this.messageQueue.shift();
      this.send(data);
    }
  }
  
  handleMessage(data) {
    // Override w subklasie
    console.log('Message:', data);
  }
  
  disconnect() {
    this.ws.close(1000, 'Normal closure');
  }
}

// Użycie
const wsManager = new WebSocketManager('ws://localhost:8080/chat');
wsManager.connect();
wsManager.send({ type: 'chat', message: 'Hello!' });
```

## 🔧 Implementacja Server

### Spring Boot (Java)
```java
// 1. Konfiguracja
@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {
    
    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(chatHandler(), "/chat")
                .setAllowedOrigins("*");
    }
    
    @Bean
    public WebSocketHandler chatHandler() {
        return new ChatWebSocketHandler();
    }
}

// 2. Handler
@Component
public class ChatWebSocketHandler extends TextWebSocketHandler {
    
    private final Set<WebSocketSession> sessions = 
        Collections.synchronizedSet(new HashSet<>());
    
    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        sessions.add(session);
        System.out.println("New connection: " + session.getId());
    }
    
    @Override
    protected void handleTextMessage(WebSocketSession session, 
                                     TextMessage message) throws IOException {
        String payload = message.getPayload();
        System.out.println("Received: " + payload);
        
        // Broadcast do wszystkich
        for (WebSocketSession s : sessions) {
            if (s.isOpen()) {
                s.sendMessage(new TextMessage("Echo: " + payload));
            }
        }
    }
    
    @Override
    public void afterConnectionClosed(WebSocketSession session, 
                                     CloseStatus status) {
        sessions.remove(session);
        System.out.println("Connection closed: " + session.getId());
    }
    
    @Override
    public void handleTransportError(WebSocketSession session, 
                                    Throwable exception) {
        System.err.println("Error: " + exception.getMessage());
    }
}
```

### Node.js (Express + ws)
```javascript
const express = require('express');
const { WebSocketServer } = require('ws');
const http = require('http');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

// WebSocket connection
wss.on('connection', (ws) => {
  console.log('New client connected');
  
  // Wysłanie powitania
  ws.send(JSON.stringify({ type: 'welcome', message: 'Hello!' }));
  
  // Otrzymanie wiadomości
  ws.on('message', (data) => {
    console.log('Received:', data.toString());
    
    const message = JSON.parse(data);
    
    // Broadcast do wszystkich klientów
    wss.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'broadcast',
          message: message.message,
          sender: message.sender
        }));
      }
    });
  });
  
  // Zamknięcie połączenia
  ws.on('close', () => {
    console.log('Client disconnected');
  });
  
  // Błąd
  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });
});

server.listen(8080, () => {
  console.log('Server running on port 8080');
});
```

## 📱 Praktyczne Zastosowania

### 1. Chat Application
```javascript
// Client
const chat = {
  ws: null,
  
  connect() {
    this.ws = new WebSocket('ws://localhost:8080/chat');
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.displayMessage(message);
    };
  },
  
  sendMessage(text) {
    this.ws.send(JSON.stringify({
      type: 'message',
      text: text,
      sender: this.username,
      timestamp: Date.now()
    }));
  },
  
  displayMessage(message) {
    const div = document.createElement('div');
    div.textContent = `${message.sender}: ${message.text}`;
    document.getElementById('messages').appendChild(div);
  }
};
```

### 2. Real-time Notifications
```javascript
const notifications = new WebSocket('ws://api.example.com/notifications');

notifications.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  
  // Wyświetl toast notification
  showToast(notification.title, notification.message);
  
  // Odtwórz dźwięk
  new Audio('/notification.mp3').play();
  
  // Update badge
  updateNotificationBadge();
};
```

### 3. Live Data Feed
```javascript
const dataFeed = new WebSocket('ws://api.example.com/stock-prices');

dataFeed.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  // Update chart
  chart.addDataPoint(data.price, data.timestamp);
  
  // Update table
  updateStockTable(data);
};
```

### 4. Collaborative Editing
```javascript
const editor = new WebSocket('ws://docs.example.com/document/123');

// Wysyłanie zmian
document.addEventListener('input', (e) => {
  editor.send(JSON.stringify({
    type: 'edit',
    position: e.target.selectionStart,
    text: e.target.value,
    userId: currentUser.id
  }));
});

// Otrzymywanie zmian
editor.onmessage = (event) => {
  const edit = JSON.parse(event.data);
  if (edit.userId !== currentUser.id) {
    applyRemoteEdit(edit);
  }
};
```

## 🔐 Bezpieczeństwo

### Authentication
```javascript
// Token w URL (nie zalecane dla production)
const ws = new WebSocket('ws://localhost:8080/chat?token=abc123');

// Token w pierwszej wiadomości
const ws = new WebSocket('ws://localhost:8080/chat');
ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'auth',
    token: localStorage.getItem('token')
  }));
};
```

```java
// Server - Spring Boot
@Override
public void afterConnectionEstablished(WebSocketSession session) {
    String token = getTokenFromSession(session);
    
    if (!jwtService.validateToken(token)) {
        session.close(CloseStatus.NOT_ACCEPTABLE);
        return;
    }
    
    sessions.add(session);
}
```

### WSS (WebSocket Secure)
```javascript
// Używaj wss:// zamiast ws:// w produkcji
const ws = new WebSocket('wss://api.example.com/chat');
```

### Rate Limiting
```java
@Component
public class RateLimitingWebSocketHandler extends TextWebSocketHandler {
    
    private final Map<String, RateLimiter> limiters = new ConcurrentHashMap<>();
    
    @Override
    protected void handleTextMessage(WebSocketSession session, 
                                     TextMessage message) {
        String sessionId = session.getId();
        RateLimiter limiter = limiters.computeIfAbsent(
            sessionId, 
            k -> RateLimiter.create(10.0) // 10 msg/s
        );
        
        if (!limiter.tryAcquire()) {
            session.sendMessage(new TextMessage(
                "{\"error\": \"Rate limit exceeded\"}"
            ));
            return;
        }
        
        // Process message
    }
}
```

## ⚡ Zalety i Wady

### Zalety
```
✅ Real-time communication
✅ Dwukierunkowa komunikacja
✅ Niski latency
✅ Mniej overhead niż HTTP polling
✅ Efektywne dla częstych updates
✅ Wsparcie przeglądarek (95%+)
```

### Wady
```
❌ Trudniejsze skalowanie
❌ Stateful (wymaga sticky sessions)
❌ Load balancing challenges
❌ Brak automatycznego reconnect
❌ Proxy/firewall issues
❌ Trudniejsze caching
```

## 🔄 Alternatywy

### Server-Sent Events (SSE)
```
✓ Prostsze niż WebSocket
✓ Jednostronna komunikacja (server → client)
✓ Auto-reconnect
✓ HTTP/2 multiplexing
✗ Brak komunikacji client → server
```

### Long Polling
```
✓ Kompatybilność ze starymi przeglądarkami
✗ Więcej overhead
✗ Wyższe latency
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[gRPC Protocol|⚡ gRPC]]
- [[REST vs SOAP vs GraphQL|⚖️ Protokoły]]
- [[API Gateway Pattern|🚪 API Gateway]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~10 minut*

#websocket #real-time #communication #full-duplex
