from langchain_google_vertexai import ChatVertexAI
import os

llm = ChatVertexAI(
    model_name="gemini-2.5-flash",
    location=os.getenv("VERTEX_LOCATION"),
    project=os.getenv("GOOGLE_PROJECT_ID")
)

response = llm.invoke("Hola, esto es una prueba de Vertex AI.")
print(response.content)
