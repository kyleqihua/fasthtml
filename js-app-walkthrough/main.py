from fasthtml.common import *
from datetime import datetime

def render(room):
    return Li(A(room.name, href=f"/rooms/{room.id}"))

app,rt,rooms,Room = fast_app('data/drawapp.db', render=render, id=int, name=str, created_at=str, canvas_data=str, pk='id')

@rt("/")
def get():
    create_room = Form(Input(id="name", name="name", placeholder="New Room Name"),
                       Button("Create Room"),
                       hx_post="/rooms", hx_target="#rooms-list", hx_swap="afterbegin")
    rooms_list = Ul(*rooms(order_by='id DESC'), id='rooms-list')
    return Titled("QuickDraw", 
                  create_room, rooms_list)

@rt("/rooms")
async def post(room:Room):
    room.created_at = datetime.now().isoformat()
    return rooms.insert(room)

@rt("/rooms/{id}")
async def get(id:int):
    room = rooms[id]
    canvas = Canvas(id="canvas", width="800", height="600")
    color_picker = Input(type="color", id="color-picker", value="#000000")
    brush_size = Input(type="range", id="brush-size", min="1", max="50", value="10")
    save_button = Button("Save Canvas", id="save-canvas", hx_post=f"/rooms/{id}/save", hx_vals="js:{canvas_data: JSON.stringify(canvas.toJSON())}")

    js = f"""
    var canvas = new fabric.Canvas('canvas');
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.color = '#000000';
    canvas.freeDrawingBrush.width = 10;

    // Load existing canvas data
    fetch(`/rooms/{id}/load`)
    .then(response => response.json())
    .then(data => {{
        if (data && Object.keys(data).length > 0) {{
            canvas.loadFromJSON(data, canvas.renderAll.bind(canvas));
        }}
    }});
    
    document.getElementById('color-picker').onchange = function() {{
        canvas.freeDrawingBrush.color = this.value;
    }};
    
    document.getElementById('brush-size').oninput = function() {{
        canvas.freeDrawingBrush.width = parseInt(this.value, 10);
    }};
    """
    
    return Titled(f"Room: {room.name}",
                  A(Button("Leave Room"), href="/"),
                  canvas,
                  Div(color_picker, brush_size, save_button),
                  Script(src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"),
                  Script(js))

@rt("/rooms/{id}/save")
async def post(id:int, canvas_data:str):
    rooms.update({'canvas_data': canvas_data}, id)
    return "Canvas saved successfully"

@rt("/rooms/{id}/load")
async def get(id:int):
    room = rooms[id]
    return room.canvas_data if room.canvas_data else "{}"

serve()

# from fasthtml.common import *
# from datetime import datetime

# # # 创建数据库连接
# # db = database('data/drawapp.db') # 创建/连接到一个 SQLite 数据库文件

# # # db 是整个数据库的连接
# # # db.t 是所有表的容器
# # # 获取rooms表引用
# # rooms = db.t.rooms

# # # database (data/drawapp.db)
# # # │
# # # ├── db.t (表容器)
# # # │   ├── rooms    (单个表)
# # # │   ├── users    (单个表)
# # # │   └── messages (单个表)

# # # 如果表不存在,创建表结构
# # if rooms not in db.t:
# #     rooms.create(
# #         id=int,      # id字段为整型
# #         name=str,    # name字段为字符串
# #         created_at=str,  # created_at字段为字符串
# #         pk='id'      # 主键为id字段
# #     )

# # # 为每个表创建对应的数据类
# # Room = rooms.dataclass()

# # # 使用@patch装饰器为Room类添加__ft__方法
# # @patch 
# # def __ft__(self:Room):
# #     # 定义如何将Room对象渲染为FastHTML组件
# #     return Li(
# #         A(self.name, href=f"/rooms/{self.id}")
# #     )

# def render(room):
#     return Li(A(room.room_name, href=f"/rooms/{room.db_id}"))

# app,rt,rooms,Room = fast_app('data/drawapp.db', render=render, db_id=int, room_name=str, created_at=str, canvas_data=str, pk='db_id')

# @rt("/")
# def get():
#     create_room = Form(Input(id="room_name_input", name="room_name", placeholder="New Room Name"),
#                        Button("Create Room"),
#                        hx_post="/rooms", hx_target="#rooms-list", hx_swap="afterbegin")
#     rooms_list = Ul(*rooms(order_by='db_id DESC'), id='rooms-list')
#     return Titled("DrawCollab", create_room, rooms_list)

# @rt("/rooms")
# async def post(room:Room): # 关键点：参数类型标注为 Room
#     room.created_at = datetime.now().isoformat()
#     return rooms.insert(room)

# # 在 Python 代码中直接管理 JavaScript 代码
# @rt("/rooms/{db_id}")
# async def get(db_id: int):
#     room = rooms[db_id]
#     canvas = Canvas(id="drawing_canvas", width="800", height="600")
#     color_picker = Input(
#         type="color",
#         id="brush_color_picker",
#         value="#3CDD8C"
#     )
#     brush_size = Input(
#         type="range",
#         id="brush_size_slider",
#         min="1",
#         max="50",
#         value="10"
#     )
#     save_button = Button("Save Canvas", id="save-canvas", hx_post=f"/rooms/{db_id}/save", hx_vals="js:{canvas_data: JSON.stringify(canvas.toJSON())}")
    
#     js = """
#     document.addEventListener('DOMContentLoaded', function() {{
#     // 确保 fabric.js 已加载
#     if (typeof fabric === 'undefined') {{
#         console.error('Fabric.js 未加载');
#         return;
#     }}
        
#     # 1. 初始化 fabric.js Canvas
#     var canvas = new fabric.Canvas('drawing_canvas');
#     canvas.isDrawingMode = true;
#     canvas.freeDrawingBrush.color = '#3CDD8C'; # 设置默认画笔颜色
#     canvas.freeDrawingBrush.width = 10; # 设置默认画笔大小
#     fetch(`/rooms/${db_id}/load`).then(res => res.json()).then(data => {{
#         if (data && Object.keys(data).length > 0) {{
#             canvas.loadFromJSON(data, canvas.renderAll.bind(canvas));
#         }}
#     }})
    
#     # 2. 颜色选择器事件处理
#     document.getElementById('brush_color_picker').onchange = function() {
#         canvas.freeDrawingBrush.color = this.value;
#     };
    
#     # 3. 画笔大小滑块事件处理 
#     document.getElementById('brush_size_slider').oninput = function() {
#         canvas.freeDrawingBrush.width = parseInt(this.value, 10);
#     };
#     """
    
#     return Titled(
#         f"房间: {room.room_name}",
#         A(Button("离开房间"), href="/"),
#         canvas,
#         Div(color_picker, brush_size, save_button),
#         Script(src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"), # 如果没有这一行,我们的自定义代码中的 fabric 对象将是未定义的
#         Script(js) # 使用 fabric.js 提供的功能来实现具体的画布行为, 设置画笔颜色、大小等具体参数, 绑定颜色选择器和画笔大小滑块的事件处理
#     )

# @rt("/rooms/{db_id}/save")
# async def post(db_id: int, canvas_data: str):
#     rooms.update({"canvas_data": canvas_data}, db_id)
#     return "Canvas saved"

# @rt("/rooms/{db_id}/load")
# async def get(db_id: int):
#     room = rooms[db_id]
#     return room.canvas_data if room.canvas_data else "{}"

# serve()