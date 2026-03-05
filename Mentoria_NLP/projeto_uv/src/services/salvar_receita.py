from pymongo.errors import DuplicateKeyError
from src.database.mongo import get_database


def buscar_receita_por_url(video_url):

    db = get_database()
    colecao = db["receitas"]

    receita = colecao.find_one({
        "video_url": video_url
    })

    return receita

def salvar_receita(receita_dict):

    db = get_database()
    colecao = db["receitas"]

    try:
        resultado = colecao.insert_one(receita_dict)
        return resultado.inserted_id

    except DuplicateKeyError:

        receita = colecao.find_one({
            "video_url": receita_dict["video_url"]
        })

        return receita["_id"]