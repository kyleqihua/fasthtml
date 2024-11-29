# type: ignore 
# it takes a while to see the delete effect. why?
from fasthtml.common import *

app, rt = fast_app(live=True)

@rt("/")
def get():
    return Main(
        P("a sentence to be deleted", id="sentence"), 
        Button("Click me to delete the sentence!", 
            hx_delete="/delete", 
            hx_target="#sentence",
            hx_swap="outerHTML"
        )
    )

@rt("/delete")
def delete():
    return ""

serve()