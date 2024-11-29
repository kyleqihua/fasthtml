
from fasthtml.common import *
from pathlib import Path

app, rt = fast_app()

upload_dir = Path("filez")
upload_dir.mkdir(exist_ok=True)

@rt('/')
def get():
    return Titled("Multiple File Upload Demo",
        Article(
            Form(hx_post=upload_many, hx_target="#result-many")(
                Input(type="file", name="files", multiple=True),
                Button("Upload", type="submit", cls='secondary'),
            ),
            Div(id="result-many")
        )
    )

def FileMetaDataCard(file):
    return Article(
        Header(H3(file.filename)),
        Ul(
            Li('Size: ', file.size),            
            Li('Content Type: ', file.content_type),
            Li('Headers: ', file.headers),
        )
    )    

@rt
async def upload_many(files: list[UploadFile]):
    cards = []
    for file in files:
        cards.append(FileMetaDataCard(file))
        filebuffer = await file.read()
        (upload_dir / file.filename).write_bytes(filebuffer)
    return cards

serve()