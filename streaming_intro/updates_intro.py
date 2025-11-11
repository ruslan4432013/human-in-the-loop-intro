from streaming_intro.graph_example import graph, initial_state

print("\n=== Режим: updates ===")
for chunk in graph.stream(initial_state, stream_mode="updates"):
    print(f"\nОбновление от узла:")
    for node_name, node_update in chunk.items():
        print(f"  Узел '{node_name}':")
        if "counter" in node_update:
            print(f"    Добавлено к счётчику: {node_update['counter']}")
        if "messages" in node_update:
            print(f"    Добавлено сообщений: {len(node_update['messages'])}")
        if "result" in node_update:
            print(f"    Результат: {node_update['result']}")