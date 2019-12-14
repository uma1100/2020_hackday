var web_socket = null;

function on_load() {
  web_socket = new WebSocket("ws://localhost:60000"); // サーバーのアドレスを指定
  web_socket.binaryType = "arraybuffer";
  web_socket.onmessage = on_message;
  console.log("接続ok");
}

function on_button_send() {
  var text_input = document.getElementById("text_input");
  web_socket.send(text_input.value);
}
