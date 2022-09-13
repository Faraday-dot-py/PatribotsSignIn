#A chatbot


import random

# Define a function that returns a random greeting
def greeting():
    # Define a list of responses
    responses = ["Hello, how are you?", "Hi, how are you doing?", "Hello, how are you feeling today?"]
    # Return a random response
    return random.choice(responses)

# Define a function that returns a random question
def question():
    # Define a list of responses
    responses = ["What is your name?", "What is your favorite color?", "What is your favorite food?"]
    # Return a random response
    return random.choice(responses)

# Define a function that returns a random statement
def statement():
    # Define a list of responses
    responses = ["I like you.", "You are cool.", "You are awesome."]
    # Return a random response
    return random.choice(responses)

# Define a function that returns a random response
def response():
    # Define a list of responses
    responses = ["That is interesting.", "Tell me more.", "Why do you think that?"]
    # Return a random response
    return random.choice(responses)

# Define a function that returns a random goodbye
def goodbye():
    # Define a list of responses
    responses = ["Goodbye!", "See you later!", "Have a nice day!"]
    # Return a random response
    return random.choice(responses)


# Define a function that sends a message to the bot
def send_message(message):
    # Print user_template including the user_message
    print(user_template.format(message))
    # Create responses
    if message == "hello":
        response = greeting()
    elif message == "goodbye":
        response = goodbye()
    elif message[-1] == "?":
        response = question()
    elif message[-1] == ".":
        response = statement()
    else:
        response = response()
    # Print the bot template including the bot's response.
    print(bot_template.format(response))

# Define a function that runs the bot
def run():
    # Print the start message
    print("Hi, I'm a chatbot. I like to chat with people. If you want to exit, type 'goodbye'.")
    # While the user input is not goodbye, keep chatting
    while True:
        message = input("You: ")
        if message == "goodbye":
            send_message(message)
            break
        else:
            send_message(message)

# Run the function
run()
