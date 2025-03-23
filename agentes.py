import openai
import json
from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Recuperar a chave da API da OpenAI do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Função para carregar o prompt do arquivo JSON
def load_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get("prompt", "")

# Função para interagir com o modelo da OpenAI
def interact_with_agent(prompt):
    try:
        # Chamada para a API da OpenAI (GPT-3 ou GPT-4)
        response = openai.Completion.create(
            model="gpt-4o",  # Ou o modelo que você estiver usando, como gpt-4
            prompt=prompt,
            max_tokens=150,  # Ajuste conforme necessário
            temperature=0.7  # Ajuste a criatividade da resposta
        )
        # Retorna a resposta do modelo
        return response.choices[0].text.strip()
    
    except Exception as e:
        print(f"Erro ao chamar a API: {e}")
        return None
    
# Carregar o prompt do arquivo JSON
prompt = load_prompt_from_file("prompt.json")

# Interagir com o modelo
if prompt:
    response = interact_with_agent(prompt)
    if response:
        print(f"Resposta do agente: {response}")
    else:
        print("Não foi possível obter uma resposta.")
else:
    print("Prompt não encontrado no arquivo.")