import torch
import torch.nn as nn


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, 80)
        self.l2 = nn.Linear(80, 40) 
        self.l3 = nn.Linear(40, num_classes)
        self.relu = nn.ReLU()
         #randomly ignore 50% of the neurons during training phase to avoid overfitting
        self.dropout1 = nn.Dropout(0.5)
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        
        out = self.dropout1(out)

        out = self.l2(out)
        out = self.relu(out)

        out = self.l3(out)
        return out

    