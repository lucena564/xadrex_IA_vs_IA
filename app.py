from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import chess

app = FastAPI()

# Montando arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

board = chess.Board()

class MoveRequest(BaseModel):
    move: str

move_history = []

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

def get_board_representations():
    """
    Retorna o estado do tabuleiro em três formatos:
    1. Notação FEN
    2. Lista de posições (JSON)
    3. Matriz 2D (JSON)
    """
    # 1. Notação FEN
    fen = board.fen()

    # 2. Lista de posições (JSON)
    piece_dict = {
        'pT': [], 'pC': [], 'pB': [], 'pQ': [], 'pK': [], 'pP': [],
        'bT': [], 'bC': [], 'bB': [], 'bQ': [], 'bK': [], 'bP': []
    }
    
    piece_symbols = {
        'r': 'pT', 'n': 'pC', 'b': 'pB', 'q': 'pQ', 'k': 'pK', 'p': 'pP',
        'R': 'bT', 'N': 'bC', 'B': 'bB', 'Q': 'bQ', 'K': 'bK', 'P': 'bP'
    }

    files = "ABCDEFGH"
    board_matrix = [["" for _ in range(8)] for _ in range(8)]  # Inicializa matriz vazia

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece.symbol()
            mapped_piece = piece_symbols[piece_type]

            rank = 8 - (square // 8)
            file = files[square % 8]
            position = f"{file}{rank}"

            piece_dict[mapped_piece].append(position)
            board_matrix[8 - rank][square % 8] = mapped_piece

    return {
        "FEN": fen,
        "Lista de Posições": piece_dict,
        "Matriz 2D": board_matrix
    }

@app.get("/board/representations")
def get_representations():
    """Endpoint para obter o estado do tabuleiro em diferentes formatos."""
    return JSONResponse(content=get_board_representations())

@app.get("/refresh", response_class=HTMLResponse)
def refresh_board():
    return read_root()

@app.get("/", response_class=HTMLResponse)
def read_root():
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
                        <div id="tabuleiro"><pre>{board.unicode(invert_color=True)}</pre></div>
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
                            <p>DeepSeek: <span id="jogada-chatgpt">Carregando...</span></p>
                            <p>ChatGPT: <span id="jogada-deepseek">Carregando...</span></p>
                        </div>
                    </div>
                    <button onclick="location.reload();">Atualizar Jogo</button>
                </footer>
            </div>

            <script>
                async function atualizarTabuleiro() {{
                    try {{
                        const resposta = await fetch('/estado');
                        const html = await resposta.text();
                        document.getElementById('tabuleiro').innerHTML = html;
                    }} catch (erro) {{
                        console.error('Erro ao atualizar o tabuleiro:', erro);
                    }}

                    try {{
                        const resposta = await fetch('/ultimas-jogadas');
                        const jogadas = await resposta.json();
                        
                        document.getElementById('jogada-chatgpt').innerText = jogadas.chatgpt || 'Aguardando jogada...';
                        document.getElementById('jogada-deepseek').innerText = jogadas.deepseek || 'Aguardando jogada...';
                    }} catch (erro) {{
                        console.error('Erro ao buscar jogadas:', erro);
                    }}
                }}

                setInterval(atualizarTabuleiro, 2000);
            </script>
        </body>
    </html>
    """
    return html_content

@app.get("/ultimas-jogadas")
def ultimas_jogadas():
    """
    Retorna as últimas jogadas de cada jogador.
    """
    return JSONResponse(content={
        "chatgpt": jogada_chatgpt if jogada_chatgpt else 'Aguardando jogada...',
        "deepseek": jogada_deepseek if jogada_deepseek else 'Aguardando jogada...'
    })

@app.get("/estado", response_class=HTMLResponse)
def estado_tabuleiro():
    return f"<pre>{board.unicode(invert_color=True)}</pre>"

jogada_chatgpt = "Aguardando jogada..."
jogada_deepseek = "Aguardando jogada..."

@app.post("/move/")
def make_move(move_request: MoveRequest):
    """
    Endpoint para realizar um movimento no tabuleiro.

    Exemplo de uso:
    - Enviar um JSON `{"move": "e4"}` para mover um peão para e4.
    """
    global jogada_chatgpt, jogada_deepseek

    try:
        move = move_request.move 
        board.push_san(move)

        if board.turn == chess.WHITE:
            jogada_chatgpt = move
        else:
            jogada_deepseek = move

        return JSONResponse(content={"success": True, "tabuleiro": get_board_state()})

    except chess.IllegalMoveError:
        return JSONResponse(content={"success": False, "error": f"Movimento ilegal! Tente outro. Movimentos disponíveis: {[board.san(move) for move in board.legal_moves]}"}, status_code=400)

    except chess.InvalidMoveError:
        return JSONResponse(content={"success": False, "error": f"Movimento inválido! Verifique a notação. Movimentos disponíveis: {[board.san(move) for move in board.legal_moves]}"}, status_code=400)

    except chess.AmbiguousMoveError:
        return JSONResponse(content={"success": False, "error": f"Movimento ambíguo! Especifique melhor. Movimentos disponíveis: {[board.san(move) for move in board.legal_moves]}"}, status_code=400)

    except chess.CheckError:
        return JSONResponse(content={"success": False, "error": f"Movimento inválido! O rei está em cheque. Movimentos disponíveis: {[board.san(move) for move in board.legal_moves]}"}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
