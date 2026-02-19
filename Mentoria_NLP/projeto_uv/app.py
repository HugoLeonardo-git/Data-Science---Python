import sys
from src.models.fluxo_gerador_receita.grafo import fluxo_resumo
from src.models.fluxo_gerador_receita.estado import EstadoReceita


def main():

    if len(sys.argv) < 2:
        print("Uso: python main.py <url_youtube>")
        return

    url = sys.argv[1]

    print(f"Processando URL: {url}")

    # Inicializa estado
    estado_inicial = EstadoReceita(url_video=url)

    # Cria grafo
    grafo = fluxo_resumo()

    print("Iniciando execução do grafo...")
    # Executa o grafo (invoke retorna o estado final)
    estado_final = grafo.invoke(estado_inicial)

    print("\n=== RECEITA GERADA ===\n")
    
    # Tenta acessar como objeto ou dicionário para evitar erro
    receita = getattr(estado_final, "receita_gerada", None)
    if receita is None and isinstance(estado_final, dict):
        receita = estado_final.get("receita_gerada")

    if receita:
        # Se for modelo Pydantic
        if hasattr(receita, "model_dump_json"):
             print(receita.model_dump_json(indent=2))
        elif hasattr(receita, "json"):
             # Fallback for V1
             try:
                print(receita.json(indent=2, ensure_ascii=False))
             except TypeError:
                print(receita.json())
        # Se for dict (caso tenha sido convertido)
        elif isinstance(receita, dict):
             import json
             print(json.dumps(receita, indent=2, ensure_ascii=False))
        else:
             print(receita)
    else:
        print("Nenhuma receita foi gerada.")




if __name__ == "__main__":
    main()
