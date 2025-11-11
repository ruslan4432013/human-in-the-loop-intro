from langgraph.types import StreamWriter

from streaming_intro.graph_example import State, graph, initial_state


# Модифицированный узел с custom streaming
def process_input_with_custom(state: State, writer: StreamWriter):
    """Обрабатывает входные данные и отправляет custom события"""
    writer("Начинаю обработку входных данных")
    writer({"step": "validation", "status": "success"})

    return {
        "messages": [("system", "Обрабатываю входные данные...")],
        "counter": 1
    }


# Использование
print("\n=== Режим: custom ===")
for chunk in graph.stream(initial_state, stream_mode="custom"):
    print(f"Custom событие: {chunk}")