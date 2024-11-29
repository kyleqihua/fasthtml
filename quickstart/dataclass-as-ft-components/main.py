from dataclasses import dataclass
from fasthtml.common import *

@dataclass
class Hero:
    title: str
    statement: str

    def __ft__(self):
        return Div(H1(self.title), P(self.statement), cls="hero")

app, rt = fast_app()

@rt("/")
def get():
    return Main(Hero("just a title", "this is a hero statement"))

serve()