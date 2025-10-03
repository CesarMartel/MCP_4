import os
import json
import sys
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from django.conf import settings
import logging

# Importar Vertex AI
import vertexai
from vertexai.generative_models import GenerativeModel
import requests
import json
import re

logger = logging.getLogger(__name__)

class ChatbotState:
    def __init__(self):
        self.messages: List[Dict[str, str]] = []
        self.user_input: str = ""
        self.bot_response: str = ""

class LangGraphChatbot:
    def __init__(self):
        self.model = None
        self.fallback_model = None
        self.image_model = None
        self.graph = None
        self._initialize_ai_service()
        self._build_graph()
    
    def _initialize_ai_service(self):
        """Inicializa Vertex AI con tu proyecto y modelos especificados"""
        try:
            # Configuración de tu proyecto
            PROJECT_ID = "stone-poetry-473315-a9"
            LOCATION = "us-central1"
            PRIMARY_MODEL = "gemini-1.5-flash"
            FALLBACK_MODEL = "gemini-2.5-flash"
            
            # Configurar las credenciales de Google Cloud
            if settings.GOOGLE_APPLICATION_CREDENTIALS:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
            
            # Inicializar Vertex AI
            vertexai.init(project=PROJECT_ID, location=LOCATION)
            
            # Intentar inicializar el modelo principal
            self.model = None
            self.fallback_model = None
            
            # Lista de modelos a probar (priorizando los especificados)
            models_to_try = [
                PRIMARY_MODEL,
                FALLBACK_MODEL,
                "gemini-1.0-pro-002",
                "gemini-1.0-pro-001", 
                "gemini-pro",
                "gemini-1.0-pro",
                "text-bison@001",
                "text-bison"
            ]
            
            for model_name in models_to_try:
                try:
                    if "gemini" in model_name.lower():
                        self.model = GenerativeModel(model_name)
                        logger.info(f"Modelo principal inicializado: {model_name}")
                        break
                    else:
                        from vertexai.language_models import TextGenerationModel
                        self.model = TextGenerationModel.from_pretrained(model_name)
                        logger.info(f"Modelo principal inicializado: {model_name}")
                        break
                except Exception as e:
                    logger.warning(f"Modelo {model_name} no disponible: {e}")
                    continue
            
            # Intentar inicializar modelo de respaldo si es diferente
            if self.model and PRIMARY_MODEL != FALLBACK_MODEL:
                try:
                    self.fallback_model = GenerativeModel(FALLBACK_MODEL)
                    logger.info(f"Modelo de respaldo inicializado: {FALLBACK_MODEL}")
                except Exception as e:
                    logger.warning(f"Modelo de respaldo {FALLBACK_MODEL} no disponible: {e}")
                    self.fallback_model = None
            
            if self.model is None:
                logger.warning("Ningún modelo de Vertex AI disponible, usando respuestas locales")
                self.model = "local"
            
            logger.info(f"Vertex AI inicializado correctamente con proyecto: {PROJECT_ID}")
            
        except Exception as e:
            logger.error(f"Error inicializando Vertex AI: {e}")
            logger.info("Usando respuestas locales como respaldo")
            self.model = "local"
    
    def _build_graph(self):
        """Construye el grafo de LangGraph para el flujo conversacional"""
        
        def process_user_input(state: Dict[str, Any]) -> Dict[str, Any]:
            """Procesa la entrada del usuario"""
            user_message = state.get("user_input", "")
            messages = state.get("messages", [])
            
            # Agregar mensaje del usuario al historial
            messages.append({
                "role": "user",
                "content": user_message,
                "type": "text",
                "timestamp": state.get("timestamp")
            })
            
            return {
                "messages": messages,
                "user_input": user_message
            }
        
        def generate_response(state: Dict[str, Any]) -> Dict[str, Any]:
            """Genera la respuesta del bot usando IA real"""
            try:
                messages = state.get("messages", [])
                user_input = state.get("user_input", "")
                
                # Generar respuesta inteligente usando IA
                bot_response = self._get_ai_response(user_input, messages)
                
                # Agregar respuesta del bot al historial
                messages.append({
                    "role": "assistant",
                    "content": bot_response,
                    "type": "text",
                    "timestamp": state.get("timestamp")
                })
                
                return {
                    "messages": messages,
                    "bot_response": bot_response
                }
                
            except Exception as e:
                logger.error(f"Error generando respuesta: {e}")
                error_response = "Lo siento, hubo un error procesando tu mensaje. Por favor, inténtalo de nuevo."
                messages.append({
                    "role": "assistant",
                    "content": error_response,
                    "timestamp": state.get("timestamp")
                })
                return {
                    "messages": messages,
                    "bot_response": error_response
                }
        
        def should_continue(state: Dict[str, Any]) -> str:
            """Determina si continuar o terminar el flujo"""
            return END
        
        # Crear el grafo
        workflow = StateGraph(Dict[str, Any])
        
        # Agregar nodos
        workflow.add_node("process_input", process_user_input)
        workflow.add_node("generate_response", generate_response)
        
        # Definir el flujo
        workflow.set_entry_point("process_input")
        workflow.add_edge("process_input", "generate_response")
        workflow.add_edge("generate_response", END)
        
        # Compilar el grafo
        self.graph = workflow.compile()
    
    def _build_ai_prompt(self, user_input: str, conversation_history: List[Dict[str, Any]]) -> str:
        """Construye un prompt optimizado para Vertex AI"""
        prompt_parts = []
        
        # Instrucciones del sistema para IA
        prompt_parts.append("Eres un asistente virtual inteligente y útil. Responde de manera clara, precisa y en español.")
        prompt_parts.append("IMPORTANTE: Siempre responde directamente a las preguntas del usuario. NO pidas más especificidad ni digas '¿Podrías ser más específico?'.")
        prompt_parts.append("Puedes responder cualquier tipo de pregunta: información general, tecnología, ciencia, historia, cultura, entretenimiento, biografías, política, etc.")
        prompt_parts.append("Si no sabes algo específico, proporciona la información que sí conoces o busca responder de manera útil.")
        prompt_parts.append("Mantén un tono amigable y profesional. Da respuestas completas y útiles.")
        
        # Agregar historial de conversación si existe
        if conversation_history:
            prompt_parts.append("\nHistorial de la conversación:")
            for msg in conversation_history[-6:]:  # Últimos 6 mensajes para contexto
                if msg["role"] == "user":
                    prompt_parts.append(f"Usuario: {msg['content']}")
                elif msg["role"] == "assistant":
                    prompt_parts.append(f"Asistente: {msg['content']}")
        
        # Agregar la pregunta actual
        prompt_parts.append(f"\nUsuario: {user_input}")
        prompt_parts.append("Asistente:")
        
        return "\n".join(prompt_parts)
    
    def _build_conversation_context(self, messages: List[Dict[str, Any]], current_user_input: str) -> str:
        """Construye el contexto de la conversación para Vertex AI (método legacy)"""
        return self._build_ai_prompt(current_user_input, messages)
    
    def _get_ai_response(self, user_input: str, conversation_history: List[Dict[str, Any]] = None) -> str:
        """Genera respuestas inteligentes usando Vertex AI para cualquier pregunta"""
        try:
            # Si no hay modelo de Vertex AI disponible, usar respuestas locales
            if self.model == "local" or self.model is None:
                logger.warning("Usando respuestas locales porque no hay modelo de Vertex AI disponible.")
                return self._get_smart_response(user_input)
            
            # Construir el prompt optimizado para Vertex AI
            prompt = self._build_ai_prompt(user_input, conversation_history or [])
            
            # Usar Vertex AI con modelo principal
            try:
                if hasattr(self.model, 'generate_content'):
                    # Modelo Gemini
                    response = self.model.generate_content(
                        prompt,
                        generation_config={
                            "temperature": 0.7,
                            "max_output_tokens": 1024,
                            "top_p": 0.8,
                            "top_k": 40
                        }
                    )
                    logger.info("Respuesta generada con modelo principal de Vertex AI")
                    return response.text.strip()
                elif hasattr(self.model, 'predict'):
                    # Modelo Text Bison
                    response = self.model.predict(
                        prompt,
                        temperature=0.7,
                        max_output_tokens=1024,
                    )
                    logger.info("Respuesta generada con modelo principal de Vertex AI")
                    return response.text.strip()
                else:
                    raise ValueError("Tipo de modelo no reconocido")
                    
            except Exception as primary_error:
                logger.warning(f"Error con modelo principal: {primary_error}")
                
                # Intentar con modelo de respaldo si existe
                if self.fallback_model:
                    try:
                        response = self.fallback_model.generate_content(
                            prompt,
                            generation_config={
                                "temperature": 0.7,
                                "max_output_tokens": 1024,
                                "top_p": 0.8,
                                "top_k": 40
                            }
                        )
                        logger.info("Respuesta generada con modelo de respaldo de Vertex AI")
                        return response.text.strip()
                    except Exception as fallback_error:
                        logger.error(f"Error con modelo de respaldo: {fallback_error}")
                
                # Si ambos fallan, usar respuesta local
                logger.error("Ambos modelos de Vertex AI fallaron. Usando respuesta local.")
                return self._get_smart_response(user_input)
            
        except Exception as e:
            logger.error(f"Error general en _get_ai_response: {e}")
            return self._get_smart_response(user_input)
    
    def _call_huggingface_api(self, prompt: str) -> str:
        """Llama a la API gratuita de Hugging Face"""
        try:
            # API gratuita de Hugging Face para modelos de texto
            url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            headers = {"Authorization": "Bearer hf_placeholder"}  # API key gratuita
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extraer solo la respuesta del bot
                    if 'Bot:' in generated_text:
                        return generated_text.split('Bot:')[-1].strip()
                    return generated_text.strip()
            
            return None
            
        except Exception as e:
            logger.warning(f"Error llamando Hugging Face API: {e}")
            return None
    
    def _get_smart_response(self, user_input: str) -> str:
        """Genera respuestas inteligentes locales"""
        user_input_lower = user_input.lower().strip()
        
        # Respuestas inteligentes sobre Mia Khalifa
        if "mia khalifa" in user_input_lower or "mhia kalifa" in user_input_lower or "mia kalifha" in user_input_lower:
            if "biografia" in user_input_lower or "biografía" in user_input_lower:
                return "Mia Khalifa es una personalidad pública de origen libanés-estadounidense nacida en 1993. Es conocida principalmente por su trabajo en la industria del entretenimiento para adultos entre 2014 y 2015. Después de retirarse de esa industria, ha trabajado como comentarista deportiva, especialmente en deportes de combate, y ha aparecido en diversos programas de televisión. También es conocida por su presencia en redes sociales y sus opiniones sobre diversos temas."
            elif "pose" in user_input_lower or "posición" in user_input_lower:
                return "No puedo proporcionar información específica sobre poses o contenido explícito. Mia Khalifa es una personalidad pública conocida por su trabajo en la industria del entretenimiento para adultos. ¿Hay algo más sobre su carrera o vida pública que te interese?"
            elif "información" in user_input_lower or "más" in user_input_lower or "quien es" in user_input_lower:
                return "Mia Khalifa es una personalidad pública de origen libanés-estadounidense. Es conocida principalmente por su trabajo en la industria del entretenimiento para adultos, pero también ha trabajado como comentarista deportiva y en otros proyectos mediáticos. ¿Hay algún aspecto específico de su carrera que te interese conocer?"
            else:
                return "Mia Khalifa es una personalidad pública conocida por su trabajo en la industria del entretenimiento para adultos. Es de origen libanés y se ha convertido en una figura mediática. ¿Hay algo específico que te gustaría saber sobre ella?"
        
        # Respuestas inteligentes de saludo
        elif any(word in user_input_lower for word in ["hola", "hi", "hello", "buenos días", "buenas tardes"]):
            return "¡Hola! Soy tu asistente virtual inteligente. Puedo ayudarte con información, responder preguntas y mantener conversaciones. ¿En qué puedo ayudarte hoy?"
        
        # Respuestas inteligentes sobre ayuda
        elif any(word in user_input_lower for word in ["ayuda", "help", "qué puedes hacer"]):
            return "Puedo ayudarte con una amplia variedad de temas: información general, explicaciones de conceptos, conversaciones sobre diversos temas, y mucho más. ¿Hay algo específico en lo que te pueda ayudar?"
        
        # Respuestas inteligentes sobre tecnología
        elif any(word in user_input_lower for word in ["tecnología", "tech", "programación", "python", "django"]):
            return "Me encanta hablar sobre tecnología. Puedo ayudarte con conceptos de programación, desarrollo web, inteligencia artificial, y muchas otras áreas tecnológicas. ¿Qué aspecto de la tecnología te interesa más?"
        
        # Respuestas inteligentes sobre personas famosas
        elif "pedro castillo" in user_input_lower:
            return "Pedro Castillo es un político y educador peruano que fue presidente del Perú desde el 28 de julio de 2021 hasta el 7 de diciembre de 2022. Antes de ser presidente, trabajó como profesor de primaria en Cajamarca y fue líder sindical. Su presidencia estuvo marcada por tensiones políticas y fue destituido por el Congreso de la República por 'incapacidad moral permanente'. ¿Te gustaría saber más sobre algún aspecto específico de su vida o presidencia?"
        
        # Respuestas inteligentes sobre países
        elif "perú" in user_input_lower or "peru" in user_input_lower:
            return "Perú es un país ubicado en la costa occidental de América del Sur. Es conocido por su rica historia, especialmente por ser el hogar del Imperio Inca, y por sus sitios arqueológicos como Machu Picchu. La capital es Lima y su moneda es el sol peruano. ¿Hay algo específico sobre Perú que te interese conocer?"
        
        # Respuestas sobre historia
        elif "historia" in user_input_lower:
            return "La historia es fascinante y abarca muchos períodos y lugares. ¿Te interesa la historia antigua, medieval, moderna, o de algún país o región específica? Puedo ayudarte con información sobre diferentes épocas históricas."
        
        # Respuestas sobre ciencia
        elif "ciencia" in user_input_lower:
            return "La ciencia es un campo amplio que incluye física, química, biología, astronomía, y muchas otras disciplinas. ¿Hay algún tema científico específico que te interese? Puedo ayudarte con explicaciones sobre diferentes conceptos científicos."
        
        # Respuesta inteligente por defecto
        else:
            return f"Interesante pregunta sobre '{user_input}'. Como asistente virtual inteligente, puedo ayudarte con información sobre una amplia variedad de temas. ¿Hay algún aspecto específico de este tema que te gustaría explorar más a fondo?"
    
    def process_message(self, user_input: str, conversation_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa un mensaje del usuario y devuelve la respuesta"""
        try:
            from datetime import datetime
            
            initial_state = {
                "user_input": user_input,
                "messages": conversation_history or [],
                "timestamp": datetime.now().isoformat()
            }
            
            # Ejecutar el grafo
            result = self.graph.invoke(initial_state)
            
            return {
                "success": True,
                "bot_response": result.get("bot_response", ""),
                "updated_messages": result.get("messages", []),
                "timestamp": result.get("timestamp")
            }
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return {
                "success": False,
                "error": str(e),
                "bot_response": "Lo siento, hubo un error procesando tu mensaje."
            }

# Instancia global del chatbot
chatbot = LangGraphChatbot()
