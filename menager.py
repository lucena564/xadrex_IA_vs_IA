import openai
import json
import os
import requests
from openai.types.chat.completion_create_params import ResponseFormat
from dotenv import load_dotenv
from openai import OpenAI

# Carregar as variáveis do arquivo .env
load_dotenv()

class Menager:
    def __init__(self, api_key_openai: str, api_key_deepseek: str, model_openai="gpt-4o-mini", model_deepseek="deepseek-chat"):
        """Inicializa a classe com a chave da API da OpenAI e o model_openaio."""
        self.api_key_openai = api_key_openai
        self.api_key_deepseek = api_key_deepseek
        self.model_openai = model_openai
        self.model_deepseek = model_deepseek
        self.context = ''
        self.last_move = None  

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
                    {"role": "system", "content": f"""Você está jogando xadrez. Para cada movimento, você deve responder com o movimento em notação algébrica. Você pode usar a notação "e4" para mover um peão para e4, "Nf3" para mover um cavalo para f3, etc. Não forneça explicações ou justificativas. Além disso, você irá saber o estado atual do tabuleiro para decidir a sua jogada.

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