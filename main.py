from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = ['http://localhost:5500', 'http://127.0.0.1:5500']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])


class Tarefa(BaseModel):
    id: int | None
    descricao: str
    responsavel: str | None
    nivel: int
    situacao: str | None = 'Novo'
    prioridade: int

# a) Adicionar listar, remover, detalhes


tarefas: list[Tarefa] = []

# Criar uma tarefa


@app.post('/tarefas', status_code=status.HTTP_201_CREATED)
def adicionar_tarefa(tarefa: Tarefa):
    tarefa.id = len(tarefas) + 0
    tarefas.append(tarefa)
    return tarefa

# Listar todas as tarefas


@app.get('/tarefas')
def listar_tarefas():
    return tarefas

# Deletar tarefa através do ID


@app.delete('/tarefas/{tarefa_id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_tarefa(tarefa_id: int):
    for tarefa_marcada in tarefas:
        if tarefa_marcada.id == tarefa_id:
            tarefas.remove(tarefa_marcada)
            return {"Tarefa excluída"}

    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa de ID {tarefa_id} não encontrada')

# Obter tarefa através do ID


@app.get('/tarefas/{tarefa_id}')
def obter_tarefa(tarefa_id: int):
    for tarefa_selecionada in tarefas:
        if tarefa_selecionada.id == tarefa_id:
            return tarefas[tarefa_id]

    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa de ID {tarefa_id} não encontrada')


# B,C,D = implementar um modelo de update - PUT para atualizar a situação da tarefa;

'''Diagrama de Estados:
1) NOVA --> Ao criar Tarefa
2) EM ANDAMENTO vem de NOVA ou de PENDENTE
3) PENDENTE vem de NOVA ou de EM ANDAMENTO
4) CANCELADA por vir de qualquer Situação
5) RESOLVIDA vem de EM ANDAMENTO'''

# Atualizar a tarefa - estado = Em andamento


@app.put('/tarefas/atualizar/situacao/andamento/{tarefa_id}')
def atualizar_tarefa(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            tarefa_id = tarefa_atual.id
            if tarefa_atual.situacao == 'Nova' or 'Pendente':
                tarefa_atual.situacao = 'Em andamento'
            if tarefa_atual.situacao == 'Em andamento':
                tarefa_atual.prioridade = 3
                tarefas[index] = tarefa_atual
                return tarefa_atual
            else:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                                    detail=f"Para atualizarmos a situação da tarefa {tarefa_id} sua situação deve ser 'Nova' ou 'Pendente' ")

    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa de ID {tarefa_id} não encontrada')


# Atualizar a tarefa - estado = Pendente
@app.put('/tarefas/atualizar/situacao/pendente/{tarefa_id}')
def atualizar_tarefa(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            tarefa_id = tarefa_atual.id
            if tarefa_atual.situacao == 'Nova' or 'Em andamento':
                tarefa_atual.situacao = 'Pendente'
            if tarefa_atual.situacao == 'Pendente':
                tarefa_atual.prioridade = 2
                tarefas[index] = tarefa_atual
                return tarefa_atual
            else:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                                    detail=f"Para atualizarmos a situação da tarefa {tarefa_id} sua situação deve ser 'Nova' ou 'Em andamento' ")
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa de ID {tarefa_id} não encontrada')


# Atualizar a tarefa - estado = Resolvida
@app.put('/tarefas/atualizar/situacao/resolvida/{tarefa_id}')
def atualizar_tarefa(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            tarefa_id = tarefa_atual.id
            if tarefa_atual.situacao == 'Em andamento':
                tarefa_atual.situacao = 'Resolvida'
                tarefas[index] = tarefa_atual

                return tarefa_atual
            else:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                                    detail=f"Para atualizarmos a situação da tarefa {tarefa_id} sua situação deve ser 'Em andamento' ")

    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa de ID {tarefa_id} não encontrada')

# Cancelar tarefa


@app.put('/tarefas/cancelar/{tarefa_id}')
def atualizar_tarefa(tarefa_id: int):
    for index in range(len(tarefas)):
        tarefa_atual = tarefas[index]
        if tarefa_atual.id == tarefa_id:
            tarefa_id = tarefa_atual.id
            if tarefa_atual.situacao == 'Nova' or 'Pendente' or 'Em andamento':
                tarefa_atual.situacao = 'Cancelada'
                tarefas[index] = tarefa_atual
                return tarefa_atual
            else:
                return 'Não foi possível cancelar a sua tarefa'

    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa de ID {tarefa_id} não encontrada')


# Listar tarefas por situação
@app.get('/tarefas/situacao/{tarefa_situacao}')
def listar_situacao(tarefa_situacao: str):
    return [pesquisa for pesquisa in tarefas if pesquisa.situacao == tarefa_situacao]

# Listar tarefas por prioridade


@app.get('/tarefas/prioridade/{tarefa_prioridade}')
def listar_situacao(tarefa_prioridade: int):
    return [pesquisa for pesquisa in tarefas if pesquisa.prioridade == tarefa_prioridade]

# Listar tarefas por nível


@app.get('/tarefas/nivel/{tarefa_nivel}')
def listar_situacao(tarefa_nivel: int):
    return [pesquisa for pesquisa in tarefas if pesquisa.nivel == tarefa_nivel]
