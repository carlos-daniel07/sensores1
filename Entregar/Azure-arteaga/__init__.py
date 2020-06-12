import logging
import azure.functions as func
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import json
import pickle
import joblib
import pyodbc 
import pandas as pd
import numpy as np

def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    variable1 = req_body.get('variable1')
    azuredriver = "ODBC Driver 17 for SQL Server"
    azurebase = "sensores1-arteaga"
    usuario = "sensores1_arteaga" 
    password = "Annydelcarmen09"
    server = "servidor-sensores1-arteaga.database.windows.net"
    connStr = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+azurebase+';UID='+usuario+';PWD='+ password)
    cursor = connStr.cursor()
    SQL_Script = "SELECT * FROM dbo.Daniel_Arteaga_Data"

    df = pd.io.sql.read_sql(SQL_Script,connStr)
    connStr.close()
    Datos= df.to_numpy()

    X=Datos[:,:-3]
    y=Datos[:,15:18]
    m,n = X.shape
    Y=[]
    for i in range(m):
        if np.all(y[i,:]==['0','1','0']):
            Y.append(2)
        elif np.all(y[i,:]==['0','0','1']):
            Y.append(3)
        elif np.all(y[i,:]==['1','0','0']):
            Y.append(1)

    Y=np.asarray(Y).T
    Y=Y.reshape((m,1))
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3,random_state=42)
    modelo = SVC(kernel='rbf')
    modelo.fit(X_train, Y_train)
    predicciones = modelo.predict(X_test)
    AccActual = accuracy_score(Y_test,predicciones)
    json_response = json.dumps(classification_report(Y_test, predicciones),indent=2)
    if variable1 < 10:
        return func.HttpResponse(json_response)
    else:
        return func.HttpResponse("NUBE Puede que se ingresara in valor mal en el postman pero la funcion se ejecuto meleramente",status_code=200)
