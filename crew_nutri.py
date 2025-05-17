import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import streamlit as st
from llm_custom import custom_llm_completion
from textwrap import dedent

#from MyLLM import MyLLM
from MyLLM import CustomLLM

#from groq import Groq

# Carregar variáveis de ambiente
#load_dotenv()

# Obter a chave da API GROQ
#GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Crie uma função de fallback
llama = CustomLLM()  # isso é um callable, mas vamos transformar em função wrapper

class CrewNutri:
    def __init__(self):
        self.crew = self._criar_crew()

    def _criar_crew(self):
        # Definindo os agentes
        nutri = Agent(
         role="Nutricionista",
         goal="Identificar se alimentos na descrição  são saudáveis ou não. Sempre considere as oabservações feitas pelo usuário em sua análise.",
         allow_delegation=False,
         tools=[], 
         llm={"type": "custom", "completion_function": custom_llm_completion},
         verbose=True,
         backstory=dedent("""
              Você é um especialista em nutrição com experiência em identificar comidas saudáveis ou não.
              Ao  analisar a descrição de alimentos considere as observações informadas pelo usuário e recomende alimentos mais saudáveis e mais adequados.
              A análise deve ser respondida em Portugues."""
     )
     )


        # Tarefas
        analise = Task(
        name='analise_imagem',
        description= dedent("""
        Análise os alimentos na descrição: {descricao}.
        Sempre responder em Portugues.
        Considere as seguintes observações ao realizar sua análise: {observacoes}.
        Informar cada observação feita pelo usuário e anlisar se é adequadio ou não o consumo.
        """),
        expected_output=dedent(
        """
             Texto claro e resumido, no maximo 1000 tokens.
             Informar as observações feitas pelo usuário.
             Nomes dos alimentos em Portugues.
             Considerar as oabservações nos resultados da análise.             
             Um relatório em Portugues detalhado com:            
             1 - Alimentos identificados na descrição;
             2 - Identificar as vitaminas presentes em cada alimento;
             3 - Informar se alimento é saudável ou não;
             4-  Informar as calorias de cada alimento;
             5 - Informar qual beneficio o alimento oferece para a saúde;
             6 - Informar alternativa mais saudável para trocar pelo alimento.
             7 - Um resumo final informando se o conjunto de alimentos descritos na imagem esta adequado as observações informadas.
             
             Exemplo a ser seguido:
 Na imagem, foram identificados os seguintes alimentos:

** Salmão (Sashimi):**
     * ** Macronutrientes (por 100g):** Aproximadamente 20g de proteína, 0g de carboidratos, 10g de gordura (muita dos quais são omega-3).
     * ** Vitaminas:** Excelente fonte de vitamina B12, vitamina D e selenio.
     * ** Calorias:** Aproximadamente 180 kcal.
     * ** Benefícios:** Ajuda a reduzir o risco de doenças cardíacas e pode ajudar a promover a saúde do cérebro.
     * ** Nível de Processamento:** In natura.
     * ** Observação:** Considerando a observação do usuário sobre manter o peso, o salmon é uma ótima escolha devido ao seu conteúdo de proteína magra e gorduras saudáveis.
* **Wasabi (Vegetal):**
    * ** Macronutrientes (por 100g):** Baixo teor de carboidratos e proteínas, mas contém muita água. O teor de gordura é zero.
    * ** Vitaminas:** Excelente fonte de vitamina C e uma boa fonte de vitamina K.
    * ** Calorias:** Aproximadamente 10 kcal.
    * ** Benefícios:** Tem propriedades anti-inflamatórias e pode ajudar a aliviar problemas respiratórios.
    * ** Nível de Processamento:** In natura.
    * ** Observação:** Considerando a observação do usuário sobre reduzir peso, o wasabi em pequenas quantidades pode ajudar a aumentar a perda de peso graças a sua capacidade de aliviar a fome.
* **Arroz Branco para o Sushi:**
    * ** Macronutrientes (por 1 xícara cozida):** Aproximadamente 45g de carboidratos (boa parte simples).
    * ** Vitaminas:** Ricos em vitamina B1, B3, B6 e umidade.
    * ** Calorias:** Aproximadamente 200 kcal.
    * ** Benefícios:** Fornece energia rápida e pode ajudar a controlar a fome.
    * ** Nível de Processamento:** Processado.
    * ** Alternativa Mais Saudável:** Considerando a qualidade recomendada de carboidrato simples (ou açúcar), o uso de arroz branco na dieta deve ser minimizado.

A tabela abaixo resume as observações feitas pelo usuário e como elas se aplicam ao conjunto de alimentos descritos.

| Observações do Usuário | Aplicação Nas Observações |
| --- | --- |
| Manter o peso | O salmÃO é uma ótima escolha devido ao seu conteúdo de proteína magra e gorduras saudáveis. |
| Alergia a amendoim | Nenhum alimento encontrado na descrição refere, directamente, nutrimentos, do amendoim. O Sushi pode ser uma opção |
| Emagrecer | O salmão nas quantidade de porto sugeridas aumenta o seu metabolismo. O wasabi também pode ajudá-lo, visto que o wasabi usa água.     |

Resumo Final:

Considerando as observações feitas pelo usuário, o conjunto de alimentos descritos na imagem têm quase exclusivamente alimentos saudáveis e 
adequados à sua escolha de dieta. Embora o arroz branco para sushi seja um carboidrato simples, ele faz parte de um prato saudável e pode ser 
consumido em moderação com base nas necessidades individuais e das atividades diárias. 
Em contrapartida, o salmÃO e o wasabi têm qualidade nutricional significativas para o corpo humano na dieta.   
 """),
        
        agent=nutri
    )    

        # Criando o Crew
        return Crew(
            agents=[nutri],
            tasks=[analise],
            process=Process.sequential,
            llm=CustomLLM()  # 👈 aqui também funciona
        )

    def kickoff(self, inputs):
        # Executa o Crew com o tópico fornecido
        resposta = self.crew.kickoff(inputs=inputs)
        return resposta.raw
