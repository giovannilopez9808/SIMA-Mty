import matplotlib.pyplot as plt
from functions_SIMA import *
from functions import *
inputs = {
    "year initial": 2015,
    "year final": 2020,
    "path data": "../Archivos/",
    "path graphics": "../Graphics/PM10/",
    "stations names file": "Stations_name",
    "path stations": "../Stations/",
    "particle type": "PM10",
}
stations = pd.read_csv(
    inputs["path data"]+inputs["stations names file"]+".csv")
stations_len = stations["Nombre"].count()
colors = ['lightcoral',
          'coral',
          'chocolate',
          'orange',
          'lightgreen',
          'springgreen',
          'paleturquoise',
          'lightskyblue',
          'lightsteelblue',
          'mediumpurple',
          'violet',
          'orchid',
          'palevioletred']
plt.figure(figsize=(10, 8))
for station_i, color in zip(range(stations_len), colors):
    station = stations["Nombre"][station_i]
    title = stations["Name"][station_i].capitalize()
    PM_data = SIMA_data(
        inputs["year initial"],
        inputs["year final"],
        station,
        inputs["particle type"],
    )
    PM_data.read_data(inputs["path data"])
    PM_data.cut_data_year("2018-07-01", "2018-08-01")
    PM_2018 = PM_data.section.groupby(PM_data.section.index.hour).mean()
    plt.plot(np.arange(len(PM_2018)), PM_2018,
             label=title, color=color, lw=2.5, marker="o", ls="--")
plt.grid(ls="--", color="#000000", alpha=0.5, lw=2)
plt.xlim(0, 24)
plt.ylim(20, 140)
plt.xticks(np.linspace(0, 24, 7))
plt.legend(frameon=False, ncol=7, mode="expand",
           fontsize=10, bbox_to_anchor=(0, 1.09, 1, 0.02))
plt.subplots_adjust(left=0.12, bottom=0.11, right=0.94, top=0.912)
plt.xlabel("Local Time (h)", fontsize=16)
plt.ylabel("PM$_{10}$ $(\mu g/m^3)$", fontsize=16)
plt.savefig(inputs["path graphics"]+"July_2018_hour.png", dpi=400)
