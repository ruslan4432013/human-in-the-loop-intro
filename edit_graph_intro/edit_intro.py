from langchain_core.messages import HumanMessage

from edit_graph_intro.react_graph import react_graph

# Входные данные
initial_input = {"messages": "Умножь 2 и 3"}

# Поток
thread = {"configurable": {"thread_id": "1"}}

# Запуск графа до первого прерывания
for event in react_graph.stream(initial_input, thread, stream_mode="values"):
    print(event['messages'][-1].pretty_print())

state = react_graph.get_state(thread)
print(state)

# Теперь мы можем напрямую применить обновление состояния. Помните, что обновления ключа `messages` будут использовать редьюсер `add_messages`:
# * Если мы хотим перезаписать существующее сообщение, мы можем указать `id` сообщения.
# * Если мы просто хотим добавить к нашему списку сообщений, то мы можем передать сообщение без указания `id`, как показано ниже.
react_graph.update_state(
    thread,
    {"messages": [HumanMessage(content="Нет, на самом деле умножь 3 и 3!")]},
)

# Посмотрим
# Мы вызвали `update_state` с новым сообщением. Редьюсер `add_messages` добавляет его к нашему ключу состояния `messages`.
print('NEW STATE:')
new_state = react_graph.get_state(thread).values
for m in new_state['messages']:
    print(m)
print('END NEW STATE')

# Теперь продолжим работу с нашим агентом, просто передав `None` и позволив ему продолжить с текущего состояния.
# Мы выдаем текущее состояние, а затем переходим к выполнению оставшихся узлов.
for event in react_graph.stream(None, thread, stream_mode="values"):
    print(event['messages'][-1].pretty_print())

# Теперь мы вернулись к `assistant`, у которого есть наша `точка останова`. Мы снова можем передать `None` для продолжения.
for event in react_graph.stream(None, thread, stream_mode="values"):
    print(event['messages'][-1].pretty_print())
