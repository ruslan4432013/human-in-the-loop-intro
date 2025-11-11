from streaming_intro.graph_example import graph, initial_state

print("\n=== Режим: debug ===")
for chunk in graph.stream(initial_state, stream_mode="debug"):
    print(f"\n[DEBUG] Событие: {chunk['type']}")
    if chunk['type'] == 'task':
        print(f"  Задача: {chunk['payload']['name']}")
        print(f"  Payload: {chunk['payload']}")
    elif chunk['type'] == 'task_result':
        print(f"  Узел: {chunk['payload']['name']}")
        print(f"  Результат получен")