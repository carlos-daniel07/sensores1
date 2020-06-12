# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 23:02:44 2020

@author: Otto
"""


import pandas as pd
import pyodbc

# Import CSV
data = pd.read_csv ("C:\\Users\\Otto\\Documents\\ITM\\2020-1\\Sensores\\SQl\\Entregar\\Daniel_Arteaga_Data.csv")   
df = pd.DataFrame(data, columns= ['S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','S11','S12','S13','S14','S15','Clases'])

# Connect to SQL Server
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-PNBI83D7\SQLEXPRESS;'
                      'Database=Matrixa;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()


# Create Table
cursor.execute('CREATE TABLE Datos (S1    NVARCHAR(15),S2    NVARCHAR(15),S3    NVARCHAR(15),S4    NVARCHAR(15),S5    NVARCHAR(15),S6    NVARCHAR(15),S7    NVARCHAR(15),S8    NVARCHAR(15),S9    NVARCHAR(15),S10    NVARCHAR(15),S11    NVARCHAR(15),S12    NVARCHAR(15),S13    NVARCHAR(15),S14    NVARCHAR(15),S15    NVARCHAR(15),Clases  NVARCHAR(4),)')

# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO Matrixa.dbo.Datos (S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15,Clases)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''',
                row.S1,
                row.S2,
                row.S3,
                row.S4,
                row.S5,
                row.S6,
                row.S7,
                row.S8,
                row.S9,
                row.S10,
                row.S11,
                row.S12,
                row.S13,
                row.S14,
                row.S15,
                row.Clases,
                )
conn.commit()