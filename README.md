## Chat-Voice-Bot-for-Admission-and-Career-Counseling

### Table of Contents
1. Background
2. Technical Overview
3. Dataset
4. File Description
5. How to run the Code on a Development Server 


### Background
It can be very frustrating and time consuming to scan a university's website to find the exact answer one is looking for. An intelligent virtual assistant there though, is able to give specific, personalized and immediate responses to any time of the day or night. Hence, if the university has a Chatbot, an efficient and friendly conversation with that assistant can be a crucial parameter to decide to take admission at that place. As internship, at Integral University Lucknow, I I was given the project of developing an innovative Chat-Voice Bot for Admission and Career Counseling for their institution. 

### Technical Overview
The Chatbot is a both Artificial Intelligence and rule-based virtual assistant which uses NLP (Natural Language Processing) for preprocessing the natural language user-input. The responses are either predefined, giving a detected  keyword in the query, or selected based on the AI’s decision using an Artificial Neuronal Network. Hereby, we use HTML, CSS and JavaScript as frontend and the python framework PyTorch, Flask and NLTK (Natural Language Toolkit) library as backend. <br>

### Dataset
The Dataset for the ANN Model (intents.json) is a manually extended JSON file with intents. The Format looks as follows:
“intents” :[<br>
{<br>
“tag”: “tag_name”,<br>
“patterns”:[<br>
“pattern_1”,<br>
“pattern_2”,<br>
“pattern_3”,<br>
.<br>
.<br>
“pattern_n”<br>
],<br>
“responses”:[<br>
“response_1”,<br>
“response_2”,<br>
“response_3”,<br>
.<br>
.<br>
“response_n”]}<br>

### File Description: 
- **Folder: static** <br>
    - **images** <br>
    Contains all used images and icons as well as some black and white versions of     them <br>

      - **chatapp.css** <br>
      Presentation of the web page, including colors, layout, button design,  fonts       and more<br>
      
      - **chatapp.js** <br>
      Displays and updates the website's visual features <br>
      
- **Folder: templates** <br>
    - **index.html** <br>
   The main HTML file that's loaded when the user's web browser requests a web        server directory<br>
      
- **app.py** <br>
     Flask web application which runs and displays the information on the web     browser<br>
        
 - **chat.py** <br>
      Executes the procedure from a user's input to the selection of an appropriate response. The function get_response takes the user's message and does the following: <br>
      - checks whether a course name is in it<br>
      - checks whether it is a specific  career request<br>
      - checks if the input has a valid length<br>
      - converts the input in a so called "bag of words" (see NLTK)<br>
      - gives it to the Deep Learning Artificial Neuronal Network<br>
      - returns the chosen reponse as a string<br>

 - **model.py** <br>
      Defines the Artificial Neuronal Network. The MLP (Multilayer Perceptron) consists of four layers of nodes (an input layer, two hidden layer, and an output layer) and uses the nonlinear activation function rectified linear unit (ReLU).
In addition it has a Dropout of 50% after the first hidden layer<br>

- **nltk.utils.py** <br>
      Contains functions (tokenize, lemmatize, and creation of a bag of word) for doing NLP preprocessing. <br>
      
- **rule_based_answers.py**<br>
     In this file all specific keywords which should be detected in the user's question and their corresponding answers are defined<br>

 - **train.py** <br>
      Executes the NLP preprocessing of the training data, gives it to the ANN and  and updates the weights to gradually learn from the data. <br>
       
      - Classification Metric: CrossEntropyLoss <br>
      - Optimizer: Adam <br>
      - Hyperparameters: <br>
        - num_epochs = 1000<br>
        - batch_size = 32 <br>
        - learning_rate = 0.001<br>
        
- **voice.py**<br>
     Makes the text-response html notation free and then converts it into speech using gTTS<br>


### How to run the Code on a Development Server 

1. Install the needed packages with the command 
``` 
pip install -r requirements.txt 
```
(3. In case there is no trained ANN, run the train.py file)
4. Run app.py
5. Follow the given url (http://127.0.0.1:5000)
6. Click on the Chatbot icon and start the conversation with writing a greeting 
