import os
import together
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
import logging
from typing import Any, Dict, List, Mapping, Optional

from pydantic import Extra, Field, root_validator

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env

import together

import logging
from typing import Any, Dict, List, Mapping, Optional

from pydantic import Extra, Field, root_validator

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from langchain.utils import get_from_dict_or_env

# Import Flask modules
from flask import Flask, request, jsonify

class TogetherLLM(LLM):
    # ... (your existing TogetherLLM code)

app = Flask(__name__)

# Global variable for conversation history
conversation_history = []

@app.route('/')
def hello():
    return 'Hello, welcome to my Flask server!'

@app.route('/post_example', methods=['POST'])
def post_example():
    global conversation_history

    if request.method == 'POST':
        try:
            # Ensure that the data is in JSON format
            data = request.get_json()
            if not data:
                raise ValueError("Invalid JSON format")

            # Process the data
            if 'question' in data:
                received_message = data['question']
                conversation_history.append(received_message)
                o = predict(received_message, conversation_history)
                return jsonify({"received_message": received_message, "response": o})
            else:
                return jsonify({"error": "No 'question' key found in the JSON data"})
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "This endpoint only accepts POST requests"})

def predict(que, conversation_history):
    global llm  # Use the LLM instance globally

    # Debug print to check conversation history
    print("Conversation History:", conversation_history)

    # Use conversation_history in LLMChain or other relevant places
    # For example, you may want to clear memory before making a new prediction
    llm.memory.clear()
    
    k = llm.predict(question=que)
    print(k)
    lines = k.split('\n')
    chatbot_value = k  # Default to the full response if 'AI:' is not found
    ai_lines = [line.split('AI: ', 1)[-1].strip() for line in lines if 'AI:' in line]
    
    # Debug print to check AI lines
    print("AI Lines:", ai_lines)

    # Print and return only unique 'AI:' lines
    for ai_line in set(ai_lines):
        print(ai_line)
        chatbot_value = ai_line

    return chatbot_value

# if __name__ == '__main__':
#    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
