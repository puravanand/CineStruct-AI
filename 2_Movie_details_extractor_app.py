from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

llm = ChatGroq( model="openai/gpt-oss-20b")  


query=input("Type Here:- ")

from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional


class Structure_data(BaseModel):
    Name:str=Field(description="Name of the Movie")
    cast: List[str]
    release_year: Optional[int]
    Director:str
    Actress:List[str]
    Total_cost:int
    Total_Earn:int
    Language:str
    genre:List[str]



prompts = ChatPromptTemplate.from_messages([
{"role":"system", "content":"You are the Novie  Extractor  Data Agent, you have to extract the Movie details  from the given input"},
{"role":"user","content":"{question}"}
])


final_promts=prompts.invoke({"question": query})
structure_llm= llm.with_structured_output(Structure_data)
res= structure_llm.invoke(final_promts)
print(res,"\n", res.model_dump_json(indent=2))

