import openai

def form_prompt(inputs):
    # Constructing the prompt
    prompt = f"""
    You have a balance of {inputs['balance']} XRP with a ledger fee of {inputs['fee']} drops. You want to trade for {inputs['desired_currency']} currency.
    Given recent book offers: {inputs['book_offers']} and their corresponding transaction histories by index: {inputs['tx_history']}, I'm seeking a trading strategy that maximize returns.
    For simplicity now, the strategy should be limited to at most one offer submission. Please only tell me will user create offer to 'buy' or 'sell' for some <value>, or 'wait' profitable offer comes.
    
    CRITICAL: RESPOND IN ONLY THE FOLLOWING FORMAT. Example: ('buy', 10), ('sell', 5), ('wait')
    """

    return prompt

# Function to call OpenAI's completion API with a prompt
def gpt(prompt, OPENAI_API_KEY):
    openai.api_key = OPENAI_API_KEY

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "system",
                "content": "You are an AI trading bot trained to provide trading advice."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    res = response.choices[0].message["content"]
    
    return res