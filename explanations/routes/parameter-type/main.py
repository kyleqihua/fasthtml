from fasthtml.common import *

app, rt = fast_app(live=True)

@rt("/user/{nm}")
def get(nm: str):
    return P(f"Hello, {nm}!")

serve()