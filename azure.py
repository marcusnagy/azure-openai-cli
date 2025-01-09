import os
import time
import argparse
from typing import List
from openai import AzureOpenAI

def start_conversation(
    client: AzureOpenAI,
    assistant_id,
    thread_id=None,
    prompt="hi",
    conversation: bool=False,
    sources: bool=False
    ):
    if thread_id is None:
        thread = client.beta.threads.create()
        thread_id = thread.id
        print(f"Thread ID: {thread_id}")
    elif not conversation:
        thread = client.beta.threads.retrieve(thread_id=thread_id)
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            order="asc",
        )
        for msg in messages:
            print(f"{msg.role.capitalize()}: {msg.content}")
            

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc",
        )
        for msg in messages:
            txt, annotations = printMessageContent(msg.content)
            if sources:
                sourcesData =f"-> Sources: { annotations if len(annotations) > 0 else 'None' }"
            print(f"{msg.role.capitalize()}: {txt}\n{sourcesData if sources else ''}")
    elif run.status == 'requires_action':
        pass
    else:
        print(run.status)

    return thread_id

def printMessageContent(content: List) -> tuple[str, str]:
    text = ""
    annotations = []
    for c in content:
        if c.type == "text":
            text += c.text.value
            annotations.extend(c.text.annotations)
    return text, annotations

def interactive_conversation(client, assistant_id, thread_id):
    while True:
        prompt = input("You: ")
        if prompt.lower() in ['exit', 'quit']:
            break
        thread_id = start_conversation(client, assistant_id, thread_id, prompt, conversation=True)

def main():
    parser = argparse.ArgumentParser(description="Azure Assistant CLI")
    parser.add_argument('--start', action='store_true', help="Start a new conversation")
    parser.add_argument('--thread', type=str, help="Thread ID to continue the conversation")
    parser.add_argument('--assistant', type=str, default="asst_5KHAEkFgKbwiM5MdCXbNQTDJ", help="Assistant ID")
    parser.add_argument('--prompt', type=str, default="hi", help="Initial prompt for the conversation")
    parser.add_argument('--sources', action='store_true', help="Show sources for the response")

    args = parser.parse_args()

    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-05-01-preview"
    )

    if args.start:
        thread_id = start_conversation(client, args.assistant, args.thread, args.prompt)
        interactive_conversation(client, args.assistant, thread_id)

if __name__ == "__main__":
    main()