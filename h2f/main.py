# type: ignore
from fasthtml.common import *

app,rt = fast_app(hdrs=[HighlightJS()])

@rt("/convert")
def post(html:str, attr1st:bool): return Pre(Code(html2ft(html, attr1st=str2bool(attr1st)))) if html else ''

@rt("/")
def get():
    return Titled(
        "Convert HTML to FT",
        Form(hx_post='/convert', target_id="ft", hx_trigger="change from:#attr1st, keyup delay:500ms from:#html")(
            Select(style="width: auto", id="attr1st")(
                Option("Children 1st", value="0", selected=True), Option("Attrs 1st", value="1")),
            Textarea(placeholder='Paste HTML here', id="html", rows=10)),
        Div(id="ft"))

serve()

# P("HTML isn't computer code, but is a language that uses US English to enable texts (words, images, sounds) to be inserted and formatting such as colo(u)r and centre/ering to be written in. The process is fairly simple; the main difficulties often lie in small mistakes - if you slip up while word processing your reader may pick up your typos, but the page will still be legible. However, if your HTML is inaccurate the page may not appear - writing web pages is, at the least, very good practice for proof reading!")