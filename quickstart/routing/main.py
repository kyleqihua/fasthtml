from fasthtml.common import * 

app, rt = fast_app()

@rt("/")
def get():
  return Titled("FastHTML", P("Let's do this!"))

@rt("/hello")
def get():
  return Titled("Hello, world!")

serve()