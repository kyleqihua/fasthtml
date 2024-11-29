from fasthtml.common import * 

app, rt = fast_app()

@rt("/{name}/{age}")
def get(name: str, age: int):
  return Titled(f"Hello {name.title()}, age {age}")

serve()