from functions_OMI import *
from functions import *
from os import listdir
import pandas as pd
import numpy as np
dir_data="../Archivos/"
input = {
    "path data": dir_data+"OMI_AOD_1/",
    # Path for HDF Files with 1 deg
    "path HDF": "/HDFEOS/GRIDS/Aerosol NearUV Grid/Data Fields/FinalAerosolSingleScattAlb",
    "lon": 25+40/60,
    "lat": -(100+18/60),
    "year initial": 2015,
    "year final": 2020,
}
AOD_list=["354","388","500"]
total_days = (input["year final"]-input["year initial"]+1)*365+2
dates = [consecutiveday2date(day, input["year initial"]) for day in range(
    total_days) if not "0229" in consecutiveday2date(day, input["year initial"])]
data_AOD = pd.DataFrame(index=dates, columns=[AOD+"nm" for AOD in AOD_list])
for AOD in AOD_list:
    print("Analizando longitud de onda "+AOD)
    data = OMI_data_AOD_1Deg(
        input["year initial"],
        input["year final"],
        input["lon"],
        input["lat"],)
    files = sorted(listdir(input["path data"]))
    data.read_files_he5(files,path=input["path data"],path_HDF=input["path HDF"]+AOD)
    data.calculate_mensual_mean()
    data.fill_empty_data()
    data.reshape()
    data_AOD[AOD+"nm"]=pd.DataFrame(data.data,index=dates)
data_AOD=data_AOD.replace(0,np.nan)
data_AOD.to_csv(dir_data+"AOD_OMI_1.csv")