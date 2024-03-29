from pydantic import BaseModel, Field
from typing import Optional, Type
import json
import os

from langchain_community.tools import BaseTool, format_tool_to_openai_function
from langchain_community.schema import HumanMessage, AIMessage, FunctionMessage
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain_community.agents import AgentType, initialize_agent, Tool
from LLM.ChatBot.WeatherAgent.GetWeather import GetWeather
from LLM.Server.outpaintAPI.outpaintAPI import OutpaintAPI


class WeatherTool(BaseTool):
    name = "get_current_weather"
    description = "Used to find the weather for a given location in said unit"

    def _run(self, location: str, unit: str):
        get_weather_obj = GetWeather()
        weather_dict = get_weather_obj.getWeatherCity(location)
        weather_info = {
            "location": location,
            "temperature": weather_dict['temperature'],
            "unit": unit,
            "forecast": [weather_dict['status']],
        }
        return weather_info

    def _arun(self, location: str, unit: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = BaseModel


class AddNumbersTool(BaseTool):
    name = "add_numbers"
    description = "Used to add two numbers"

    def _run(self, num1: float, num2: float):
        return num1 + num2

    def _arun(self, num1: float, num2: float):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = BaseModel


class OutpaintImageTool(BaseTool):
    name = "outpaint_image"
    description = "Outpaints the image provided as input"

    def _run(self, image_bytes: bytes):
        outpaint_api = OutpaintAPI(image_bytes)
        outpainted_image = outpaint_api.outpend_image()
        return outpainted_image

    def _arun(self, image_bytes: bytes):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = BaseModel


class ChatBot:
    def __init__(self, model_name: str, api_key: str):
        os.environ["OPENAI_API_KEY"] = api_key
        self.model_name = model_name
        self.model = ChatOpenAI(model=model_name, temperature=0)
        self.tools = [WeatherTool(), AddNumbersTool(), OutpaintImageTool()]
        self.functions = [format_tool_to_openai_function(tool.name) for tool in self.tools]

    def process_message(self, query: str, image_bytes: Optional[bytes] = None):
        response_ai_message = self.model.predict_messages([HumanMessage(content=query)], functions=self.functions)
        args = json.loads(response_ai_message.additional_kwargs['function_call'].get('arguments'))
        tool_name = response_ai_message.additional_kwargs['function_call'].get('name')
        tool = next((t for t in self.tools if t.name == tool_name), None)

        if tool:
            if tool_name == "outpaint_image" and image_bytes is not None:
                tool_result = tool.run(image_bytes)
                return tool_result
            else:
                tool_result = tool.run(**args)

            function_message = FunctionMessage(name=tool_name, content=str(tool_result))
            response_final = self.model.predict_messages(
                [HumanMessage(content=query), response_ai_message, function_message],
                functions=self.functions
            )
            return response_final.content
        else:
            return "No matching tool found for the given function name."


# if __name__ == "__main__":
#     query = "Outpaint the below image"
#     sample_image_bytes = b'your_image_bytes_here'
#     chatbot = ChatBot(model_name="gpt-3.5-turbo-0613", api_key="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")
#     print(chatbot.process_message(query, image_bytes=sample_image_bytes))
