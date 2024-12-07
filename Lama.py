from groq import Groq
import os
import json
import requests
import Lama_finfo

grok_api_key="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"
client = Groq(api_key = grok_api_key)
MODEL = 'llama3-70b-8192'




def run_conversation(user_prompt):
    # Step 1: send the conversation and available functions to the model
    messages=[
        {
            "role": "system",
            "content": "Your name is Yididya, You are a systems chat bot that helps blind people easily use the computer. You can answer simple questions, you can also engage in small talk but keep your responces short. You have functions avaiable to you to help the user execute what they want, Always keep your responces short, Do not do something unless asked"
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = Lama_finfo.Function_info.tools
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",  
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = Lama_finfo.Function_info.available_functions
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content
    else:
        return response.choices[0].message.content