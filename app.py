from flask import Flask, render_template, request, jsonify
from flask_cors import CORS,cross_origin
import pickle
import sklearn
import os

app = Flask(__name__) # initializing a flask app

@app.route('/', methods=['GET','POST'])  # route to display the home page
def homePage():
    return render_template("index.html")

@app.route('/predict', methods=['GET','POST']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            gre_score=float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            if(is_research=='yes'):
                research=1
            else:
                research=0
            filename = 'linear_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=loaded_model.predict([[gre_score,toefl_score,university_rating,sop,lor,cgpa,research]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=round(100*prediction[0]))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'Something is Wrong!'
    # return render_template('results.html')
    else:
        return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True)
