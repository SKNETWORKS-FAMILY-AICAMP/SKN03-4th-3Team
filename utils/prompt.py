from .constant import CHATBOT_MESSAGE, CHATBOT_ROLE

def create_message(role:CHATBOT_ROLE, prompt:str):

    return {
        CHATBOT_MESSAGE.role.name: role.name,
        CHATBOT_MESSAGE.content.name: prompt
    }
