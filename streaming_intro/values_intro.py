from streaming_intro.graph_example import graph, initial_state

print("=== Режим: values ===")
for chunk in graph.stream(initial_state, stream_mode="values"):
    print(f"\nШаг выполнен:")
    print(f"  Счётчик: {chunk.get('counter', 0)}")
    print(f"  Сообщений: {len(chunk.get('messages', []))}")
    print(f"  Результат: {chunk.get('result', 'Нет')}")