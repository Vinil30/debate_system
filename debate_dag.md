---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	user_input(user_input)
	agent_a(agent_a)
	agent_b(agent_b)
	round_control(round_control)
	judge(judge)
	__end__([<p>__end__</p>]):::last
	__start__ --> user_input;
	agent_a --> round_control;
	agent_b --> round_control;
	round_control -.-> agent_a;
	round_control -.-> agent_b;
	round_control -.-> judge;
	user_input --> round_control;
	judge --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
