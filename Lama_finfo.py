from Functions.sound import *

class Function_info:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "increase_system_volume",
                "description": "Increases the volume of the computer and returns the current volume of the computer, if it doesnt, False is returned",
                "parameters": {
                    "type": "object",
                    "properties": {
                        'percentage':{
                            'type':"integer",
                            'description':'Percentage volume to be increased or decreased'
                        },
                    },
                    'required':['percentage']
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "decrease_system_volume",
                "description": "decreases the volume of the computer by a certain percentage and returns the current volume, by default it decreases it by 10 if it doesnt, False is returned",
                "parameters": {
                    "type": "object",
                    "properties": {
                        'percentage':{
                            'type':"integer",
                            'description':'Percentage volume to be increased or decreased'
                        },
                    },
                    'required':['percentage']
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "set_system_volume",
                "description": "Sets the volume of the computer to a certain percentage and returns the current volume.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        'percentage':{
                            'type':"integer",
                            'description':'Percentage volume to be increased or decreased'
                        },
                    },
                    'required':['percentage']
                },
            },
        }
    ]


    available_functions = {
            "set_system_volume": Volume.set_system_volume,
            "increase_system_volume": Volume.increase_system_volume,
            "decrease_system_volume":Volume.decrease_system_volume
        }