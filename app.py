from flask import Flask,render_template,request, jsonify
from chat import get_response
from voice import bot_speaks
app=Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods = ['POST'])
def predict():
    text=request.get_json().get("message")
    response = get_response(text)
    message={"answer":response}
    return jsonify(message)



@app.route("/audioOutput", methods = ['POST'])
def audioOutput():
    response = request.get_json().get("current_response")
    return jsonify(response), bot_speaks(response)

    
if __name__=="__main__":
    app.run(debug=True) 


