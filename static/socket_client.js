var web_socket = null;

function on_load() {
  web_socket = new WebSocket("ws://192.168.43.195:8080"); // サーバーのアドレスを指定
  web_socket.binaryType = "arraybuffer";
  console.log("接続ok");
}

function finish_notice(flag) {
  // flag = document.getElementById("text_inp);
  web_socket.send(flag);
}

on_load();