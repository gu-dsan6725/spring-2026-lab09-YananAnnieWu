## Session Information

- The user_id is demo_user, which identifies the user interacting with the agent.
- The agent_id is memory-agent, which identifies the agent handling the conversation.
- The run_id is b15f177f, which represents the session ID for this conversation.

## Memory Types & Examples

- Factual Memory: Alice's name, Alice's job (software engineer), Alice uses Python
- Semantic Memory: Alice is working on a machine learning project using scikit-learn
- Preference Memory: Favorite language is Python, Prefers clean and maintainable code
- Episodic Memory: The earlier conversation where Alice mentioned working on an ML project

## Tool Usage Patterns

- insert_memory is used after important user information, e.g., Turn 1, 2, 4.
- Automatic Background Storage is used automatically at the same time.

## Memory Recall

Turn 3, 5, 7 trigger memory search since these turns ask about previously shared information. The log shows when the agent using the search_memory tool.

## Single Session

All turns happen in ONE session because they share the same run_id. And it's important as the agent can connect information across multiple turns.