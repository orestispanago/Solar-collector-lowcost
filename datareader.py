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
    mycursor.execute("SELECT * FROM measurements WHERE time BETWEEN %s AND %s",
                     (start_date, end_date))
    data = pd.DataFrame(mycursor.fetchall())
    data.columns = mycursor.column_names
    mydb.close()
    return data


def selectToday():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM measurements WHERE DATE(time) = CURDATE()")
    dfout = pd.DataFrame(mycursor.fetchall())
    dfout.columns = mycursor.column_names
    mydb.close()
    return dfout
