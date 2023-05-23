from copyreg import pickle
import os
import re
from statistics import mode
from flask import Flask, render_template, request as req, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

app = Flask(__name__)
cors = CORS(app)

@app.post("/input")
@cross_origin()
def predict():
    f = req.files['file']
    f.save(secure_filename(f.filename))
    fileName = os.path.abspath(f.filename)
    df = pd.read_csv(fileName)
    if "Date" and "SalesPrice" in df.columns:
        df.set_index('Date')
        if req.form.get('periodicity') == 'weekly':
            df['Sale_lastweek']=df['SalesPrice'].shift(+1)
            df['Sale_2weeksback']=df['SalesPrice'].shift(+2)
            df['Sale_3weeksback']=df['SalesPrice'].shift(+3)
        elif req.form.get('periodicity') == 'monthly':  
            df['Sale_LastMonth']=df['SalesPrice'].shift(+1)
            df['Sale_2Monthsback']=df['SalesPrice'].shift(+2)
            df['Sale_3Monthsback']=df['SalesPrice'].shift(+3)
        elif req.form.get('periodicity') == 'yearly': 
            df['Sale_Lastyear']=df['SalesPrice'].shift(+1)
            df['Sale_2yearback']=df['SalesPrice'].shift(+2)
            df['Sale_3yearback']=df['SalesPrice'].shift(+3)
        df=df.dropna()
        model = pickle.load(open("Models\RfRegressor",'rb'))
        if req.form.get('periodicity') == 'weekly':
              x1,x2,x3,y=df['Sale_lastweek'],df['Sale_2weeksback'],df['Sale_3weeksback'],df['SalesPrice']
        if req.form.get('periodicity') == 'monthly':
              x1,x2,x3,y=df['Sale_LastMonth'],df['Sale_2Monthsback'],df['Sale_3Monthsback'],df['SalesPrice']
        if req.form.get('periodicity') == 'yearly':
              x1,x2,x3,y=df['Sale_Lastyear'],df['Sale_2yearback'],df['Sale_3yearback'],df['SalesPrice']
        x1,x2,x3,y=np.array(x1),np.array(x2),np.array(x3),np.array(y)
        x1,x2,x3,y=x1.reshape(-1,1),x2.reshape(-1,1),x3.reshape(-1,1),y.reshape(-1,1)
        final_x=np.concatenate((x1,x2,x3),axis=1)
        print(final_x)
        X_train,X_test,y_train,y_test=final_x[:-30],final_x[-30:],y[:-30],y[-30:]
        pred = model.predict(X_test)
        plt.rcParams["figure.figsize"] = (12,8)
        plt.plot(pred,label='Forecast')
        plt.plot(y_test,label='Actual Sales')
        plt.legend(loc="upper left")
        plt.show()

        return "Successfully Predicted"
    else:
        return "Your dataset does not contain 'Date' or 'SalesPrice'"    


    


app.run()