import os
from gpt_assistant.home_assistant.langchain_tool import HomeAssistantProcessor
from typing import List

import openai
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI

llm = None
tools = None


def init_agent():
    global llm
    global tools

    openai.api_key = os.environ["OPENAI_API_KEY"]
    ha_processor = HomeAssistantProcessor()
    llm = OpenAI(temperature=0)
    tools = [
        Tool(
            name="Discover home devices",
            func=ha_processor.discover,
            description="useful for when you need to discover all devices in your home, this tool takes no input. The response will be a list of all devices in your home in JSON format, with fields 'entity_id' representing the device ID, 'state' representing the device status, 'friendly_name' representing the name of the device, 'device_class' representing the kind of the device.",
        ),
        Tool(
            name="Get device state",
            func=ha_processor.read,
            description="Use this tool only when you need to get the current state of specific switch or device returned from discover. Run discover before this tool. This tool accepts 3 arguments, the \"entity_id\" of the device, \"device_class\" of device and \"friendly_name\" of device in lowercase string. For example, [\"scene.tv\", \"scene\", \"TV\"] would be the input if you wanted to turn on the TV, the output will be a simple string of the \"state\" of the device.",
        ),
        Tool(
            name="Get sensor read",
            func=ha_processor.read_sensor,
            description="Use this tool only when you need to get the current value of specific sensor. This tool takes 3 arguments, the \"entity_id\" of the device, \"device_class\" of device and \"friendly_name\" of device in lowercase string. For example, [\"sensor.living_room_temperature\", \"sensor\", \"temperature\"] would be the input if you wanted to get the temperature, the output will be a simple string of the \"state\" of the sensor.",
        ),
        Tool(
            name="Toggle discovered light or switch",
            func=ha_processor.run,
            description="Use this tool only when you have discovered a device and need to toggle a specific light or switch returned from discover. You cannot run toggle device before discover home devices. This tool accepts 4 arguments from discover, the \"entity_id\" of the device, \"device_class\" of device, desired status and \"friendly_name\" of device in lowercase string. For example, [\"scene.tv\", \"scene\", \"on\", \"TV\"] would be the input if you wanted to turn on the TV.",
        ),
        Tool(
            name="Reset context",
            func=lambda string: "Reached a final stage, do not proceed to other action, give final answer now. Giving \"RESET_CONTEXT\" as final answer.",
            description="Use this tool only when you are requested to reset the context",
        ),
        Tool(
            name="Default",
            func=lambda string: "Reached a final stage, do not proceed to other action, give final answer now. Giving \"DEFAULT_ACTION\" as final answer.",
            description="use in general",
        ),
    ]


def execute_agent(prompt: str):
    print("\rExecuting agent with prompt: ", prompt)
    global llm
    global tools

    if llm is None or tools is None:
        init_agent()

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    return agent.run(prompt)
