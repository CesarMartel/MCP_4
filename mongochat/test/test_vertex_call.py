from chat.graph import chat_graph, ChatState

state = ChatState(messages=[{"role": "user", "text": "Hola"}])
result = chat_graph.invoke(state)
print(result)
