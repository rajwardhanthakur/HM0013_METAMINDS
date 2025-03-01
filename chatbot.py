import requests

API_URL = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
HEADERS = {"Authorization": "Bearer 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"}

chat_history = []  # Store previous messages

def chat_with_bot(user_input):
    global chat_history
    chat_history.append(f"User: {user_input}")

    # Ensure proper input structure
    prompt = "\n".join(chat_history[-5:]) + "\nBot:"

    # Send request with parameters to limit response
    response = requests.post(API_URL, headers=HEADERS, json={
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,  # Prevents long outputs
            "return_full_text": False,  # Prevents repeating input
            "stop": ["\nUser:", "\nBot:"]  # Stops generation early
        }
    })

    # Print raw response for debugging
    print("\nAPI Raw Response:", response.text, "\n")

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        return "Error: Unable to decode response."

    if isinstance(data, dict) and "error" in data:
        return f"Error: {data['error']}"

    # Extract only generated text
    if isinstance(data, list) and len(data) > 0 and "generated_text" in data[0]:
        bot_response = data[0]["generated_text"].strip()
    else:
        bot_response = "Error: Unexpected response format."

    chat_history.append(f"Bot: {bot_response}")  # Add bot's response to history
    return bot_response

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print("Bot:", chat_with_bot(user_input))
