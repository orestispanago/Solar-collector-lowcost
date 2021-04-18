import mysql.connector
import pandas as pd


mydb = mysql.connector.connect(
  host="DatabaseIP",
  port="3360",
  user="ReadOnlyUser",
  passwd="ReadOnlyPassword",
  database="collector"
)

def select(start_date, end_date):  
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM measurements WHERE Time BETWEEN %s AND %s", 
                     (start_date, end_date))
    data = pd.DataFrame(mycursor.fetchall())
    data.columns = mycursor.column_names
    mydb.close()
    return data

df = select('2021-04-18 00:00:00', '2021-04-18 16:00:00')
