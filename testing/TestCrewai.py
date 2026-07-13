# from crewai import Agent
# from dotenv import load_dotenv
# import os
# from crewai import LLM


# load_dotenv()

# llm = LLM(
#     model="gpt-4o-mini",
#     api_key=os.getenv("OPENAI_API_KEY")
# )

# agent = Agent(
#     role="Researcher",
#     goal="Answer questions",
#     backstory="You are an AI researcher.",
#     llm=llm
# )

# print(agent)



from dotenv import load_dotenv
import os

load_dotenv()

# print("Loaded:", load_dotenv())
# print(os.getcwd())
# print(os.path.exists(".env"))



print("GOOGLE:", os.getenv("GOOGLE_API_KEY"))
print("GEMINI:", os.getenv("GEMINI_API_KEY"))
print("TAVILY:", os.getenv("TAVILY_API_KEY"))