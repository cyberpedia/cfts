import ReconnectingWebSocket from 'reconnecting-websocket';

const WS_URL = 'ws://127.0.0.1:8000/ws/activity';

class WebSocketService {
  constructor() {
    this.socket = new ReconnectingWebSocket(WS_URL);
    this.listeners = new Set();

    this.socket.onmessage = (event) => {
      this.listeners.forEach(listener => listener(event));
    };

    this.socket.onopen = () => {
      console.log('WebSocket connection established.');
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    this.socket.onclose = () => {
      console.log('WebSocket connection closed.');
    };
  }

  subscribe(callback) {
    this.listeners.add(callback);
  }

  unsubscribe(callback) {
    this.listeners.delete(callback);
  }
  
  close() {
      this.socket.close();
  }
}

// Export a singleton instance
const websocketService = new WebSocketService();
export default websocketService;
