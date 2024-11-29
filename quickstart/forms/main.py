# type: ignore

from fasthtml.common import *
from dataclasses import dataclass

app, rt = fast_app(live=True)

# define a dataclass to validate data from users 
@dataclass
class Profile:
    email: str;
    phone: str;
    age: int 

# profile_form = Form(method="post", action="/profile")(
#         Fieldset(
#             Label('Email', Input(name="email")),
#             Label("Phone", Input(name="phone")),
#             Label("Age", Input(name="age")),
#         ),
#         Button("Save", type="submit"),
#     )

# 可以改造为 HTMX 方式
profile_form = Form()(  # 移除 method 和 action
    Fieldset(
        Label('Email', Input(name="email")),
        Label("Phone", Input(name="phone")),
        Label("Age", Input(name="age")),
    ),
    Button("Save", 
           hx_post="/profile",        # 声明式提交
           hx_target="#result",       # 结果显示位置
           hx_indicator=".spinner")   # 加载动画
)

# 创建了一个 Profile 实例并预填了一些示例数据。在当前代码中,它主要用于演示目的
profile = Profile(email='john@example.com', phone='123456789', age=5)

fill_form(profile_form, profile)


@rt("/")
def get():
    return P("Hello, World!", A("个人信息表单", 
                                hx_get="/profile",  # 使用 AJAX 获取内容
                                hx_target="body",   # 将新内容替换到 body 
                                hx_push_url="true"  # 更新浏览器 URL,支持前进后退
                                )) 

@rt("/profile") 
def get():
    return Titled(
        "个人信息表单",
        profile_form,
        Div(id="result")  # 添加一个结果容器
    )

@rt("/profile") 
def post(profile: Profile):
    # 这里可以添加数据验证和保存逻辑
    return Titled(
        "提交成功",
        P(f"邮箱: {profile.email}"),
        P(f"电话: {profile.phone}"), 
        P(f"年龄: {profile.age}")
    )

serve()