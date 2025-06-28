from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import re
import time
class DebateJudge:
    def __init__(self, model: str = "llama3-70b-8192"):
        self.llm = ChatGroq(model_name=model, temperature=0.2)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert debate judge. Analyze the following debate 
             transcript and determine which participant made stronger arguments. Consider:
             1. Logical consistency
             2. Evidence and reasoning quality
             3. Rebuttal effectiveness
             4. Persuasiveness
             
             Debate Topic: {topic}
             
             Provide:
             1. A comprehensive summary of the key points
             2. Your verdict with the winner (must be either "Scientist" or "Philosopher")
             3. Detailed justification for your decision
             
             Format your response to clearly indicate the winner."""),
            ("human", "Debate Transcript:\n{transcript}"),
        ])

    def judge(self, topic: str, history: list) -> dict:
        # Convert history to transcript format
        transcript = "\n".join([f"{speaker}: {argument}" for speaker, argument in history])
        time.sleep(10)
        chain = self.prompt | self.llm
        response = chain.invoke({
            "topic": topic,
            "transcript": transcript
        })

        response_text = response.content

        winner = self._extract_winner_fallback(response_text)

        return {
            "summary": response_text,
            "winner": winner,
            "reasoning": response_text
        }

    def _extract_winner_fallback(self, text: str) -> str:
        text_lower = text.lower()

        # Try direct match
        match = re.search(r"winner:\s*(scientist|philosopher)", text_lower)
        if match:
            return match.group(1).capitalize()

        # Try fuzzy clues
        if "scientist wins" in text_lower or "victory for scientist" in text_lower:
            return "Scientist"
        if "philosopher wins" in text_lower or "victory for philosopher" in text_lower:
            return "Philosopher"

        # Fallback: most mentioned
        scientist_count = text_lower.count("scientist")
        philosopher_count = text_lower.count("philosopher")

        if scientist_count > philosopher_count:
            return "Scientist"
        elif philosopher_count > scientist_count:
            return "Philosopher"

        return "Draw"
