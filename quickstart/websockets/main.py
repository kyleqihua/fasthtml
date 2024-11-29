# type: ignore
from fasthtml.common import *
from asyncio import sleep

# 与传统的 HTTP 请求-响应模型不同，WebSocket 允许服务器和客户端之间进行实时、双向的数据交换
# 这使得 WebSocket 特别适合需要低延迟和高频率数据更新的应用程序，例如在线游戏、实时聊天应用程序和股票行情推送等
# 双向通信：服务器可以主动推送数据到客户端，而不仅仅是客户端发起请求
app, rt = fast_app(exts='ws')

def mk_inp(): return Input(id='msg', autofocus=True)

@rt('/')
async def get(request):
    cts = Div(
        Div(id='notifications'),
        Form(mk_inp(), id='form', ws_send=True),
        hx_ext='ws', ws_connect='/ws')
    return Titled('Websocket Test', cts)

async def on_connect(send):
    print('Connected!')
    await send(Div('Hello, you have connected', id="notifications"))

async def on_disconnect(ws):
    print('Disconnected!')

@app.ws('/ws', conn=on_connect, disconn=on_disconnect)
async def ws(msg:str, send):
    await send(Div('Hello ' + msg, id="notifications"))
    await sleep(2)
    return Div('Goodbye ' + msg, id="notifications"), mk_inp() # 只是向客户端发送了一个新的消息, 并没有关闭连接

serve()