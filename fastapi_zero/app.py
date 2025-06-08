# live 258 e 211 / 207 / 234
#
from asyncio import sleep
from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.routers import auth, users
from fastapi_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    await sleep(1)
    return {'message': 'Olá Mundo!'}


'''
# @app.post('/users/', status_code=HTTPStatus.CREATED,
#  response_model=UserPublic)
# def create_user(user: UserSchema):
#     user_with_id = UserDB(
#         **user.model_dump(),
#         id=len(database) + 1,
#     )

#     database.append(user_with_id)

#     return user_with_id


#        **user.model_dump(),
#         igual a
#         username=user.username,
#         email=user.email,
#         password=user.password,


# @app.get('/aula02', response_class=HTMLResponse)
# def read_aula02():
#     text_html = f"""
#     <html>
#       <head>
#         <title>Nosso olá mundo!</title>
#       </head>
#       <body>
#         <h1> Olá Mundo! </h1>
#         <h2> O Socket Name IP é {IP.get_ip()} </h2>
#       </body>
#     </html>"""
#     return text_html
#    return {'message': f'Olá Mundo! O IP do servidor é {IP.get_ip()}'}
'''
