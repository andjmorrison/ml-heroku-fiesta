# flask, env
from dotenv import load_dotenv
from os import getenv
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# modeling
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense

# Load environment variables
load_dotenv()

# Create an instance of Flask
app = Flask(__name__)

# Get the connection string for the database
app.config['MONGO_URI'] = getenv('MONGO_URI', '')
print(getenv('MONGO_URI'))

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app)

# load model
model = load_model('iris_model')

classes = {
    0:'Iris-setosa',
    1:'Iris-versicolor',
    2:'Iris-virginica',
}

# predict function
def predict_class(provided_data, model_used):

    data = [list(provided_data.values())[0:4]]
    data = np.asarray(data, dtype=np.float32)

    std_scaler = StandardScaler().fit(data)
    scaled_data = std_scaler.transform(data)

    prediction = model_used.predict_classes(scaled_data)
    print(prediction)

    predicted_name = classes[prediction[0]]
    
    return(scaled_data, prediction, predicted_name)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    iris_data = mongo.db.iris.find_one({},{'_id':False})

    print(f'doc: {iris_data}')

    predicted_class = ""
    predicted_name = ""

    # Return template and data
    return render_template("index.html",
        iris=iris_data,
        prediction=predicted_class,
        prediction_name=predicted_name)

@app.route("/predict")
def predict():

    # pull mongo data
    iris_data = mongo.db.iris.find_one({},{'_id':False})
    print(f'doc: {iris_data}')

    # load model
    print("iris_model")

    # run pred func
    data, predicted_class, predicted_name = predict_class(iris_data, model)

    # Return template and data
    return render_template("index.html", 
        iris=iris_data, 
        prediction=predicted_class,
        prediction_name=predicted_name)

if __name__ == "__main__":
    app.run(debug=True)
