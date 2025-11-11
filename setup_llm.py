from langchain_openai import ChatOpenAI

from config import settings

gpt_llm = ChatOpenAI(model="gpt-4.1", base_url='https://openrouter.ai/api/v1',
                     api_key=settings.OPENROUTER_API_KEY)

anthropic_llm = ChatOpenAI(
    model='anthropic/claude-haiku-4.5',
    api_key=settings.OPENROUTER_API_KEY,
    base_url='https://openrouter.ai/api/v1',
    temperature=0.7,
)

