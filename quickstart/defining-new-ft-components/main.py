from fasthtml.common import *

app, rt = fast_app()

def hero(title, statement):
    return Div(H1(title), P(statement), cls="hero")

@rt("/")
def get():
    return Main("a simple webpage", hero("welcome", "this is a website built with fasthtml"))

serve()