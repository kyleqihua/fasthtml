from fasthtml.common import *

app, rt = fast_app(debug=True)

@rt("/")
def get():
    1/0
    return Titled("FastHTML Error!", P("Let's error!"))

serve()