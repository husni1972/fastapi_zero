from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastapi_zero.classes.ip import IP
from fastapi_zero.schemas import Message

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/aula02', response_class=HTMLResponse)
def read_aula02():
    text_html = f"""
    <html>
      <head>
        <title>Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo! </h1>
        <h2> O IP do servidor é {IP.get_ip()} </h2>
      </body>
    </html>"""
    return text_html


#    return {'message': f'Olá Mundo! O IP do servidor é {IP.get_ip()}'}
