import openai
import json
import os
import requests
from openai.types.chat.completion_create_params import ResponseFormat
from dotenv import load_dotenv
from openai import OpenAI
from selenium import webdriver

# Carregar as variáveis do arquivo .env
load_dotenv()

class Menager:
    def __init__(self, api_key_openai: str, api_key_deepseek: str, model_openai="gpt-4o-mini", model_deepseek="deepseek-reasoner"):
        """Inicializa a classe com a chave da API da OpenAI e o model_openaio."""
        self.api_key_openai = api_key_openai
        self.api_key_deepseek = api_key_deepseek
        self.model_openai = model_openai
        self.model_deepseek = model_deepseek
        self.context = ''
        self.last_move = None
        self.flag_openai = True
        self.cont_rep = 0
        self.erro = False
        self.erro_prompt = ""

    def set_last_move(self, move: str):
        """Define o último movimento realizado pelo agente."""
        self.last_move = move

    def interact_with_OpenAI(self, prompt: str, context="A partida ainda não começou, escolha o seu primeiro movimento"):
        self.context = context
        CHAVE_DA_OPEN_AI=self.api_key_openai
        client = OpenAI(api_key=CHAVE_DA_OPEN_AI)
        try:
            resposta = client.chat.completions.create(
                model=self.model_openai,
                messages=[
                    {"role": "system", "content": f"""Você está jogando xadrez. Para cada movimento, você deve responder com o movimento em notação algébrica. Você pode usar a notação "e4" para mover um peão para e4, "Nf3" para mover um cavalo para f3, etc. Não forneça explicações ou justificativas. Além disso, você irá saber o estado atual do tabuleiro para decidir a sua jogada.

Estado atual do tabuleiro: {self.context}

Responda **apenas** assim: {{ "move": "<movimentação_da_peça>" }}."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
                )
            return json.loads(resposta.choices[0].message.content)
        except Exception as e:
            return f"Erro ao obter resposta: {str(e)}"
        
    def interact_with_DeepSeek(self, prompt: str, context="Você é o jogador com as peças pretas."):
        self.context = context
        CHAVE_DO_DEEPSEEK=self.api_key_deepseek
        client = OpenAI(api_key=CHAVE_DO_DEEPSEEK, base_url="https://api.deepseek.com")
        try:
            resposta = client.chat.completions.create(
                model=self.model_deepseek,
                messages=[
                    {"role": "system", "content": f"""Você está jogando xadrez com as peças pretas. Para cada movimento, você deve responder com o movimento em notação algébrica. Você pode usar a notação "e4" para mover um peão para e4, "Nf3" para mover um cavalo para f3, etc. Não forneça explicações ou justificativas. Além disso, você irá saber o estado atual do tabuleiro para decidir a sua jogada.

Estado atual do tabuleiro: {self.context}

Responda **apenas** assim: {{ "move": "<movimentação_da_peça>" }}."""},
                    {"role": "user", "content": prompt}
                ],
                stream=False
                )
            return json.loads(resposta.choices[0].message.content)
        except Exception as e:
            return f"Erro ao obter resposta: {str(e)}"
    
    def make_move(self, move: str):
        """Fazer uma movimentação de uma peça de xadrez chamando o servidor local."""
        try:
            response = requests.post("http://localhost:8000/move", json={"move": move})
            if response.status_code == 200:
                return response.json()
            else:
                return f"Erro ao fazer a movimentação: {response.status_code}"
        except Exception as e:
            print(f"Erro ao fazer a movimentação: {e}")
            return None
        
    def single_moviment(self, cont=0):
        """Processo para realizar um movimento da partida. Tanto para o jogador 1 quanto para o jogador 2."""
        
        # Pegando o estado atual do tabuleiro
        url_satate_board = "http://localhost:8000/board/representations"

        payload_state_board = {}
        headers_state_board = {}

        state_board = requests.request("GET", url_satate_board, headers=headers_state_board, data=payload_state_board)

        # Tratando inicio da partida
        if self.last_move == None:
            prompt = "A partida ainda não começou. Você é o jogador 1 e deve fazer a primeira jogada. Escolha o seu movimento."
        else:
            if self.erro == True:
                prompt = self.erro_prompt
                self.erro == False
            else:
                prompt = f"Qual o seu próximo movimento? Jogada do último jogador: {self.last_move}"

        # Verificando qual agente deve jogar
        if self.flag_openai:
            print(json.dumps(state_board.text))
            print(prompt)
            jogada = self.interact_with_OpenAI(prompt, json.dumps(state_board.text))
            print(f"OpenAI output: {jogada}")
            
            self.flag_openai = False
        else:
            print(json.dumps(state_board.text))
            print(prompt)
            jogada = self.interact_with_DeepSeek(prompt, json.dumps(state_board.text))
            print(f"DeepSeek output: {jogada}")
            self.flag_openai = True

        # Verificando se o movimento foi válido
        url = "http://localhost:8000/move/"

        payload = json.dumps(jogada)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text)

        if response['success'] == False:
            if self.flag_openai:
                self.flag_openai = False
                self.erro = True
            else:
                self.flag_openai = True
                self.erro = True

            posicoes = json.loads(state_board.text)
            posicoes = posicoes['FEN']
            self.erro_prompt = prompt = f"Você está jogando xadrez contra um outro jogador. Você deve escolher o seu próximo movimento sabendo que o movimento do último jogador foi: {self.last_move}. Você tentou realizar uma movimentação inválida por isso você deve fazer uma nova escolha de peças para a sua próxima jogada. Vou disponibilizar o estado do tabuleiro atual e também as peças que você tem disponível para jogar. Estado atual do tabuleiro: {json.dumps(posicoes)}, Peças disponíveis para jogar: {response['error']}. Escolha o seu movimento."
            print(cont)
            self.single_moviment(cont+1)

            if cont > 3:
                return "self.cont_rep = 3. Critério de parada atingido."

        else:
            self.set_last_move(jogada)
            if self.flag_openai:
                print(f"\nJogador 2 (DeepSeek) jogou: {jogada}\n-----------------------------------------------------")
            else:
                print(f"\nJogador 1 (OpenAI) jogou: {jogada}\n-----------------------------------------------------")
            self.erro = False