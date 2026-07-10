# THIS IS TEAM - DIVISION
# highly optimised and integrated in order to conduct research, writing or surfing the web based on user reqs


import os
import json
from confluent_kafka import Consumer


from crewai import Agent, Task, Crew, Process
from crewai import LLM

from crewai_tools import TavilySearchTool
from dotenv import load_dotenv


load_dotenv()


# llm api keys (.env)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")



# LLM here will be acting as a brain of the DIVISION
llm = LLM(
    model="openrouter/openai/gpt-4o-mini",   # or another OpenRouter model
    api_key=OPENROUTER_API_KEY,
    max_tokens=1000,
)


# websearch tool -- TAVILY
web_search = TavilySearchTool(api_key=TAVILY_API_KEY)   #-- fetch from .env




# every agent will have their own backstory, role, goal, tasks, verbose

# researcher (with work with Tavily)
researcher = Agent(
    role="Senior Technology Researcher",
    goal="Always use Tavily for factual or current-event questions. Base your final answer ONLY on the search results. If the search contradicts your memory, trust the search.",
    backstory="""
        You are an expert researcher.
        
        Rules:
        - ALWAYS use the Tavily search tool for factual, recent, or real-world questions.
        - NEVER answer from memory if Tavily can answer.
        - Base your final answer ONLY on Tavily's results.
        - If the search results contradict your internal knowledge, trust the search.
        - Keep answers concise unless asked otherwise.
        """,
    tools=[web_search],
    verbose=True,
    llm=llm
)


# writer
writer = Agent(
    role="Tech Content Writer",
    goal="Create engaging blog posts about technology.",
    backstory="You are a skilled writer who transforms complex technical data into simple articles.",
    verbose=True,
    llm=llm
)


# kafka consumer for pager duty
config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "division-group",
    "auto.offset.reset": "latest"
}

consumer = Consumer(config)
consumer.subscribe(["system_data"])


print("Brain is active! waiting for messages")



# The Real-Time Processing Loop
while True:
    
        msg = consumer.poll(1.0)
    
        if msg is None:
            continue
    
        if msg.error():
            print(msg.error())
            continue
    
        data = json.loads(msg.value().decode("utf-8")).get("message")
    
        print(f"Got the fucking data from the user - {data}")
        print("🤖 Launching the DIVISION Agents for Battle ...")
    
    
    
        # research task
        researcher_task = Task(
            description=data,
            expected_output="A bulleted list with short summary.",
            agent=researcher
        )
        
        
        # writer task
        writer_task = Task(
            description="Using the insights provided by the researcher, write a short, compelling 2-paragraph blog post.",
            expected_output="A 2-paragraph blog post ready for publishing.",
            agent=writer
        )
        
        
        
        # tech crew
        tech_crew = Crew(
            agents=[researcher, writer],
            tasks=[researcher_task, writer_task],
            process=Process.sequential,
            verbose=True
        )
        
        
        
        
        print(" Divison is executing  -- (❁´◡`❁) ")
        result = tech_crew.kickoff()
        
        
        print("FINAL OUTPUT - ")
        print(result)