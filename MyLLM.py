import os
from litellm import completion

from dotenv import load_dotenv


import traceback

# Carregar variáveis de ambiente
load_dotenv()

# Obter a chave da API GROQ
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Obter a chave da API OPENROUTER
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

class CustomLLM(LLM):
    def __init__(self):
        self.groq_model = "groq/llama3-8b-8192"  # substitua pelo nome correto do modelo da Groq
        self.openrouter_model = "openrouter/meta-llama/llama-3.2-3b-preview"
        print("✅ CustomLLM foi instanciado")
        
        @property
        def type(self) -> str:
            return "custom"

        # Inicializa a classe base LLM com o modelo principal
        super().__init__(model=self.groq_model)

    def complete2(self, messages, **kwargs):
        try:
            print("GROQ")
            response = completion(
                model=self.groq_model,
                messages=messages,
                api_key=os.getenv("GROQ_API_KEY")
            )
            #return response['choices'][0]['message']['content']
            content = response['choices'][0]['message']['content']
            return f"[Modelo usado: {self.groq_model}]\n\n{content}"
        except Exception as e:
            print("Erro com Groq, fallback para OpenRouter:", e)
            response = completion(
                model=self.openrouter_model,
                messages=messages,
                api_key=os.getenv("OPENROUTER_API_KEY")
            )
            #return response['choices'][0]['message']['content']
            content = response['choices'][0]['message']['content']
            return f"[Modelo usado: {self.openrouter_model}]\n\n{content}"
            
    def complete(self, messages, **kwargs):
        try:
            print("Tentando Groq")
            response = completion(
            model=self.groq_model,
            messages=messages,
            api_key=os.getenv("GROQ_API_KEY")
        )
            content = response['choices'][0]['message']['content']
            return f"[Modelo usado: {self.groq_model}]\n\n{content}"
        except Exception as e:
            print("Erro com Groq:", e)
            traceback.print_exc()  # 👈 mostra detalhes da exceção
            try:
                print("Tentando OpenRouter")
                response = completion(
                model=self.openrouter_model,
                messages=messages,
                api_key=os.getenv("OPENROUTER_API_KEY")
            )
                content = response['choices'][0]['message']['content']
                return f"[Modelo usado: {self.openrouter_model}]\n\n{content}"
            except Exception as e2:
                print("Erro com OpenRouter:", e2)
                traceback.print_exc()
                return "[Erro] Nenhum modelo pôde ser executado."