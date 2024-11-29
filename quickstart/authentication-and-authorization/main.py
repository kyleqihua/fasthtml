# type: ignore
from fasthtml.common import *

# 定义登录重定向响应
# 303 主要用于 POST、PUT 或 DELETE 请求之后的重定向
# 它强制客户端使用 GET 方法访问新的 URL，而不管原始请求是什么方法
login_redir = RedirectResponse('/login', status_code=303)

# 定义身份验证中间件函数
def user_auth_before(req, sess):
    # 从会话中获取认证信息
    # The `auth` key in the request scope is automatically provided
    # to any handler which requests it, and can not be injected
    # by the user using query params, cookies, etc, so it should
    # be secure to use.   
    auth = req.scope['auth'] = sess.get('auth', None)
    # 如果未认证则重定向到登录页
    if not auth: 
        return login_redir 

# 创建 Beforeware 实例
beforeware = Beforeware(
    user_auth_before,
    skip=[
        r'/favicon\.ico',  # 跳过图标请求
        r'/static/.*',     # 跳过静态文件
        r'.*\.css',        # 跳过 CSS 文件
        r'.*\.js',         # 跳过 JS 文件
        '/login',          # 跳过登录页面
        '/'               # 跳过首页
    ]
)

app, rt = fast_app(live=True, before=beforeware)

# 登录页面路由
@rt("/login")
def get():
    frm = Form(
        Input(id='name', placeholder='用户名'),
        Input(id='pwd', type='password', placeholder='密码'), 
        Button('登录'),
        action='/login',
        method='post'
    )
    return Titled("登录", frm)

# 处理登录请求
@rt("/login") 
def post(name:str, pwd:str, sess):
    # 这里应该添加真实的用户验证逻辑
    if name and pwd:
        sess['auth'] = name
        return RedirectResponse('/', status_code=303)
    return login_redir

# 登出路由
@rt("/logout")
def get(sess):
    del sess['auth']
    return login_redir

@rt("/")
def get():
    return P("Hello, World!")

@rt("/private")
def get():
    return P("a private page")

@rt("/private2")
def get(sess):
    auth_user = sess.get('auth')
    return P(f"这是私有页面。当前登录用户: {auth_user}")

serve()