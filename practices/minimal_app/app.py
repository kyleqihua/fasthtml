# type: ignore
from fasthtml.common import *

app, rt = fast_app(live=True)

@rt("/")
def get():
    return P("Hello, World!")

serve()