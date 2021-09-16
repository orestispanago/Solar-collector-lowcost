import datetime
import mysql.connector
import pandas as pd


mydb = mysql.connector.connect(
    host="databaseIP",
    port="3360",
    user="ReadOnlyUser",
    passwd="ReadOnlyPassword",
    database="collector"
)


def selectFromTo(start_date, end_date):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM measurements WHERE time BETWEEN %s AND %s",
                     (start_date, end_date))
    data = pd.DataFrame(mycursor.fetchall())
    data.columns = mycursor.column_names
    mydb.close()
    return data


def nextDay(day):
    return day + datetime.timedelta(days=1)


def dateToDatetime(date):
    return datetime.datetime.combine(date, datetime.datetime.min.time())


def selectDay(date):
    return selectFromTo(date, nextDay(date))
