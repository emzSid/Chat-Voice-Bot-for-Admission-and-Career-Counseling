import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from rule_based_answers import course_inputs, course_responses, ErrorMsg, validOneWord, career_paths_responses, career_paths_inputs


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"


def get_response(msg):
    
    # split query in single words and store all in an array
    query_array = tokenize(msg)

    #go through the array containing all words in the query
    for word in query_array:
        #go through all possible course names and remember its index
        for idx, course_names in enumerate(course_inputs):
            #convert the word in lower case
            #give corresponding response if course name was found in the query 
            if word.lower() in course_names:
                    return course_responses[idx]

    #go through the array containing all words in the query
    for word in query_array:
        #go through all possible keywords regarding career and remember its index
        for idx, input in enumerate(career_paths_inputs):
            #convert the word in lower case
            #give corresponding response if keyword equal to the query 
            if word.lower() == input:
                    return career_paths_responses[idx]

    #if query only contains one word and this word is not in the list of valid single words,
    #then respond request to type at least two words
    if len(query_array) < 2:
        if query_array[0].lower() not in validOneWord:
            return "Thanks for reaching out! Type in at least two full words to get a proper response."

    #convert user-input into computer-understandable format (array of zeros and ones)
    X = bag_of_words(query_array, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    """predict correct response using the ann model"""

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return random.choice(ErrorMsg)


'''if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)'''



