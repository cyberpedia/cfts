import ReconnectingWebSocket from 'reconnecting-websocket';

// Construct WebSocket URL relative to the current host
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const host = window.location.host;
const WS_URL = `${protocol}//${host}/ws/activity`;


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

const websocketService = new WebSocketService();
export default websocketService;
