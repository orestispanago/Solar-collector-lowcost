import datareader
import matplotlib.pyplot as plt

cp = 4200  # J/(kg*K)
pyranometer_constant = 10.5  # uV/(W/m2)
area_fpc = 1.3 * 0.66
area_sco4 = 0.275 * 0.275


def convertUnits(df):
    df["Flow"] = df["Flow"] / 3600  # liters/h to litres/s
    df["Irr"] = df["Irr"] * 1000 / pyranometer_constant  # mV to W/m2


df = datareader.selectToday()
convertUnits(df)

irr = df["Irr"]
flow = df["Flow"]
tamb = df["Tenv2"]
df["eff_fpc"] = flow * cp * (df["Tlout"] - df["Tlin"]) / (irr * area_fpc)
df["eff_sco4"] = flow * cp * (df["Tsout"] - df["Tsin"]) / (irr * area_sco4)
df["dt_i_fpc"] = (df["Tlin"] - tamb) / irr
df["dt_i_sco4"] = (df["Tsin"] - tamb) / irr

df.set_index("time", inplace=True)
selected = df.loc["2021-09-14 12:59:00":"2021-09-14 13:15:00"]


def plotEfficiencyDTI(df, x=None, y=None, label=None):
    coly = df[y]
    colx = df[x]
    plt.plot(colx, coly, '.', label=label)
    plt.ylabel("Efficiency")
    plt.xlabel("(Tin - Tamb) / I")
    plt.axvline(0, c='black', ls='--')
    plt.axhline(0, c='black')
    plt.axis([-0.005,0.05,0,1])
    plt.legend()


plotEfficiencyDTI(selected, x="dt_i_fpc", y="eff_fpc", label="FPC")
plotEfficiencyDTI(selected, x="dt_i_sco4", y="eff_sco4", label="SCO4")
plt.show()
