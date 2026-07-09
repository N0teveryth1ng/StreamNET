# THIS IS TEAM - DIVISION
# highly optimised and integrated in order to conduct research, writing or surfing the web based on user reqs


import os
import json
from kafka import KafkaConsumer
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults





# LLM here will be acting as a brain of the DIVISION
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)  #-- fetch from .env

# websearch tool -- TAVILY
web_search = TavilySearchResults(api_key=".env")   #-- fetch from .env




# every agent will have their own backstory, role, goal, tasks, verbose

# researcher (with work with Tavily)
researcher = Agent(
    role="Senior Technology Researcher",
    goal="ncover cutting-edge developments in AI and technology.",
    backstory="You are an expert researcher with a knack for finding the latest tech trends.",
    tools=web_search,
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
consumer = KafkaConsumer(
    'market_trends', # <-- Make sure this matches your actual Kafka topic name!
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)



print("Brain is active! waiting for messages")



# The Real-Time Processing Loop
for message in consumer:
    
        data = message.value.get("message")
        print(f"Got the fucking data from the user - {data}  ")
        print("🤖 Launching the DIVISION Agents for Battle ...")

    
        # research task
        researcher_task = Task(
            description="Analyze the top 3 trends in Generative AI for 2026.",
            expected_output="A bulleted list of the top 3 trends with a short summary for each.",
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