from langchain_community.llms import OpenAI
from langchain_core.tools import BaseTool
from LLM.ChatBot.WeatherAgent.GetWeather import GetWeather
from langchain_openai import ChatOpenAI  # Updated import
from langchain_core.utils.function_calling import convert_to_openai_function  # Updated import
from pydantic import BaseModel, Field
from typing import Optional, Type
from langchain.schema import HumanMessage, AIMessage, FunctionMessage
import json
import os


def get_current_weather(location, unit):
    get_weather_obj = GetWeather()
    weather_dict = get_weather_obj.getWeatherCity(location)
    # Mocked response data
    weather_info = {
        "location": location,
        "temperature": weather_dict['temperature'],
        "unit": unit,
        "forecast": [weather_dict['status']],
    }
    return weather_info


class GetCurrentWeatherCheckInput(BaseModel):
    location: str = Field(..., description="The name of the location for which we need to find the weather")
    unit: str = Field(..., description="The unit for the temperature value")


class GetCurrentWeatherTool(BaseTool):
    name = "get_current_weather"
    description = "Used to find the weather for a given location in said unit"

    def _run(self, location: str, unit: str):
        weather_response = get_current_weather(location, unit)
        return weather_response

    def _arun(self, location: str, unit: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GetCurrentWeatherCheckInput


class AddNumbersInput(BaseModel):
    num1: float = Field(..., description="The first number to add")
    num2: float = Field(..., description="The second number to add")


class AddNumbersTool(BaseTool):
    name = "add_numbers"
    description = "Used to add two numbers"

    def _run(self, num1: float, num2: float):
        return num1 + num2

    def _arun(self, num1: float, num2: float):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = AddNumbersInput


os.environ["OPENAI_API_KEY"] = "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"
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

model_name = "gpt-3.5-turbo-0613"

tools = [GetCurrentWeatherTool()]  # add multiple function-tools here
functions = [convert_to_openai_function(tool) for tool in tools]  # Updated function

model = ChatOpenAI(model=model_name, temperature=0)


def main(query):
    # Example query

    tools = [GetCurrentWeatherTool(), AddNumbersTool()]

    functions = [convert_to_openai_function(tool) for tool in tools]  # Updated function

    response_ai_message = model.invoke([HumanMessage(content=query)], functions=functions)

    args = json.loads(response_ai_message.additional_kwargs['function_call'].get('arguments'))

    tool_name = response_ai_message.additional_kwargs['function_call'].get('name')
    tool = next((t for t in tools if t.name == tool_name), None)

    if tool:

        tool_result = tool.run(tool_input=args)

        # Prepare the function message
        function_message = FunctionMessage(name=tool_name, content=str(tool_result))

        # Generate final response
        response_final = model.invoke(
            [HumanMessage(content=query), response_ai_message, function_message],
            functions=functions
        )

        print(response_final.content)
    else:
        print("No matching tool found for the given function name.")


if __name__ == "__main__":
    query = "What is 10 plus 9"
    main(query)