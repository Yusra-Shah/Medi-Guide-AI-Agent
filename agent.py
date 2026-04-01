import os
import logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

load_dotenv()
model_name = os.getenv("MODEL")

wikipedia_tool = LangchainTool(
    tool=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
)

def save_symptoms_to_state(
    tool_context: ToolContext, symptoms: str
) -> dict[str, str]:
    """Saves the user's symptoms to state."""
    tool_context.state["SYMPTOMS"] = symptoms
    return {"status": "success"}

symptom_researcher = Agent(
    name="symptom_researcher",
    model=model_name,
    description="Researches medical conditions based on symptoms.",
    instruction="""
    You are a medical research assistant. 
    Research the symptoms provided in SYMPTOMS using Wikipedia.
    Find possible conditions, causes, and general information.
    
    SYMPTOMS:
    { SYMPTOMS }
    """,
    tools=[wikipedia_tool],
    output_key="research_data"
)

medical_advisor = Agent(
    name="medical_advisor",
    model=model_name,
    description="Provides friendly medical guidance based on research.",
    instruction="""
    You are a friendly medical information assistant.
    Based on RESEARCH_DATA, provide:
    1. Possible conditions related to the symptoms
    2. General information about each condition
    3. Always remind the user to consult a real doctor
    4. Be compassionate and clear
    
    RESEARCH_DATA:
    { research_data }
    """
)

medi_workflow = SequentialAgent(
    name="medi_workflow",
    description="Research symptoms then provide medical guidance.",
    sub_agents=[symptom_researcher, medical_advisor]
)

root_agent = Agent(
    name="medi_greeter",
    model=model_name,
    description="MediGuide AI - Personal Medical Information Assistant",
    instruction="""
    Greet the user warmly as MediGuide AI assistant.
    Ask them to describe their symptoms.
    When they respond, use save_symptoms_to_state tool to save their symptoms.
    Then transfer to medi_workflow.
    Always remind users you are not a substitute for professional medical advice.
    """,
    tools=[save_symptoms_to_state],
    sub_agents=[medi_workflow]
)