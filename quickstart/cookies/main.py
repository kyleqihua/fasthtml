# type: ignore
from fasthtml.common import *
from datetime import datetime
# from IPython.display import HTML

app, rt = fast_app(live=True, debug=True)

@rt("/")
def get():
    return P("Hello, World!")

@rt("/settimestamp")
def get(req):
    now = datetime.now()
    return P(f"Cookie was set at time {now.time()}", cookie("now", str(now)))

serve()
