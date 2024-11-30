from fasthtml.common import *
from functools import wraps

app, rt = fast_app(live=True)

def basic_auth(f):
    @wraps(f)
    async def wrapper(req, *args, **kwargs):
        token = req.headers.get("Authorization")
        if token == 'abc123':
            return await f(req, *args, **kwargs)
        return Response('Not Authorized', status_code=401)
    return wrapper

@rt("/protected")
@basic_auth
async def get(req):
    return "protected content that you can see if you know the token in the header authorization field"

serve()