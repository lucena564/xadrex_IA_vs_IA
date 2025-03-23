from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import chess

app = FastAPI()

# Montando arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

board = chess.Board()  # Cria uma nova instância do jogo

class MoveRequest(BaseModel):
    move: str

def get_board_state():
    """
    Retorna o estado atual do tabuleiro como uma string formatada.
    """
    pecas_letras = {
        'r': 'pT', 'n': 'pC', 'b': 'pB', 'q': 'pQ', 'k': 'pK', 'p': 'pP',
        'R': 'bT', 'N': 'bC', 'B': 'bB', 'Q': 'bQ', 'K': 'bK', 'P': 'bP'
    }

    board_str = str(board).split("\n")
    tabuleiro_formatado = ["      A      B      C      D      E      F      G      H"]
    tabuleiro_formatado.append("  +------+------+------+------+------+------+------+------+")

    for i, row in enumerate(board_str):
        linha = [f"{8 - i} |"]
        for casa in row.split():
            if casa in pecas_letras:
                linha.append(f" {pecas_letras[casa]}  |")
            else:
                linha.append("     |")
        tabuleiro_formatado.append(" ".join(linha))
        tabuleiro_formatado.append("  +------+------+------+------+------+------+------+------+")

    tabuleiro_formatado.append("      A      B      C      D      E      F      G      H\n")
    return "\n".join(tabuleiro_formatado)


# @app.get("/", response_class=HTMLResponse)
# def read_root():
#     """
#     Endpoint que retorna o estado atual do tabuleiro de xadrez com a interface em HTML.
#     """
#     html_content = f"""
#     <html lang="pt">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <link rel="stylesheet" type="text/css" href="/static/css/style.css">
#             <title>Xadrez: IA vs IA</title>
#         </head>
#         <body>
#             <div class="container">
#                 <header>
#                     <h1>Xadrez: IA vs IA</h1>
#                     <p>Jogo de Xadrez entre duas Inteligências Artificiais</p>
#                 </header>
#                 <section class="board">
#                     <h2>Tabuleiro de Xadrez</h2>
#                     <pre>{board.unicode()}</pre>
#                 </section>
#                 <footer>
#                     <button onclick="location.reload();">Atualizar Jogo</button>
#                 </footer>
#             </div>
#         </body>
#     </html>
#     """
#     return html_content

@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Endpoint que retorna o estado atual do tabuleiro de xadrez com a interface em HTML.
    """
    html_content = f"""
    <html lang="pt">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" type="text/css" href="/static/css/style.css">
            <title>Xadrez: IA vs IA</title>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Xadrez: IA vs IA</h1>
                    <p>Jogo de Xadrez entre ChatGPT e DeepSeek</p>
                </header>
                <div class="game-board">
                    <section class="player player1">
                        <h2>Jogador 1: ChatGPT (Peças Brancas)</h2>
                        <img src="/static/imgs/chatgpt.png" alt="ChatGPT" class="player-img">
                    </section>
                    <section class="board">
                        <h2>Tabuleiro de Xadrez</h2>
                        <pre>{board.unicode()}</pre>
                    </section>
                    <section class="player player2">
                        <h2>Jogador 2: DeepSeek (Peças Pretas)</h2>
                        <img src="/static/imgs/deepseek.png" alt="DeepSeek" class="player-img">
                    </section>
                </div>
                <footer>
                    <div class="messages-block">
                        <h3>Mensagens</h3>
                        <div class="messages">
                            <p>ChatGPT: Ainda não instanciado!</p>
                            <p>DeepSeek: Ainda não instanciado!</p>
                        </div>
                    </div>
                    <button onclick="location.reload();">Atualizar Jogo</button>
                </footer>
            </div>
        </body>
    </html>
    """
    return html_content

@app.post("/move/")
def make_move(move_request: MoveRequest):
    """
    Endpoint para realizar um movimento no tabuleiro.

    Exemplo de uso:
    - Enviar um JSON `{"move": "e4"}` para mover um peão para e4.

    Retorna:
    - Sucesso: Novo estado do tabuleiro
    - Erro: Mensagem de erro explicando o problema do movimento
    """
    try:
        move = move_request.move  # Acessa o movimento do corpo da requisição
        board.push_san(move)  # Tenta fazer o movimento
        return JSONResponse(content={"success": True, "tabuleiro": get_board_state()})

    except chess.IllegalMoveError:
        return JSONResponse(content={"success": False, "error": "Movimento ilegal! Tente outro."}, status_code=400)

    except chess.InvalidMoveError:
        return JSONResponse(content={"success": False, "error": "Movimento inválido! Verifique a notação."}, status_code=400)

    except chess.AmbiguousMoveError:
        return JSONResponse(content={"success": False, "error": "Movimento ambíguo! Especifique melhor."}, status_code=400)

    except chess.CheckError:
        return JSONResponse(content={"success": False, "error": "Movimento inválido! O rei está em cheque."}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
