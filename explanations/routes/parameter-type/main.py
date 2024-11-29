from fasthtml.common import *
from starlette.testclient import TestClient

app, rt = fast_app(live=True)

@rt("/user/{nm}")
def get(nm: str):
    return P(f"Hello, {nm}!")

client = TestClient(app)
r = client.get('/user/Jeremy')

# serve()