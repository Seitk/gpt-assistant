#!/usr/bin/env python

import gpt_assistant.recording as recording
import gpt_assistant.wake_word as wake_word
import gpt_assistant.llm_agent as llm_agent
import gpt_assistant.text_to_speech.tts as tts
import gpt_assistant.chat.response as response

initial_prompt = {"role": "system", "content": "Acts like a smart home assistant, your name is Atom. I will be your user, you will be my assistant and help with some home tasks. Do not write all the conservation at once, wait for my response. I want you to only do the talk with for with a kind tone, do not mention anything related to AI and do not ask me for context. Keep the response short and one sentence. Now talk to me."}
messages = [
    initial_prompt,
]


def execute():
    """Main execution flow of the assistant"""
    global initial_prompt
    global messages

    text = recording.listen_for_speech()

    # Pass to LLM for command execution
    if text is not None and text != "":
        res = llm_agent.execute_agent(text)

        # Add user prompt
        messages.append({"role": "user", "content": text})

        if "RESET_CONTEXT" in res:
            messages = [initial_prompt]
            tts.text_to_speech("Context reset successfully.")
        elif "DEFAULT_ACTION" in res:
            print("Response in ChatGPT conversation")
            res = response.generate_response(messages)
            tts.text_to_speech(res)
        else:
            tts.text_to_speech(res)

        # Add response to the context
        messages.append({"role": "assistant", "content": res})


def main():
    try:
        print("GPT Assistant is running (press Ctrl+C to exit)")
        wake_word.listen_for_wake_word(execute)
    except KeyboardInterrupt:
        print("\rExiting...", end="")


if __name__ == '__main__':
    main()
