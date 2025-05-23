from crewai import LLM

class MyLLM():
    GPT4o_mini    = LLM(model='gpt-4o-mini')
    GPT4o_mini_2024_07_18    = LLM(model='gpt-4o-mini-2024-07-18')
    GPT4o    = LLM(model='gpt-4o')
    GPT_o1    = LLM(model='01-preview')
    GPT3_5    = LLM(model='gpt-3.5-turbo')
    LLAMA3_70B    = LLM(model='llama3-70b-8192')
    GROQ_LLAMA    = LLM(model='groq/llama-3.1-8b-instant')
    GROQ_DEEPSEEK    = LLM(model='"groq/deepseek-r1-distill-llama-70b')
    GROQ_LLAMA_MM    = LLM(model='groq/llama-4-scout-17b-16e-instruct')
