from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import chess
import chess.svg
from fastapi.responses import JSONResponse

app = FastAPI()
board = chess.Board()  # Cria uma nova instância do jogo


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


@app.get("/")
def read_root():
    """
    Endpoint que retorna o estado atual do tabuleiro de xadrez.
    """
    # return JSONResponse(content={"tabuleiro": get_board_state()})
    return PlainTextResponse(board.unicode())


@app.post("/move/")
def make_move(move: str):
    """
    Endpoint para realizar um movimento no tabuleiro.

    Exemplo de uso:
    - Enviar um JSON `{"move": "e4"}` para mover um peão para e4.

    Retorna:
    - Sucesso: Novo estado do tabuleiro
    - Erro: Mensagem de erro explicando o problema do movimento
    """
    try:
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