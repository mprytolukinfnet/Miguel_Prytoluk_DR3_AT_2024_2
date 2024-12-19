**Assessment (AT)**

**Disciplina:** Desenvolvimento de Data-Driven Apps com Python

**Aluno:** Miguel Belardinelli Prytoluk

**Data:** 18/12/2024


## Descrição do Projeto
**Análise de Partidas de Futebol** é uma aplicação que utiliza LLMs e um dashboard streamlit para analisar partidas de futebol e a performance de jogadores.

## Objetivo
O objetivo principal da aplicação é facilitar a análise e interpretação de dados de futebol, oferecendo:

1. **Sumarização de Partidas**: Resumos detalhados dos principais eventos e destaques de uma partida.
2. **Perfil de Jogadores**: Análise individual de estatísticas de desempenho para jogadores específicos.
3. **Narrativas Personalizadas**: Criação de narrativas com estilos variados (formal, técnico ou humorístico) para enriquecer a experiência do usuário.

## Requisitos

- Python 3.10 ou superior
- `virtualenv` para criação de ambiente virtual
- Os pacotes listados no arquivo `requirements.txt`
- Uma chave de API Open AI

## Instruções para configurar o ambiente

### 1. Clonar o Repositório

Clone este repositório na sua máquina local.

```bash
git clone https://github.com/mprytolukinfnet/Miguel_Prytoluk_DR3_AT_2024_2.git
```

### 2. Criar um Ambiente Virtual

No diretório do projeto, crie um ambiente virtual usando `virtualenv`:

```bash
virtualenv venv
```

### 3. Ativar o Ambiente Virtual
- No Windows:
```bash
venv\Scripts\activate
```

- No Linux/Mac:
```bash
source venv/bin/activate
```

### 4. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

### 5. Variáveis de ambiente

Criar um arquivo `.env` na raiz do projeto contendo sua chave de API Open AI no formato:
```env
OPENAI_API_KEY=chave-open-ai
```

## Instruções para rodar o projeto

### Aplicação Streamlit
Para rodar a aplicação streamlit, execute o seguinte comando no terminal:
```bash
streamlit run main.py
```

### API
Para rodar a versão API da aplicação, execute o seguinte comando no terminal:
```bash
uvicorn: api:app
```

## Exemplo de utilização da API:

Documentação extensa da API em: http://127.0.0.1:8000/docs

### Sumarização de Partida:

**Requisição:**
```python
import requests

# URL base da API
BASE_URL = "http://127.0.0.1:8000"

# Dados para o teste
endpoint = "/match_summary"
payload = {
    "match_id": 3895302
}

# Realizando a requisição POST
response = requests.post(f"{BASE_URL}{endpoint}", json=payload)

print(response.json())
```

**Resposta:**
```json
{"match_id": 3895302,
 "summary": "O Bayer Leverkusen venceu o Werder Bremen por 5 a 0. Os destaques foram os gols de Victor Okoh Boniface aos 24 minutos (pênalti), Granit Xhaka aos 59 minutos, e Florian Wirtz, que marcou três vezes, aos 67, 82 e 89 minutos. Leonardo Bittencourt e Piero Martín Hincapié Reyna receberam cartões amarelos aos 46 minutos. Amine Adli entrou para substituir Florian Wirtz aos 45 minutos, enquanto Nathan Tella e Victor Okoh Boniface entraram no lugar de Jeremie Frimpong e Patrik Schick, respectivamente, aos 61 minutos."}
 ```

### Perfil de Jogador:
**Requisição:**
```python
endpoint = "/player_profile"  
payload = {
    "match_id": 3895302,
    "player_id": 40724
}  

response = requests.post(f"{BASE_URL}{endpoint}", json=payload)  

print(response.json())  
```
**Resposta:**
```json
{
  "match_id": 3895302,
  "player_id": 40724,
  "player_name": "Florian Wirtz",
  "profile": {
    "Gols": 3,
    "Assistências": 0,
    "Chutes": 5,
    "Finalizações-Gol (%)": 60.0,
    "Passes": 27,
    "Passes-Sucesso (%)": 92.6,
    "Dribles": 3,
    "Dribles-Sucesso (%)": 33.3,
    "Recepções": 37,
    "Recepções-Sucesso (%)": 86.5,
    "Interceptações": 2,
    "Interceptações-Sucesso (%)": 0.0
  }
}
```

### Narrativa de Partida:
**Requisição:**
```python
endpoint = "/match_narrative"  
payload = {
    "match_id": 3895302,
    "style": "humoristico"
}  

response = requests.post(f"{BASE_URL}{endpoint}", json=payload)  

print(response.json())  
```
**Resposta:**
```json
{
  "match_id": 3895302,
  "style": "humoristico",
  "narrative": "Em uma tarde ensolarada na Alemanha, o Bayer Leverkusen recebeu o Werder Bremen em um duelo que mais parecia uma aula de futebol sobre como não se deve defender. Florian Wirtz brilhou com três gols e mostrou que estava inspirado. Enquanto isso, o Werder Bremen parecia estar em um treinamento defensivo, mas para o time adversário. Uma partida que divertiu a todos, exceto os torcedores do Werder Bremen."
}
```

## Exemplo de interação com o Assistente na Aplicação Streamlit API:
### Número de passes
- **Quem deu mais passes na partida?**

-   O jogador que deu mais passes na partida foi Granit Xhaka, do Bayer Leverkusen.

