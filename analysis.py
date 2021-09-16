import datetime
import datareader
import matplotlib.pyplot as plt

cp = 4200  # J/(kg*K)
pyranometer_constant = 10.5  # uV/(W/m2)
area_fpc = 1.3 * 0.66 # m
area_sco4 = 0.275 * 0.275

day = datetime.date(2021, 9, 15)


def convertUnits(df):
    df["Flow"] = df["Flow"] / 3600  # liters/h to litres/s
    df["Irr"] = df["Irr"] * 1000 / pyranometer_constant  # mV to W/m2


def plotEfficiencyDTI(df, x=None, y=None, label=None):
    coly = df[y]
    colx = df[x]
    plt.plot(colx, coly, '.', label=label)
    plt.ylabel("Efficiency")
    plt.xlabel("(Tin - Tamb) / I")
    plt.axvline(0, c='black', ls='--')
    plt.axhline(0, c='black')
    plt.axis([-0.005, 0.03, 0, 1])
    plt.legend()


df = datareader.selectDay(day)
convertUnits(df)

irr = df["Irr"]
flow = df["Flow"]
tamb = df["Tenv2"]
df["eff_fpc"] = flow * cp * (df["Tlout"] - df["Tlin"]) / (irr * area_fpc)
df["eff_sco4"] = flow * cp * (df["Tsout"] - df["Tsin"]) / (irr * area_sco4)
df["dt_i_fpc"] = (df["Tlin"] - tamb) / irr
df["dt_i_sco4"] = (df["Tsin"] - tamb) / irr

df.set_index("time", inplace=True)
selected_eff_dti = df.loc[f"{day} 12:30:00": f"{day} 12:50:00"]


plotEfficiencyDTI(selected_eff_dti, x="dt_i_fpc", y="eff_fpc", label="FPC")
plotEfficiencyDTI(selected_eff_dti, x="dt_i_sco4", y="eff_sco4", label="SCO4")
plt.show()


def plotDeltaTs(df):
    dt_fpc = df["Tlout"] - df["Tlin"]
    dt_fpc.name = "FPC"
    dt_sco4 = df["Tsout"] - df["Tsin"]
    dt_sco4.name = "SCO4"
    dt_fpc.plot(legend=True)
    dt_sco4.plot(ylabel="Tout - Tin (°C)", xlabel="Time, UTC", legend=True)
    plt.show()


def plotEfficiencies(df):
    dt_fpc = df["eff_fpc"]
    dt_fpc.name = "FPC"
    dt_sco4 = df["eff_sco4"]
    dt_sco4.name = "SCO4"
    dt_fpc.plot(legend=True)
    dt_sco4.plot(ylabel="Efficiency", xlabel="Time, UTC", legend=True)
    plt.show()


selected = df.loc[f"{day} 10:55:00":f"{day} 13:35:00"]
# resampled = df.resample("10s").mean()


plotDeltaTs(selected)
plotEfficiencies(selected)
