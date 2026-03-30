# 🍳 Assistente Inteligente de Receitas do YouTube

Você já assistiu a um vídeo de uma receita incrível no YouTube, mas ficou com preguiça de pausar o vídeo várias vezes para anotar os ingredientes e o passo a passo? 

Este projeto resolve exatamente esse problema! Criamos um **Assistente Inteligente** que "assiste" ao vídeo por você, escuta o que o chef está dizendo e transforma isso em uma receita escrita, organizada e pronta para você cozinhar.

---

## 🌟 O que o nosso sistema faz?

Tudo o que você precisa fazer é **copiar o link de um vídeo de culinária do YouTube** e colar na nossa ferramenta. A partir daí, a "Mágica" (também conhecida como Inteligência Artificial) acontece:

1. **Ouvidos Atentos**: O sistema baixa o áudio do vídeo e usa uma inteligência artificial avançada para "escutar" e transcrever tudo o que foi falado.
2. **Leitura e Compreensão**: Outra inteligência artificial, treinada para entender textos, lê essa gigantesca transcrição, separa as histórias ou brincadeiras do cozinheiro e foca no que importa: **Ingredientes** e **Modo de Preparo**.
3. **Sua Receita Pronta**: Em questão de segundos ou poucos minutos, ele te entrega a receita formatada de forma bonitinha, separando os ingredientes, as medidas corretas e listando os passos de forma clara.

---

## 🚀 Como usar a aplicação?

Nossa plataforma foi pensada para ser extremamente fácil de usar.

1. **Abra o aplicativo**: Você verá uma página inicial simples e amigável.
2. **Cole o Link**: Na caixa de texto indicada, cole a URL (o link) do vídeo do YouTube e clique no botão para gerar a receita.
3. **Aguarde a IA trabalhar**: Em alguns instantes, a receita vai pipocar na sua tela.
4. **Salve para depois**: Gostou? Você pode clicar no botão **"Salvar Receita"**! O sistema guarda a receita no nosso banco de dados, e você pode acessá-la a qualquer momento na aba **Receitas Salvas**.

---

## 🧠 Para os curiosos: Como funciona "por baixo dos panos"?

Embora o uso seja super natural, nos bastidores o sistema orquestra tecnologias modernas para tudo isso funcionar de forma rápida:

* **Interface Visual (Onde você clica)**: Criada com uma tecnologia chamada `Streamlit`, que permite criar telas de aplicativos direto com Python.
* **Transcrição (De Áudio para Texto)**: Utilizamos modelos de reconhecimento de fala da OpenAI (Whisper), executados em processadores ultrarrápidos graças à plataforma da **Groq**.
* **Inteligência Artificial "Cerebral"**: Usamos modelos de linguagem de última geração que são controlados por uma arquitetura em "Grafo" (agentes de IA que conversam entre si para garantir que a receita não tenha erros).
* **Banco de Dados**: Utilizamos o MongoDB para guardar as suas receitas favoritas na nuvem de forma segura.

---

*Transforme qualquer vídeo do YouTube em sua próxima criação culinária. Bom apetite!* 👨‍🍳👩‍🍳
