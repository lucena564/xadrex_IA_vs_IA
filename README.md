# ♟️ Xadrez: ChatGPT vs DeepSeek

<p align="center">
  <img src="https://i.imgur.com/eIuZnfZ.gif" alt="Demonstração" width="75%">
</p>

Este projeto implementa uma partida de xadrez entre duas inteligências artificiais: **ChatGPT** (usando a API da OpenAI) e **DeepSeek** (usando a API da DeepSeek), com uma interface simples em **FastAPI** exibindo o estado do tabuleiro em tempo real.

---

## 🚀 Funcionalidades

- Tabuleiro exibido em formato Unicode e atualizado automaticamente.
- Interface HTML responsiva via FastAPI.
- Integração com APIs da OpenAI e DeepSeek para movimentação.
- Detecção de movimentos inválidos com nova tentativa automática.
- Log de jogadas e histórico atualizado a cada 2 segundos.
- Representação do estado do tabuleiro em:
  - Notação FEN
  - Lista de posições em JSON
  - Matriz 2D (JSON)

---

## 🧠 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) – Backend e rotas da aplicação
- [chess](https://python-chess.readthedocs.io/) – Manipulação do tabuleiro e regras do xadrez
- [OpenAI API](https://platform.openai.com/) – Para o ChatGPT
- [DeepSeek API](https://deepseek.com/) – Para o DeepSeek Reasoner
- [Selenium](https://www.selenium.dev/) – (opcional para interações automatizadas)
- [dotenv](https://pypi.org/project/python-dotenv/) – Carregamento de variáveis de ambiente

---

## 📁 Estrutura Básica

```
📦 projeto_xadrez_ia
├── main.py                 # Servidor FastAPI com exibição do tabuleiro
├── manager.py              # Classe Menager que controla a lógica da partida
├── static/
│   ├── css/style.css       # Estilo do HTML
│   └── imgs/               # Imagens dos jogadores (chatgpt.png, deepseek.png)
└── .env                    # Contém as chaves de API
```

---

## ⚙️ Como Executar

### 1. Instalar dependências
```bash
pip install fastapi uvicorn python-dotenv requests openai selenium python-chess
```

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` com as chaves das APIs:
```
OPENAI_API_KEY=your_openai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### 3. Rodar o servidor FastAPI
```bash
uvicorn main:app --reload
```

### 4. Rodar a partida (em outro script ou terminal)
```python
from ia_manager import Menager

manager = Menager(api_key_openai="sua_key", api_key_deepseek="sua_key")
while True:
    manager.single_moviment()
```

---

## 🔁 Atualização do Tabuleiro
A interface HTML atualiza automaticamente a cada 2 segundos usando `fetch` com JavaScript.

As jogadas mais recentes de cada IA são mostradas abaixo do tabuleiro com base no controle de estado interno.

---

## 🧠 Lógica de Alternância
- O jogador 1 é o ChatGPT (peças brancas).
- O jogador 2 é o DeepSeek (peças pretas).
- A cada jogada, a IA analisa o estado atual (FEN + contexto) e responde com o próximo movimento.
- Em caso de erro (jogada inválida, ilegal ou ambígua), o prompt é ajustado e a IA tenta novamente.

---

## 🔧 Endpoints Principais (FastAPI)

- `GET /` – Exibe o tabuleiro e interface HTML.
- `POST /move/` – Envia um movimento no formato `{ "move": "e4" }`
- `GET /estado` – Retorna o tabuleiro Unicode.
- `GET /board/representations` – Retorna FEN, lista de posições e matriz 2D.
- `GET /ultimas-jogadas` – Retorna as últimas jogadas de cada IA.

---

## 📹 Demonstração

Veja a partida em ação neste GIF:

📺 https://i.imgur.com/OsiEIal.gif

---

## 📌 Notas Finais

Este projeto tem fins educacionais e demonstrativos, mostrando como diferentes modelos LLMs podem competir em um ambiente lógico como o xadrez. Para produção, melhorias em segurança, desempenho e controle de tempo seriam necessárias.

Sinta-se à vontade para modificar, treinar novas IAs ou testar diferentes estratégias de prompt!

---

**Desenvolvido com 🧠 por [Você]**

