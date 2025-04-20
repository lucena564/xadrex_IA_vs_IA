import openai
import json
import os
import requests
from openai.types.chat.completion_create_params import ResponseFormat
from dotenv import load_dotenv
from openai import OpenAI

# Carregar as variáveis do arquivo .env
load_dotenv()

class OpenAIAgent:
    def __init__(self, api_key: str, model="gpt-4o-mini"):
        """Inicializa a classe com a chave da API da OpenAI e o modelo."""
        self.api_key = api_key
        self.model = model
        self.instruction = None
        self.context = "A partida ainda não começou. Você está com as peças brancas. Escolha o seu movimento inicial."  

    def load_instruction(self, instruction: str):
        """Carrega a instrução inicial do agente."""
        self.instruction = instruction
        self.context = instruction  # Inicializa o contexto com a instrução

    def interact_with_agent(self, prompt: str):
        """Interage com o modelo da OpenAI com base no contexto e no prompt dado."""
        CHAVE_DA_OPEN_AI=self.api_key
        client = OpenAI(api_key=CHAVE_DA_OPEN_AI)
        try:
            resposta = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"""Você está jogando xadrez. Para cada movimento, você deve responder com o movimento em notação algébrica. Você pode usar a notação "e4" para mover um peão para e4, "Nf3" para mover um cavalo para f3, etc. Não forneça explicações ou justificativas. Além disso, você irá saber o estado atual do tabuleiro para decidir a sua jogada.

Estado atual do tabuleiro: {self.context}

Responda **apenas** assim: {{ "jogada": "e4" }}."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
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