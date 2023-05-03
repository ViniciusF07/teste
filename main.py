from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from bson import ObjectId


app = FastAPI()
# Configuração da conexão com o MongoDB
client = MongoClient("mongodb+srv://vreabin:ZNbqixYWpkcnMIvK@cluster0.ysransw.mongodb.net/?retryWrites=true&w=majority")
db = client["tarefasbd"]
collection = db["tarefas"]

origins = ["http://localhost:5500", "http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Classe modelo para a tarefa


class Tarefa(BaseModel):

    descricao: str
    responsavel: str | None
    nivel: int
    situacao: str | None = "Novo"
    prioridade: int

# Criar uma tarefa


@app.post("/criar", status_code=status.HTTP_201_CREATED)
def adicionar_tarefa(tarefa: Tarefa):
    tarefa_dict = tarefa.dict()
    inserted_tarefa = collection.insert_one(tarefa_dict)
    tarefa_dict["_id"] = str(inserted_tarefa.inserted_id)
    return tarefa_dict


# Listar todas as tarefas


@app.get("/tarefas")
def listar_tarefas():
    tarefas = []
    for tarefa in collection.find():
        tarefa["_id"] = str(tarefa["_id"])
        tarefas.append(tarefa)
    return tarefas

# Obter tarefa através do ID


@app.get("/tarefas/{tarefa_id}")
def obter_tarefa(tarefa_id: str):
    tarefa = collection.find_one({"_id": ObjectId(tarefa_id)})
    if tarefa:
        tarefa["_id"] = str(tarefa["_id"])
        return tarefa
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f"Tarefa de ID {tarefa_id} não encontrada")

# Deletar tarefa através do ID


@app.delete("/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_tarefa(tarefa_id: str):
    delete_result = collection.delete_one({"_id": ObjectId(tarefa_id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f"Tarefa de ID {tarefa_id} não encontrada")


# Atualizar a tarefa - estado = Em andamento


@app.put('/tarefas/atualizar/emandamento/{tarefa_id}')
def atualizar_tarefa(tarefa_id: str):
    tarefa_atual = collection.find_one({"_id": ObjectId(tarefa_id)})
    if tarefa_atual:
        if tarefa_atual["situacao"] == 'Nova' or tarefa_atual["situacao"] == 'Pendente':
            result = collection.update_one(
                {"_id": ObjectId(tarefa_id)},
                {"$set": {"situacao": "Em andamento",
                          "prioridade": 3}}
            )
            if result.modified_count == 1:
                # Convertendo o ObjectId para string antes de chamar o jsonable_encoder
                tarefa_atual["_id"] = str(tarefa_atual["_id"])
                tarefa_atual = jsonable_encoder(tarefa_atual)
                return tarefa_atual
            raise HTTPException(status.HTTP_200_OK,
                                detail=f"Tarefa {tarefa_id} atualizada com sucesso")
        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"Para atualizarmos a situação da tarefa {tarefa_id} sua situação deve ser 'Nova' ou 'Pendente' ")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Tarefa de ID {tarefa_id} não encontrada')


# Atualizar a tarefa - estado = Pendente
@app.put('/tarefas/atualizar/pendente/{tarefa_id}')
def atualizar_tarefa_pendente(tarefa_id: str):
    tarefa_atual = collection.find_one({"_id": ObjectId(tarefa_id)})
    if tarefa_atual:
        if tarefa_atual["situacao"] == 'Nova' or tarefa_atual["situacao"] == 'Em andamento':
            result = collection.update_one(
                {"_id": ObjectId(tarefa_id)},
                {"$set": {"situacao": "Pendente",
                          "prioridade": 2}}
            )
            if result.modified_count == 1:
                # Convertendo o ObjectId para string antes de chamar o jsonable_encoder
                tarefa_atual["_id"] = str(tarefa_atual["_id"])
                tarefa_atual = jsonable_encoder(tarefa_atual)
                return tarefa_atual
            raise HTTPException(status.HTTP_200_OK,
                                detail=f"Tarefa {tarefa_id} atualizada com sucesso")
        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"Para atualizarmos a situação da tarefa {tarefa_id} sua situação deve ser 'Nova' ou 'Em andamento' ")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Tarefa de ID {tarefa_id} não encontrada')


# Atualizar a tarefa - estado = Resolvida
@app.put('/tarefas/atualizar/resolvida/{tarefa_id}')
def atualizar_tarefa_resolvida(tarefa_id: str):
    tarefa_atual = collection.find_one({"_id": ObjectId(tarefa_id)})
    if tarefa_atual:
        if tarefa_atual["situacao"] == 'Em andamento':
            result = collection.update_one(
                {"_id": ObjectId(tarefa_id)},
                {"$set": {"situacao": "Resolvida",
                          "prioridade": 1}}
            )
            if result.modified_count == 1:
                # Convertendo o ObjectId para string antes de chamar o jsonable_encoder
                tarefa_atual["_id"] = str(tarefa_atual["_id"])
                tarefa_atual = jsonable_encoder(tarefa_atual)
                return tarefa_atual
            raise HTTPException(status.HTTP_200_OK,
                                detail=f"Tarefa {tarefa_id} atualizada com sucesso")
        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"Para atualizarmos a situação da tarefa {tarefa_id} sua situação deve ser 'Em andamento' ")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Tarefa de ID {tarefa_id} não encontrada')


@app.put('/tarefas/cancelar/{tarefa_id}')
def atualizar_tarefa_resolvida(tarefa_id: str):
    tarefa_atual = collection.find_one({"_id": ObjectId(tarefa_id)})
    if tarefa_atual:
        if tarefa_atual["situacao"] == 'Nova' or 'Pendente' or 'Em andamento':
            result = collection.update_one(
                {"_id": ObjectId(tarefa_id)},
                {"$set": {"situacao": "Cancelada",
                          "prioridade": 1}}
            )
            if result.modified_count == 1:
                # Convertendo o ObjectId para string antes de chamar o jsonable_encoder
                tarefa_atual["_id"] = str(tarefa_atual["_id"])
                tarefa_atual = jsonable_encoder(tarefa_atual)
                return tarefa_atual
            raise HTTPException(status.HTTP_200_OK,
                                detail=f"Tarefa {tarefa_id} cancelada com sucesso")

        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"Para atualizarmos a situação da tarefa {tarefa_id} sua situação deve ser 'Em andamento' ")
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Tarefa de ID {tarefa_id} não encontrada')
