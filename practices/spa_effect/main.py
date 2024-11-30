from fasthtml.common import *

app, rt = fast_app(live=True)

@rt("/")
def get():
    return Div(
        Nav(
            A("Home Page", href="/"),
            A("Book Page", hx_get="/book", hx_target="#content"),
            A("Music Page", hx_get="/music")            
        ),
        Main(id="content")
        )

@rt("/book")
def get():
    return P("您可以在这里浏览图书列表")

@rt("/music")
def get():
    return P("music page returned")

serve()