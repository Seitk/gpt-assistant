import gpt_assistant.llm_agent as llm_agent
import gpt_assistant.chat.response as response
import json
import falcon
from dotenv import load_dotenv
load_dotenv()


initial_prompt = {"role": "system", "content": "Acts like a smart home assistant, your name is Atom. I will be your user, you will be my assistant and help with some home tasks. Do not write all the conservation at once, wait for my response. I want you to only do the talk with for with a kind tone, do not mention anything related to AI and do not ask me for context. Keep the response short and one sentence. Now talk to me."}
messages = [
    initial_prompt,
]


def generate_response(prompt):
    global messages
    res = llm_agent.execute_agent(prompt)

    # Add user prompt
    messages.append({"role": "user", "content": prompt})

    if "RESET_CONTEXT" in res:
        messages = [initial_prompt]
        return "Context reset successfully."
    elif "DEFAULT_ACTION" in res:
        print("Response in ChatGPT conversation")
        res = response.generate_response(messages)

    # Add response to the context
    messages.append({"role": "assistant", "content": res})
    return res


class AssistantChatResource:
    def on_post(self, req, resp):
        """Handle POST requests."""
        try:
            doc = json.load(req.stream)
            prompt = doc['text']
            response = generate_response(prompt)
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "response": response,
            })
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({
                "error": str(e),
            })


app = falcon.App()
app.add_route('/v1/commands', AssistantChatResource())
