# type: ignore
from fasthtml.common import *

app, rt = fast_app(live=True)

# 添加 toasts 支持
setup_toasts(app)

@rt("/")
def get(session):
    # 添加一些示例 toasts
    add_toast(session, "欢迎来到我的应用!", "success")
    add_toast(session, "这是一条信息提示", "info") 
    add_toast(session, "警告提示", "warning")
    add_toast(session, "错误提示", "error")
    return P("Hello, World!")

serve()

