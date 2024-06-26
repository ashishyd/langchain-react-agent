from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, render_text_description
from langchain_google_genai import GoogleGenerativeAI

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """
    Returns the length of a text by characters
    """
    print(f"get_text_length enter with {text=}")
    text = text.strip("`\n").strip('"')
    return len(text)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    print("React Langchain")
    tools = [get_text_length]
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), tool_names=", ".join([t.name for t in tools]))

    llm = GoogleGenerativeAI(temperature=0, model="gemini-pro", model_kwargs={"stop": ["\nObservation", "Observation"]})