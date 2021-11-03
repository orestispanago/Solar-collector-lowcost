import datetime
import datareader
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
import json

params = {'figure.figsize': (9, 6),
          'axes.titlesize': 18,
          'axes.titleweight': 'bold',
          'axes.labelsize': 24,
          'axes.labelweight': 'bold',
          'xtick.labelsize': 18,
          'ytick.labelsize': 18,
          'font.weight' : 'bold',
          'font.size': 18,
          'savefig.dpi': 300.0,
          'savefig.format': 'png',
          'figure.constrained_layout.use': True}
plt.rcParams.update(params)

cp = 4200  # J/(kg*K)
pyranometer_constant = 10.5  # uV/(W/m2)
area = 1.3 * 0.66 # m

clear_sky = datetime.date(2021, 10, 4)
stagnation = datetime.date(2021, 10, 5)

def convertUnits(df):
    df["Flow"] = df["Flow"] / 3600  # liters/h to litres/s
    df["FlowS"] = df["FlowS"] / 3600
    df["Irr"] = df["Irr"] * 1000 / pyranometer_constant  # mV to W/m2
    df["IrrS"] = df["IrrS"] * 1000 / pyranometer_constant
    return df

def calc_dt_i(df, Tin="Tin"):
    df["eff"] = df["Flow"] * cp * (df["Tout"] - df[Tin]) / (df["Irr"] * area)
    df["dt_i"] = (df[Tin] - df["Tenv2"]) / df["Irr"]

def save_regresults(linregress):
    linregress_dict = {
        "slope": linregress.slope,
        "intercept": linregress.intercept,
        "slope_stderr":linregress.stderr,
        "intercept_stderr": linregress.intercept_stderr,
        "rvalue": linregress.rvalue,
        "pvalue":linregress.pvalue
        }
    with open("linregress_stats.json", "w") as f:
        json.dump(linregress_dict,f, indent=4)

def plot_efficiency_dt_i(df, linregress):
    g = sns.regplot(x=all_days["dt_i"], 
                    y=all_days["eff"], 
                    scatter_kws={'s':1},
                    line_kws={'label': "$y={0:.1f}x+{1:.1f}$".\
                              format(linregress.slope, linregress.intercept)})
    g.legend()
    ax = g.axes
    ax.axvline(0, c='black', ls='--', linewidth=0.5)
    ax.axhline(0,  c='black', ls='--', linewidth=0.5)
    ax.set_ylabel('$n$')
    ax.set_xlabel('$\\frac{Tin - Tamb}{I}$')
    ax.set_ylim(-0.05, 1)
    plt.savefig("eff_dt_i")
    plt.show()

clear_sky_raw = datareader.selectDay(clear_sky)
stagnation_raw = datareader.selectDay(stagnation)
# clear_sky_raw.to_csv(f"{clear_sky}.csv")
# stagnation_raw.to_csv(f"{stagnation}.csv")
clear_sky_converted = convertUnits(clear_sky_raw)
stagnation_converted = convertUnits(stagnation_raw)

calc_dt_i(clear_sky_converted)
calc_dt_i(stagnation_converted, Tin="Tafmu")

clear_sky_converted["Tout_Tin"] = clear_sky_converted["Tout"] - clear_sky_converted["Tin"]
clear_sky_converted["ToutS_TinS"] = clear_sky_converted["ToutS"] - clear_sky_converted["TinS"]
clear_sky_converted.describe().to_csv("describe.csv")

clear_sky_selected = clear_sky_converted.loc[f"{clear_sky} 10:30:00": 
                                             f"{clear_sky} 12:30:00"]
stagnation_selected = stagnation_converted.loc[f"{stagnation} 10:00:00":
                                               f"{stagnation} 11:00:00"]

df_list = [clear_sky_selected, stagnation_selected]
all_days = pd.concat(df_list, axis=0)

linregress = stats.linregress(all_days["dt_i"], all_days["eff"])

plot_efficiency_dt_i(all_days, linregress)

# save_regresults(linregress)
