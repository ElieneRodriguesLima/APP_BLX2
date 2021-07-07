from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from src.routers import rotas_produtos, rotas_auth, rotas_pedidos
from src.jobs.write_notification import write_notification

app = FastAPI()

#CORS
origins = ['http://localhost:3000',
           'http://myapp.vercel.com']
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)

#ROTAS PRODUTOS
app.include_router(rotas_produtos.router)

#ROTAS DE SEGURANÇA: AUTENTICAÇÃO E AUTORIZAÇÃO
app.include_router(rotas_auth.router, prefix="/auth")

#ROTAS PEDIDOS
app.include_router(rotas_pedidos.router)

#BACKGROUND TASK - TAREFAS EM SEGUNDO PLANO
@app.post('/send_email/{email}')
def send_email(email: str, background: BackgroundTasks):
    background.add_task(write_notification,
                        email, 'Olá tudo bem?!')
    return {'OK': 'Mensagem enviada'}



@app.middleware('http')
async def tempoMiddleware(request: Request, next):
    print('Interceptou Chegada...')

    response = await next(request)

    print('Interceptou Volta ...')

    return response