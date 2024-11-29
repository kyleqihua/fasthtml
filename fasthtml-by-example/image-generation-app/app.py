# type: ignore
from fastcore.parallel import threaded
from fasthtml.common import *
import uuid, os, uvicorn, requests, replicate
from PIL import Image
# from dotenv import load_dotenv
# load_dotenv()

# gens database for storing generated image details
tables = database('data/gens.db').t
gens = tables.gens
if not gens in tables:
    gens.create(id=int, prompt=str, folder=str, pk='id')
Generation = gens.dataclass()

# Flexbox CSS (http://flexboxgrid.com/)
gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")

# Our FastHTML app
app = FastHTML(hdrs=(picolink, gridlink))

# Main page
@app.get("/")
def home():
    inp = Input(id="new-prompt", name="prompt", placeholder="Enter a prompt")
    add = Form(Group(inp, Button("Generate")), hx_post="/", target_id='gen-list', hx_swap="afterbegin")
    gen_containers = [generation_preview(g) for g in gens(limit=10)] # Start with last 10
    gen_list = Div(*reversed(gen_containers), id='gen-list', cls="row") # flexbox container: class = row
    return Title('Image Generation Demo'), Main(H1('Magic Image Generation'), add, gen_list, cls='container')

# Show the image (if available) and prompt for a generation
def generation_preview(g):
    if not g:  # 如果记录不存在
        return Div("记录不存在", cls="box col-xs-12 col-sm-6 col-md-4 col-lg-3")
    
    grid_cls = "box col-xs-12 col-sm-6 col-md-4 col-lg-3"
    image_path = f"{g.folder}/{g.id}.png"
    
    if os.path.exists(image_path):
        return Div(Card(
                       Img(src=image_path, alt="Card image", cls="card-img-top"),
                       Div(P(B("提示语: "), g.prompt, cls="card-text"), cls="card-body"),
                   ), id=f'gen-{g.id}', cls=grid_cls)
    
    return Div(f"正在生成图片 {g.id}，提示语: {g.prompt}", 
              id=f'gen-{g.id}', 
              hx_get=f"/gens/{g.id}", 
              hx_trigger="every 2s", 
              hx_swap="outerHTML", 
              cls=grid_cls)

# A pending preview keeps polling this route until we return the image preview
@app.get("/gens/{id}")
def preview(id:int):
    try:
        gen = gens.get(id)
        return generation_preview(gen)
    except Exception as e:
        print(f"获取生成记录时出错: {str(e)}")
        return Div(f"找不到 ID 为 {id} 的生成记录", 
                  cls="box col-xs-12 col-sm-6 col-md-4 col-lg-3")

# For images, CSS, etc.
@app.get("/{fname:path}.{ext:static}")
def static(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# Generation route
@app.post("/")
def post(prompt:str):
    folder = f"data/gens/{str(uuid.uuid4())}"
    os.makedirs(folder, exist_ok=True)
    # 生成新的 ID
    new_id = len(list(gens())) + 1
    g = gens.insert(Generation(id=new_id, prompt=prompt, folder=folder))
    generate_and_save(g.prompt, g.id, g.folder)
    clear_input =  Input(id="new-prompt", name="prompt", placeholder="Enter a prompt", hx_swap_oob='true')
    return generation_preview(g), clear_input

# 添加 URL 生成函数
def get_url(prompt): 
    return f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?model=flux&width=1024&height=1024&seed=42&nologo=true&enhance=true"

# 简化后的图片生成函数
@threaded
def generate_and_save(prompt, id, folder):
    try:
        full_url = get_url(prompt)
        Image.open(requests.get(full_url, stream=True).raw).save(f"{folder}/{id}.png")
        return True
    except Exception as e:
        print(f"生成图片时出错: {str(e)}")
        return False
    

if __name__ == '__main__': uvicorn.run("app:app", host='0.0.0.0', port=int(os.getenv("PORT", default=8000)))