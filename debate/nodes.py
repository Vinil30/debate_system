import time
from typing import Dict, Any

class UserInputNode:
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        input_func = state["input"]["input_func"]
        prompt = state["input"]["prompt"]
        topic = input_func(prompt)

        memory = state["memory"]
        memory.set_topic(topic)

        state.update({
            "topic": topic,
            "round": 0,
            "next_speaker": "Scientist",
            "memory": memory
        })
        return state

class AgentNode:
    def __init__(self, name: str, agent):
        self.name = name
        self.agent = agent

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        time.sleep(1.5)

        topic = state["memory"].get("topic")
        history = state["memory"].get_history()
        response = self.agent.respond(topic, history)

        memory = state["memory"]
        memory.add_argument(self.name, response)

        state.update({
            "last_speaker": self.name,
            "last_argument": response,
            "memory": memory
        })
        return state

class RoundControlNode:
    def __init__(self, max_rounds: int):
        self.max_rounds = max_rounds

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        current_round = state.get("round", 0)

        # Don't increment if we already marked done
        if state.get("done", False):
            return state

        # Advance round count
        current_round += 1

        # Determine if done AFTER all rounds
        done = current_round > self.max_rounds

        # Decide next speaker
        next_speaker = (
            "Philosopher" if state.get("last_speaker") == "Scientist" else "Scientist"
        )

        state.update({
            "round": current_round,
            "done": done,
            "next_speaker": next_speaker
        })

        return state

class JudgeNode:
    def __init__(self, judge):
        self.judge = judge

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("🧠 JudgeNode called!")  # ✅ Confirm judge runs
        topic = state["memory"].get("topic")
        history = state["memory"].get_history()

        result = self.judge.judge(topic, history)

        print("📢 Judge verdict returned:\n", result)  # ✅ See if anything comes back

        return {
            "judgment": result,
            "memory": state["memory"]
        }
