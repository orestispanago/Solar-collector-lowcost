import mysql.connector
import datetime
import pandas as pd
import matplotlib.pyplot as plt

cp = 4200  # J/(kg*K)
pyranometer_constant = 10.5  # uV/(W/m2)
area_fpc = 1.3 * 0.66 # m
area_sco4 = 0.275 * 0.275

day = datetime.date(2021, 9, 29)

def select(label):
    mydb = mysql.connector.connect(
    host="DatabaseIP",
    port="3360",
    user="ReadOnlyUser",
    passwd="ReadOnlyPassword",
    database="collector"
    )
    mycursor = mydb.cursor()
    mycursor.execute("""SELECT time, mean
                     FROM measurements_detailed WHERE label=%s""",
                     (label, ))
    data = pd.DataFrame(mycursor.fetchall())
    # data.columns = mycursor.column_names
    data.columns = ['time', label]
    data.set_index('time', inplace=True)
    mydb.close()
    return data

def convertUnits(df):
    df["FLOW"] = df["FLOW"] / 3600  # liters/h to litres/s
    df["IRR"] = df["IRR"] * 1000 / pyranometer_constant  # mV to W/m2


def plotEfficiencyDTI(df, x=None, y=None):
    coly = df[y]
    colx = df[x]
    plt.plot(colx, coly, '.')
    plt.ylabel("Efficiency")
    plt.xlabel("(Tin - Tamb) / I")
    plt.axvline(0, c='black', ls='--', linewidth=0.5)
    # plt.axhline(0, c='black')
    plt.axis([-0.005, 0.03, 0, 1])
    plt.show()

tin = select('IN')
tout = select('OUT')
amb = select('Tamb2')
flow = select('FLOW')
irr = select('IRR')

df_list = [tin, tout, flow, irr, amb]

df = pd.concat(df_list, axis=1)
convertUnits(df)
df = df.resample('1min').mean()
df = df.loc[f"{day} 09:50:00":f"{day} 11:40:00"]
df['eff'] = df['FLOW'] * cp * (df["OUT"] - df["IN"]) / (df["IRR"] * area_fpc)

df['eff'].plot()
plt.show()

df["dt_i"] = (df["IN"] - df['Tamb2']) / df['IRR']
df = df.reset_index()
plotEfficiencyDTI(df, x='dt_i', y='eff')
