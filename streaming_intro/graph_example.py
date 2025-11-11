from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import operator

from setup_llm import gpt_llm


# Определяем состояние графа
class State(TypedDict):
    messages: Annotated[list, add_messages]
    counter: Annotated[int, operator.add]
    result: str

# Инициализируем LLM


# Узел 1: Обработка входного сообщения
def process_input(state: State):
    """Обрабатывает входное сообщение и увеличивает счётчик"""
    return {
        "messages": [("system", "Обрабатываю входные данные...")],
        "counter": 1
    }

# Узел 2: Вызов LLM
def call_llm(state: State):
    """Вызывает LLM для генерации ответа"""
    response = gpt_llm.invoke(state["messages"])
    return {
        "messages": [response],
        "counter": 1
    }

# Узел 3: Финальная обработка
def finalize(state: State):
    """Финализирует результат"""
    return {
        "result": f"Обработка завершена за {state['counter']} шагов",
        "counter": 1
    }

# Создаём граф
workflow = StateGraph(State)

# Добавляем узлы
workflow.add_node("process", process_input)
workflow.add_node("llm", call_llm)
workflow.add_node("finalize", finalize)

# Определяем рёбра
workflow.add_edge(START, "process")
workflow.add_edge("process", "llm")
workflow.add_edge("llm", "finalize")
workflow.add_edge("finalize", END)

# Компилируем граф
graph = workflow.compile()

# Начальное состояние
initial_state = {
    "messages": [("user", "Привет! Расскажи про LangGraph")],
    "counter": 0,
    "result": ""
}