from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get(): return Div(P('hello world!'), hx_get="/change")

@rt("/change")
def get(): return P("nice to be here")

serve()


# # 从fasthtml.common导入所有必需的组件和工具
# from fasthtml.common import *

# # 创建一个FastHTML应用实例和路由装饰器
# app,rt = fast_app()

# # 定义根路由('/')的处理函数
# @rt('/')
# def get():
#     # 返回一个Div元素,包含:
#     # 1. 一个P元素,内容为'hello world!'
#     # 2. hx_get属性设置为"/change",这是HTMX的属性,
#     #    意味着这个Div会通过HTMX自动向/change发送GET请求
#     return Div(P('hello world!'), hx_get="/change")

# # 定义/change路由的处理函数
# @rt("/change")
# def get():
#     # 当/change被请求时,返回一个新的P元素
#     # 内容为"nice to be here"
#     # 这个内容会通过HTMX替换掉原来的Div内容
#     return P("nice to be here")

# # 启动服务器
# serve()