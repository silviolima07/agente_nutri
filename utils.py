import base64
import streamlit as st



# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8') 

#def image_to_text(client, model, b64_image, prompt, idioma):	
def image_to_text(client, model, b64_image, prompt):
    result = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                {'type': 'text', 'text': prompt},
                {
                  'type': 'image_url',
                  'image_url': {
                                 'url':f"data:image/jpeg;base64,{b64_image}",
                    }, 
                },
              ], 
            }    
        ], 
        model=model,
        temperature=0.5,  # Controla a criatividade
        top_p=0.9,  # Controla a diversidade das respostas
   )      
  
    return result.choices[0].message.content



# Função para executar a crew
def executar_crew(crew, inputs):
    try:
        result = crew.kickoff(inputs=inputs)  # Inicia a execução da crew
        #st.write("Result from analyse of description")
        #st.write(result)
      
        return result  # Obtém a saída após a execução
    except Exception as e:
        st.error(f"Ocorreu um erro ao executar a crew: {e}")


	