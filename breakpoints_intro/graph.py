from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import HumanMessage, SystemMessage

from setup_llm import gpt_llm


def multiply(a: int, b: int) -> int:
    """Умножить a и b.

    Аргументы:
        a: первое целое число
        b: второе целое число
    """
    return a * b


# Это будет инструментом
def add(a: int, b: int) -> int:
    """Сложить a и b.

    Аргументы:
        a: первое целое число
        b: второе целое число
    """
    return a + b


def divide(a: int, b: int) -> float:
    """Разделить a на b.

    Аргументы:
        a: первое целое число
        b: второе целое число
    """
    return a / b


tools = [add, multiply, divide]



llm_with_tools = gpt_llm.bind_tools(tools)

# Системное сообщение
sys_msg = SystemMessage(content="Ты полезный помощник, выполняющий арифметические операции над набором входных данных.")


# Узел
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}


# Построитель графа
builder = StateGraph(MessagesState)

# Определение узлов: они выполняют работу
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Определение ребер: они определяют поток управления
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # Если последнее сообщение (результат) от assistant - вызов инструмента -> tools_condition ведет к tools
    # Если последнее сообщение (результат) от assistant - не вызов инструмента -> tools_condition ведет к END
    tools_condition,
)
builder.add_edge("tools", "assistant")

memory = MemorySaver()
graph = builder.compile(interrupt_before=["tools"], checkpointer=memory)

# Входные данные
initial_input = {"messages": HumanMessage(content="Умножь 2 на 3")}

# Поток
thread = {"configurable": {"thread_id": "1"}}

# Запуск графа до первого прерывания
for event in graph.stream(initial_input, thread, stream_mode="values"):
    last_message = event['messages'][-1]
    print(f'[{type(last_message).__name__}]: ', last_message)

# Мы можем получить состояние и посмотреть на следующий узел для вызова.
# Это удобный способ увидеть, что граф был прерван.
state = graph.get_state(thread)
print(f'{state.next=}')
# 
# # Теперь введем удобный трюк. Когда мы вызываем граф с `None`, он просто продолжит выполнение с последней контрольной точки состояния!
# # Для ясности, LangGraph повторно выдаст текущее состояние, которое содержит `AIMessage` с вызовом инструмента.
# # Затем он продолжит выполнение следующих шагов в графе, начиная с узла инструмента.
# # Мы видим, что узел инструмента выполняется с этим вызовом инструмента, и он передается обратно в чат-модель для нашего окончательного ответа.
# for event in graph.stream(None, thread, stream_mode="values"):
#     last_message = event['messages'][-1]
#     print(f'[{type(last_message).__name__}]: ', last_message)
#
# # Теперь объединим это с конкретным шагом подтверждения пользователем, который принимает ввод пользователя.
# # Входные данные
# initial_input = {"messages": HumanMessage(content="Умножь 2 на 3")}
#
# # Поток
# thread = {"configurable": {"thread_id": "2"}}
#
# # Запуск графа до первого прерывания
# for event in graph.stream(initial_input, thread, stream_mode="values"):
#     last_message = event['messages'][-1]
#     print(f'[{type(last_message).__name__}]: ', last_message)
#
# # Получение подтверждения пользователя
# user_approval = input("Вы хотите вызвать инструмент? (да/нет): ")
#
# # Проверка подтверждения
# if user_approval.lower() == "да":
#     # Если подтверждено, продолжить выполнение графа
#     for event in graph.stream(None, thread, stream_mode="values"):
#         last_message = event['messages'][-1]
#         print(f'[{type(last_message).__name__}]: ', last_message)
# else:
#     print("Операция отменена пользователем.")
