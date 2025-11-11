from streaming_intro.graph_example import graph, initial_state

print("\n=== Режим: messages ===")
for chunk in graph.stream(initial_state, stream_mode="messages"):
    token, metadata = chunk
    print(f"{token.content}", end="", flush=True)