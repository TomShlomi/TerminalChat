import openai
import json
import argparse

root = "/Users/tomshlomi/ChatGPT/TerminalChat/"

def ask(question : str):
    with open(root + 'context.json', 'r') as fin:
        context = json.load(fin)
    try:
        context.append({"role": "user", "content": question})
        answer = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=context).choices[0].message.content
    except openai.error.APIConnectionError:
        print("No internet")
        return None
    context.append({"role": "assistant", "content": answer})
    print(answer)
    with open(root + 'context.json', 'w') as fout:
        json.dump(context, fout)
    return answer

def clear():
    with open(root + 'context.json', 'r') as fin:
        context = json.load(fin)
    with open(root + 'log.json', 'w') as log:
        json.dump(context, log)
    with open(root + 'context.json', 'w') as fout:
        json.dump([{"role": "system", "content": "You are Assistant, a helpful, harmless and honest chatbot."}], fout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="Question to ask")
    parser.add_argument("-c", "--clear", help="Clear context", action="store_true")
    if parser.parse_args().clear:
        clear()
    args = parser.parse_args()
    ask(args.question)