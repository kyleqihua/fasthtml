# type: ignore
from fasthtml.common import *

app, rt = fast_app(live=True)

@rt("/")
def get(session):  # 添加 session 参数
    return P("Hello, World!")

@rt("/counter")
def get(session):
    # 初始化计数器
    session.setdefault('count', 0)
    # 增加计数
    session['count'] = session.get('count') + 1
    return P(f"您已访问此页面 {session['count']} 次")

@rt('/adder/{num}')
def get(session, num: int):
    session.setdefault('sum', 0)
    session['sum'] = session.get('sum') + num
    return Response(f'The sum is {session["sum"]}.')

serve()