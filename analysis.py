import mysql.connector
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cp = 4200  # J/(kg*K)
pyranometer_constant = 10.5  # uV/(W/m2)
area = 1.3 * 0.66 # m

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


def plotEfficiencyDTI(df):
    s = sns.scatterplot(data = df
                    ,x = 'dt_i'
                    ,y = 'eff'
                    # ,edgecolor = 'none'
                    ,alpha = .5
                    # ,color = 'darkred'
                    )
    ax = s.axes
    ax.axvline(0, c='black', ls='--', linewidth=0.5)
    ax.set_ylabel('Efficiency')
    ax.set_xlabel('(Tin - Tamb) / I')
    ax.set_ylim(0, 1)
    ax.set_xlim(-0.004, 0.03)
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
df = df.loc[f"{day} 09:50:00":f"{day} 11:50:00"]
df['eff'] = df['FLOW'] * cp * (df["OUT"] - df["IN"]) / (df["IRR"] * area)

df['eff'].plot()
plt.show()

df["dt_i"] = (df["IN"] - df['Tamb2']) / df['IRR']
# df = df.reset_index()
plotEfficiencyDTI(df)


