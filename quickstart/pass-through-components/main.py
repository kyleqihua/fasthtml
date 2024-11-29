from fasthtml.common import *

app, rt = fast_app()

def layout(*args, **kwargs):
    return Main(H1("dashboard"), Div(*args, **kwargs), cls="dashboard")


@rt("/")
def get():
    return layout(Ul(*[Li(o) for o in range(3)]), P("some content", cls="description"))

serve()