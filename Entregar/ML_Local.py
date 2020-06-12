# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 12:58:02 2020

@author: Otto
"""


#import logging
#import azure.functions as func
import pyodbc
import pandas as pd
import json
import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report,accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
   

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     req_body = req.get_json()
#     variable1 = req_body.get('variable1')
    
    
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-PNBI83D7\SQLEXPRESS;'
                      'Database=Matrixa;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
   

sql = "SELECT * FROM Datos"
df = pd.read_sql(sql,conn)
   
Datos = df.to_numpy(dtype='float64')
x = Datos[:,:-1]
y = Datos[:,15:16]
X_train, X_test, Y_train, Y_test = train_test_split(x[:649,:],y,test_size=0.3,random_state=42)


#%%e*******   SVM     *******#####
modelo = SVC(kernel='rbf')
modelo.fit(X_train, Y_train)
predicciones = modelo.predict(X_test)
AccActual = accuracy_score(Y_test,predicciones)
json_response = json.dumps(AccActual,indent=2)
    

#%%*******   KNN     *******#
algKNN = KNeighborsClassifier(n_neighbors = 10, metric = 'minkowski', p = 2)
algKNN.fit(X_train, Y_train)
pr1 = algKNN.predict(X_test)
res_K = classification_report(Y_test, pr1)
json_response1 = json.dumps(res_K,indent=2)



#%%*******     Naive Bayes    *******#
alg_NB = GaussianNB()
alg_NB.fit(X_train, Y_train)
pr2 = alg_NB.predict(X_test)
res_N = classification_report(Y_test, pr2)
# json_response2 = json.dumps(res_N,indent=2)
# json_responseT = json_response + json_response1 + json_response2
# if variable1 < 10:
#     return func.HttpResponse(json_responseT)
# else:
#     return func.HttpResponse("Valor invalido en el Postman!-- Función ejecutada correctamente :)",status_code=200)