import asyncio
import websockets
import io
import servo
class WebSockets_Server:

    def __init__(self, loop, address , port):
        self.loop = loop
        self.address = address
        self.port = port

    async def _handler(self, websocket, path):
        while True:
            recv_data = await websocket.recv()
            print(recv_data)
            print(type(recv_data))
            if recv_data == "0":
                # Lock
                servo.setFinishServo(0)
                #servo.setTempServo(0)
            elif recv_data == "1":
                # UnLock
                servo.setFinishServo(1)
                #servo.setTempServo(1)
            #elif recv_data == "2":
             #   servo.setFinishServo(0)
            #elif recv_data == "3":
             #   servo.setFinishServo(1)

    def run(self):
        self._server = websockets.serve(self._handler, self.address, self.port)
        self.loop.run_until_complete(self._server)
        self.loop.run_forever()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    wss = WebSockets_Server(loop, '0.0.0.0', 8080)
    wss.run()
