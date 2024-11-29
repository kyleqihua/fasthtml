# type: ignore
import random
from asyncio import sleep
from fasthtml.common import *

hdrs=(Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),)
app,rt = fast_app(hdrs=hdrs, live=True)

@rt
def index():
    return Titled("SSE Random Number Generator",
        P("Generate pairs of random numbers, as the list grows scroll downwards."),
        Div(hx_ext="sse", # Tell HTMX to load the SSE extension
            sse_connect="/number-stream", # look at the /number-stream endpoint for SSE content
            hx_swap="beforeend show:bottom",
            sse_swap="message")) # 指定如何处理从服务器接收到的 SSE 事件数据。在这个例子中,它告诉 HTMX 监听名为 "message" 的事件。当服务器发送一个 "message" 事件时,HTMX 会使用事件数据来更新 DOM。如果您需要在同一个页面上处理多个不同类型的 SSE 事件,可以通过指定不同的事件名称来区分它们。"message" 是 FastHTML 的默认事件名称

shutdown_event = signal_shutdown()

async def number_generator():
    while not shutdown_event.is_set():
        data = Article(random.randint(1, 100))
        yield sse_message(data) # sse_wrap="message"与服务器端的sse_message() 函数相对应
        await sleep(1)

@rt("/number-stream")
async def get(): return EventStream(number_generator())

serve() 