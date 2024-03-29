import numpy as np
import random
import json
import torch
import torch.nn as nn
from nltk.stem import WordNetLemmatizer
from torch.utils.data import Dataset, DataLoader
from nltk.corpus import stopwords
from nltk_utils import bag_of_words, tokenize
from model import NeuralNet

with open('intents.json', 'r') as f:
    intents = json.load(f)

lemmatizer = WordNetLemmatizer()

all_words = []
tags = []
xy = []

#words which are commonly used and hence don't help by grasping the meaning of the query
stopwords = stopwords.words('english')
stopwords.extend([":", ",", "%", "/'", "$", "!", "?", '&', "'m", "'s", '(', ')', '.', 'i'])

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = tokenize(pattern)
        # add to our words list
        all_words.extend(w)
        # add to xy pair
        xy.append((w, tag))

# stem and lower each word
all_words = [lemmatizer.lemmatize(w.lower()) for w in all_words if w not in stopwords]
# remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))

"""
print(len(xy), "patterns")
print(len(tags), "tags:", tags)
print(len(all_words), "unique lemmatized words:", all_words)
"""

# create training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    # X: bag of words for each pattern_sentence
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    
    # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)
y_train = np.array(y_train)

# Hyper-parameters 
num_epochs = 1000
batch_size = 32
learning_rate = 0.001
input_size = len(X_train[0])
hidden_size = 446
output_size = len(tags)
print(input_size, output_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()

"""
# split dataset in train and validation set
full_datasize = len(dataset)
train_size = int(0.8 * full_datasize)
valid_size = full_datasize - train_size
"""

#dataset, validset = random_split(dataset, [train_size, valid_size])

train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)
"""
valid_loader = DataLoader(dataset = validset, 
                          batch_size = batch_size,  
                          shuffle=True, 
                          num_workers=0)

"""
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

#last_valid_loss = np.inf

# Train the model
for epoch in range(num_epochs):
    #train_loss = 0.0
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        #train_loss += loss.item()

    """
    #Extra validaiton loop
        valid_loss = 0.0
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(dtype=torch.long).to(device)

            # Forward pass
            outputs = model(words)
            # if y would be one-hot, we must apply
            # labels = torch.max(labels, 1)[1]
            loss = criterion(outputs, labels)
            
            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            valid_loss += loss.item()

        """
        
        
    
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
        
    """
    #Elaborate documentation: 
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}],Training Loss: {train_loss / len(train_loader)} \t\t Validation Loss: {valid_loss / len(valid_loader)}')
        if last_valid_loss > valid_loss:
            print(f'Validation Loss Decreased({last_valid_loss:.6f}--->{valid_loss:.6f})')
            last_valid_loss = valid_loss
    """

print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')