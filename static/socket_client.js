var web_socket = null;

function on_load() {
  web_socket = new WebSocket("ws://192.168.43.195:8080"); // サーバーのアドレスを指定
  web_socket.binaryType = "arraybuffer";
  // web_socket.onmessage = on_message;
  console.log("接続ok");
}

function finish_notice(flag) {
  web_socket.send(flag);
}
