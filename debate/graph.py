# debate/graph.py
from langgraph.graph import StateGraph
from typing import Dict, Any
from .nodes import UserInputNode, AgentNode, RoundControlNode, JudgeNode

class DebateGraph:
    def __init__(self, agent_a, agent_b, judge, max_rounds: int = 7):
        self.agent_a = agent_a
        self.agent_b = agent_b
        self.judge = judge
        self.max_rounds = max_rounds
        self.graph = StateGraph(state_schema=dict)
        self._build_graph()

    def _build_graph(self):
        user_input_node = UserInputNode()
        agent_a_node = AgentNode("Scientist", self.agent_a)
        agent_b_node = AgentNode("Philosopher", self.agent_b)
        round_control_node = RoundControlNode(self.max_rounds)
        judge_node = JudgeNode(self.judge)

        self.graph.add_node("user_input", user_input_node)
        self.graph.add_node("agent_a", agent_a_node)
        self.graph.add_node("agent_b", agent_b_node)
        self.graph.add_node("round_control", round_control_node)
        self.graph.add_node("judge", judge_node)

        self.graph.set_entry_point("user_input")
        self.graph.add_edge("user_input", "round_control")

        def route_next_speaker(state: Dict[str, Any]):
            if state.get("done", False):
                return "judge"
            return "agent_a" if state.get("next_speaker") == "Scientist" else "agent_b"

        self.graph.add_conditional_edges(
            "round_control",
            route_next_speaker,
            {
                "agent_a": "agent_a",
                "agent_b": "agent_b",
                "judge": "judge"
            }
        )

        self.graph.add_edge("agent_a", "round_control")
        self.graph.add_edge("agent_b", "round_control")

        # ❗️Add this line to define when the graph ends
        self.graph.set_finish_point("judge")
# This ends the graph correctly


    def compile(self):
        return self.graph.compile()

    def visualize(self, filename="debate_dag"):
        try:
            print("Graph visualization skipped (avoiding LangGraph state conflict)")
            return
        except Exception as e:
            print(f"Error generating visualization: {e}")