-   **Quantos passes ele deu?**

-   Granit Xhaka deu um total de 122 passes na partida, com uma taxa de sucesso de 92.6%.

### Número de finalizações
- **Qual jogador teve mais finalizações no primeiro tempo?**

- No primeiro tempo, o jogador que teve mais finalizações foi Alejandro Grimaldo García, do Bayer Leverkusen, com um total de 2 chutes.

### Comparação de jogadores
- **Compare os jogadores Ermedin Demirović e Patrik Schick.**
- Aqui está a comparação entre Ermedin Demirović e Patrik Schick com base em suas estatísticas na partida:

    Ermedin Demirović
    - Gols: 0
    - Assistências: 0
    - Chutes: 2
    - Finalizações-Gol (%): 0.0
    - Passes: 19
    - Passes-Sucesso (%): 57.9
    - Dribles: 4
    - Dribles-Sucesso (%): 50.0
    - Recepções: 29
    - Recepções-Sucesso (%): 65.5
    - Interceptações: 1
    - Interceptações-Sucesso (%): 100.0

    Patrik Schick
    - Gols: 0
    - Assistências: 0
    - Chutes: 4
    - Finalizações-Gol (%): 0.0
    - Passes: 13
    - Passes-Sucesso (%): 84.6
    - Dribles: 3
    - Dribles-Sucesso (%): 33.3
    - Recepções: 40
    - Recepções-Sucesso (%): 52.5
    - Interceptações: 0
    - Interceptações-Sucesso (%): 0.0

    Análise Comparativa
    - Chutes: Schick teve mais chutes (4) em comparação a Demirović (2).
    - Passes: Demirović completou mais passes (19), mas com uma taxa de sucesso inferior (57.9%) em comparação com Schick (13 passes e 84.6% de sucesso).
    - Dribles: Demirović teve um desempenho melhor em dribles, com 50% de sucesso, enquanto Schick teve 33.3%.
    - Recepções: Schick teve mais recepções (40), mas com uma taxa de sucesso menor (52.5%) em relação a Demirović (29 recepções e 65.5% de sucesso).
    - Interceptações: Demirović conseguiu 1 interceptação com 100% de sucesso, enquanto Schick não teve interceptações.

    Ambos os jogadores não marcaram gols ou deram assistências na partida, mas tiveram desempenhos distintos em várias estatísticas.
### Resumo da partida
- **Gere um resumo da partida.**
- O Bayer Leverkusen venceu o Augsburg por 1 a 0. O destaque da partida foi o gol de Exequiel Alejandro Palacios aos 93 minutos, assistido por Alejandro Grimaldo García. O Augsburg teve dois jogadores amarelados: Ruben Vargas e Iago Amaral Borduchi, ambos no primeiro tempo. Além disso, ocorreram várias substituições no segundo tempo, incluindo a entrada de Adam Hložek no lugar de Florian Wirtz pelo Bayer Leverkusen e a troca de Ruben Vargas por Arne Maier pelo Augsburg.
### Narrativa da partida
- **Crie uma narrativa da partida em estilo humorístico**
- Era uma vez, no reino do futebol alemão, uma partida entre Augsburg e Bayer Leverkusen que prometia ser mais emocionante do que uma montanha-russa em um parque de diversões!

    Os torcedores de Augsburg chegaram ao estádio com a esperança de que seus jogadores estivessem mais afiados do que faca de chef, mas logo perceberam que o único que estava afiado era o goleiro Finn Dahmen, que fez mais defesas do que um super-herói tentando salvar o mundo. Enquanto isso, o Bayer Leverkusen parecia estar em um dia de "estou aqui só para me divertir", mas Patrik Schick decidiu que ele realmente queria ser o protagonista e marcou o único gol da partida.

    Os jogadores de Augsburg atacaram como se estivessem jogando um jogo de videogame, mas sempre acabavam perdendo a "vida" antes de conseguir marcar. Era como se cada vez que eles se aproximassem do gol, alguém dissesse: "Desculpe, você não tem permissão para entrar aqui!" Os defensores do Leverkusen estavam mais organizados do que uma reunião de família no Natal.

    E assim, com um gol e muitas tentativas frustradas, o Bayer Leverkusen saiu vitorioso, deixando os torcedores de Augsburg com a sensação de que deveriam ter trazido um pouco mais de sorte e talvez uma pitada de magia. No final, o único que riu foi Patrik Schick, que provavelmente já estava pensando na próxima partida enquanto os jogadores do Augsburg tentavam entender como ter mais sorte na próxima vez.

    E assim, a partida terminou 1 a 0, mas a verdadeira vitória foi para o humor, que sempre faz parte do belo jogo!

## Estrutura do Projeto
- **app.py**: Contém o código principal da aplicação streamlit.
- **api.py**: Contém o código principal da API.
- **agent/agent.py**: Contém a lógica para criar um Agente ReAct.
- **controllers/controllers.py**: Contém as funções utilizadas pelos endpoints da API.
- **data/loader.py**: Contém as funções necessárias para carregar os dados nas aplicações.
- **models/models.py**: Contém os modelos Pydantic utilizados pelos endpoints da API.
- **st_pages/**: Contém as páginas da aplicação Streamlit.
- **tools/soccer.py**: Carrega e configura as ferramentas (tools) a serem utilizadas pelo Agente.
- **requirements.txt**: Lista de dependências necessárias para rodar o projeto.
