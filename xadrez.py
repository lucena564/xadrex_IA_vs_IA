class Peca:
    def __init__(self, cor):
        self.cor = cor

    def movimento_valido(self, origem, destino, tabuleiro):
        return False

class Torre(Peca):
    def movimento_valido(self, origem, destino, tabuleiro):
        return origem[0] == destino[0] or origem[1] == destino[1]

class Bispo(Peca):
    def movimento_valido(self, origem, destino, tabuleiro):
        return abs(ord(origem[0]) - ord(destino[0])) == abs(int(origem[1]) - int(destino[1]))

class Rainha(Peca):
    def movimento_valido(self, origem, destino, tabuleiro):
        return Torre(self.cor).movimento_valido(origem, destino, tabuleiro) or Bispo(self.cor).movimento_valido(origem, destino, tabuleiro)

class Cavalo(Peca):
    def movimento_valido(self, origem, destino, tabuleiro):
        dx = abs(ord(origem[0]) - ord(destino[0]))
        dy = abs(int(origem[1]) - int(destino[1]))
        return (dx, dy) in [(2, 1), (1, 2)]

class Rei(Peca):
    def movimento_valido(self, origem, destino, tabuleiro):
        return max(abs(ord(origem[0]) - ord(destino[0])), abs(int(origem[1]) - int(destino[1]))) == 1

class Peao(Peca):
    def movimento_valido(self, origem, destino, tabuleiro):
        direcao = 1 if self.cor == 'branco' else -1
        linha_atual = int(origem[1])
        linha_destino = int(destino[1])

        # Movimento de uma casa para frente
        if origem[0] == destino[0] and linha_destino - linha_atual == direcao:
            return True

        # Movimento de duas casas na primeira jogada
        if origem[0] == destino[0] and linha_destino - linha_atual == 2 * direcao:
            if (self.cor == 'branco' and linha_atual == 2) or (self.cor == 'preto' and linha_atual == 7):
                # Verificar se a casa intermediária está vazia
                casa_intermediaria = f"{origem[0]}{linha_atual + direcao}"
                return casa_intermediaria not in tabuleiro and destino not in tabuleiro

        return False

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = {
            "A1": Torre('branco'), "H1": Torre('branco'), "A8": Torre('preto'), "H8": Torre('preto'),
            "C1": Bispo('branco'), "F1": Bispo('branco'), "C8": Bispo('preto'), "F8": Bispo('preto'),
            "D1": Rainha('branco'), "D8": Rainha('preto'),
            "B1": Cavalo('branco'), "G1": Cavalo('branco'), "B8": Cavalo('preto'), "G8": Cavalo('preto'),
            "E1": Rei('branco'), "E8": Rei('preto'),
            **{f"{c}2": Peao('branco') for c in "ABCDEFGH"},
            **{f"{c}7": Peao('preto') for c in "ABCDEFGH"}
        }

    def exibir(self):
        print("    A    B    C    D    E    F    G    H")
        print("  +----+----+----+----+----+----+----+----+")
        for i in range(8, 0, -1):
            linha = [f"{i} |"]
            for c in "ABCDEFGH":
                peca = self.tabuleiro.get(f"{c}{i}", None)
                if peca:
                    cor_prefixo = 'b' if peca.cor == 'branco' else 'p'
                    tipo = 'Q' if isinstance(peca, Rainha) else 'K' if isinstance(peca, Rei) else peca.__class__.__name__[0]
                    linha.append(f"{cor_prefixo}{tipo} |")
                else:
                    linha.append("   |")
            print(" ".join(linha))
            print("  +----+----+----+----+----+----+----+----+")
        print("     A    B    C    D    E    F    G    H\n")

    def mover(self, origem, destino):
        if origem in self.tabuleiro and self.tabuleiro[origem]:
            peca = self.tabuleiro[origem]
            if peca.movimento_valido(origem, destino, self.tabuleiro):
                self.tabuleiro[destino] = peca
                del self.tabuleiro[origem]
                return True
            else:
                print("Movimento inválido!")
        else:
            print("Nenhuma peça na posição informada!")
        return False

def jogar():
    tabuleiro = Tabuleiro()
    turno = 'branco'
    while True:
        tabuleiro.exibir()
        print(f"Turno do {turno}!")
        origem = input("Origem (ex: E2): ")
        destino = input("Destino (ex: E4): ")
        if tabuleiro.mover(origem, destino):
            turno = 'preto' if turno == 'branco' else 'branco'

if __name__ == "__main__":
    jogar()
