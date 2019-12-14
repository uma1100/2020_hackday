import asyncio
import websockets
from PIL import Image, ImageDraw, ImageFont
import numpy
import io

class WebSockets_Server:

    def __init__(self, loop, address , port):
        self.loop = loop
        self.address = address
        self.port = port
        # self.mode_pixcel = mode_pixcel  # True:ピクセルデータ形式,False=ファイル形式

        # self.font_path = "(font path)" # フォントのパスを指定
        # self.font = ImageFont.truetype(font=self.font_path, size=80)

    async def _handler(self, websocket, path):
        while True:
            recv_data = await websocket.recv()
            print(recv_data);

            # image = Image.new("RGBA", (300, 150))
            # draw = ImageDraw.Draw(image)
            # draw.text((0, 0), recv_data, (0, 0, 255), font=self.font)

            # if self.mode_pixcel:
            #     # ピクセルデータを送信する場合
            #     image_np = numpy.array(image)
            #     await websocket.send(image_np.tobytes())
            # else:
            #     # ファイル形式のデータを送信する場合
            #     with io.BytesIO() as image_temp:
            #         image.save(image_temp, format="png")
            #         await websocket.send(image_temp.getvalue())

    def run(self):
        self._server = websockets.serve(self._handler, self.address, self.port)
        self.loop.run_until_complete(self._server)
        self.loop.run_forever()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    wss = WebSockets_Server(loop, '0.0.0.0', 60000)
    wss.run()
