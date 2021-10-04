import datetime
import datareader
import matplotlib.pyplot as plt
import seaborn as sns

cp = 4200  # J/(kg*K)
pyranometer_constant = 10.5  # uV/(W/m2)
area = 1.3 * 0.66 # m

day = datetime.date(2021, 10, 4)


def convertUnits(df):
    df["Flow"] = df["Flow"] / 3600  # liters/h to litres/s
    df["Irr"] = df["Irr"] * 1000 / pyranometer_constant  # mV to W/m2
    return df


def plotEfficiencyDTI(df):
    s = sns.scatterplot(data = df,
                    x = 'dt_i',
                    y = 'eff',
                    edgecolor = 'none',
                    alpha = .5,
                    # ,color = 'darkred',
                    s=3
                    )
    ax = s.axes
    ax.axvline(0, c='black', ls='--', linewidth=0.5)
    ax.set_ylabel('Efficiency')
    ax.set_xlabel('(Tin - Tamb) / I')
    ax.set_ylim(0, 1)
    ax.set_xlim(-0.007, 0.03)
    plt.savefig("eff_dt_i.png")
    plt.show()

raw = datareader.selectDay(day)
# raw.to_csv(f"{day}.csv")
df = convertUnits(raw)

df["eff"] = df["Flow"] * cp * (df["Tout"] - df["Tin"]) / (df["Irr"] * area)
df["dt_i"] = (df["Tin"] - df["Tenv2"]) / df["Irr"]

df.set_index("time", inplace=True)
selected = df.loc[f"{day} 10:00:00": f"{day} 13:00:00"]


plotEfficiencyDTI(df)



