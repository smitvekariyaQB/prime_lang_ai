from agent.graph import workflow
import asyncio

async def test_graph():
    while True:
        human = input("Human: ")
        result = await workflow.ainvoke({"messages": human})
        data = result["messages"][-1]
        response_data = data.model_dump()
        print(f"Bot: {response_data['content']}\n")

try:
    asyncio.run(test_graph())
except KeyboardInterrupt:
    print("\nExited with Ctrl + C")
