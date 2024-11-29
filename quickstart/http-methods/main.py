from fasthtml.common import * 

app, rt = fast_app()

@rt("/")  
def get():
  return Titled("HTTP GET", P("Handle GET"))

@rt("/")  
def post():
  return Titled("HTTP POST", P("Handle POST"))

serve()