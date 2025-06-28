from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

class DebateAgent:
    def __init__(self, name: str, role: str, model: str = "llama3-8b-8192"):
        self.name = name
        self.role = role
        self.llm = ChatGroq(model_name=model, temperature=0.7)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are {name}, {role}. You are participating in a structured debate.
             
             Your role: {role}
             
             Instructions:
             - Present clear, well-reasoned arguments
             - Respond to previous arguments when relevant
             - Stay focused on the debate topic
             - Use your expertise as {role}
             - Keep responses concise but substantive (2-3 paragraphs max)
             - Be respectful but assertive in your position
             
             Topic: {{topic}}
             """),
            ("human", "Previous arguments:\n{history}\n\nYour response:"),
        ])
    
    def respond(self, topic: str, history: list) -> str:
        # Format history for the prompt
        history_text = "\n".join([f"{speaker}: {argument}" for speaker, argument in history]) if history else "No previous arguments."
        
        chain = self.prompt | self.llm
        response = chain.invoke({
            "topic": topic,
            "history": history_text
        })
        
        return response.content