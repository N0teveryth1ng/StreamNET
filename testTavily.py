from dotenv import load_dotenv
import os
from langchain_tavily import TavilySearch

load_dotenv()

search = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))

result = search.invoke("Latest AI agent frameworks")
print(result)