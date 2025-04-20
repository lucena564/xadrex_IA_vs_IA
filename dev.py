from agentes import OpenAIAgent
import json
import os

# Recupera a chave da API da OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Instancia a classe do agente
agent = OpenAIAgent(api_key)

# Carregar a instrução para o agente
with open("prompt.json", "r") as file:
    instructions = json.load(file)

agent.load_instruction(instructions['prompt'])

# Interagir com o agente com uma pergunta específica
question = "Qual é o melhor movimento para as brancas após 1. e4 e5?"
response = agent.interact_with_agent(question)

if response:
    print(f"Resposta do agente: {response}")
else:
    print("Não foi possível obter uma resposta.")

# # Exemplo de movimentação de peça de xadrez
# move = "e2e4"  # Exemplo de movimento de xadrez
# move_response = agent.make_move(move)
# if move_response:
#     print(f"Resposta da movimentação: {move_response}")
# else:
#     print("Não foi possível realizar a movimentação.")