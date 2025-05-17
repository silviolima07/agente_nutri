# llm_custom.py
import os
from dotenv import load_dotenv
from litellm import completion
import traceback

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

GROQ_MODEL = "groq/llama3-8b-8192"
OPENROUTER_MODEL = "openrouter/meta-llama/llama-3.2-3b-preview"

def custom_llm_completion(messages):
    try:
        print("🔹 Usando modelo Groq")
        response = completion(
            model=GROQ_MODEL,
            messages=messages,
            api_key=GROQ_API_KEY
        )
        content = response['choices'][0]['message']['content']
        return f"[Modelo usado: {GROQ_MODEL}]\n\n{content}"
    except Exception as e:
        print("⚠️ Erro com Groq, tentando OpenRouter:", e)
        traceback.print_exc()
        try:
            response = completion(
                model=OPENROUTER_MODEL,
                messages=messages,
                api_key=OPENROUTER_API_KEY
            )
            content = response['choices'][0]['message']['content']
            return f"[Modelo usado: {OPENROUTER_MODEL}]\n\n{content}"
        except Exception as e2:
            print("❌ Erro com OpenRouter também:", e2)
            traceback.print_exc()
            return "[Erro] Nenhum modelo pôde ser executado."
