import numpy as np
import math 
import os
#<-------------------------Funcion que le da el formato a SMARTS------------------------>
def escribir(lon_i,lon_f,day,month,year,hour,ozono,aod):
    file=open("data.inp.txt","w")
    file.write(" 'AOD="+str(aod)+"'\n")
    file.write(" 2\n")
    file.write(" 25.750 0.512 0\n")
    file.write(" 1\n")
    file.write(" 'USSA'\n")
    file.write(" 1\n")
    file.write(" 0\n")
    file.write(" 1 "+str(round(ozono/1000,4))+"\n")
    #<-------------------------Card 6------------------>
    file.write(" 0\n")
    #<-------------------------Card 6a----------------->
    file.write(" 3\n")
    file.write(" 390\n")
    file.write(" 0\n")
    file.write(" 'S&F_URBAN'\n")
    file.write(" 5\n")
    file.write(" "+str(aod)+" 2\n")
    file.write(" 18\n")
    file.write(" 1\n")
    file.write(" 51 37. 180.\n")
    file.write(" "+str(lon_i)+" "+str(lon_f)+" 1 1366.1\n")
    file.write(" 2\n")
    file.write(" "+str(lon_i)+" "+str(lon_f)+" 1\n")
    file.write(" 1\n")
    file.write(" 4\n")
    file.write(" 1\n")
    file.write(" 0 2.9 0\n")
    file.write(" 0\n")
    file.write(" 0\n")
    file.write(" 1\n")
    file.write(" 3\n")
    file.write(" "+str(year)+" "+str(month)+" "+str(day)+" "+str(hour)+" 25.75 -100.25 -6\n")
    file.close()
def writeAOD(date,year,month,day,o3,aod,DR):
    AOD_file.write(str(int(date))+" "+str(year)+" "+str(month)+" "+str(day)+" "+str(o3)+" " 
    +str(round(aod,3))+" "+str(round(DR,2))+"\n")
#<----------------------------Lectura de los datos de entrada--------------------------------------->
car="../../Stations/"
stations=["noreste"]
DR_lim,aod_i=7,0.025
#<------------------------Hora inicial y final del calculo-------------------------->
hour_i,hour_f=11,14
#<---------------------Longitud inicial y final del calculo---------------------->
lon_i,lon_f=285,2800
#<---------------------------Diferencia de horas y longitudes de onda------------------->
dl_i=lon_i-280+1;dh=(hour_f-hour_i);n_min=dh*60
for station in stations:
    print("Calculando estacion "+station)
    carp=car+station
    AOD_file=open(carp+"/DataAOD.txt","w")
    data=np.loadtxt(carp+"/datos.txt")
    date,day,month,year,o3=data[:,0],data[:,1],data[:,2],data[:,3],data[:,4];del data
    n=np.size(year)
    #<-----------------------------Ciclo para variar los dias--------------------------------------->
    for i in range(n):
        data=np.loadtxt(carp+"/Mediciones/"+str(int(date[i]))+".txt",skiprows=hour_i)
        data=np.max(data[0:dh,1])
        year_i,month_i,day_i,o3_i=int(year[i]),int(month[i]),int(day[i]),o3[i]
        if year_i!=2014:
            print("           Calculando el dia ",year_i,month_i,day_i)
            #<------------------------------Valores iniciales------------------------------------------->
            aod,var,k=aod_i,False,1
            while var==False and k<32:
                resul=np.zeros(n_min)
                for min in range(n_min):
                    escribir(lon_i,lon_f,day_i,month_i,year_i,round(hour_i+min/60,4),o3_i,aod)
                    os.system("./smarts.out")
                    mod=np.loadtxt("data.ext.txt",skiprows=dl_i)
                    sum=0
                    size=np.size(mod[:,0])
                    for lon in range(size):
                        if lon==0:
                            sum+=mod[lon,1]
                        else:
                            sum+=mod[lon,1]*(mod[lon,0]-mod[lon-1,0])
                    resul[min]=sum
                    os.system("rm data*")
                #<-------------------------Posicion del valor mas alto------------------------------------>
                pos=(np.where(np.max(resul)==resul)[0])[0]
                #<-----------------------Promedio de datos minuto a minuto------------------------------>
                data_mod=np.mean(resul[pos-30:pos+31])
                DR=100*(data_mod-data)/data
                if abs(DR)<DR_lim: 
                    writeAOD(date[i],year_i,month_i,day_i,o3_i,aod,DR)
                    var=True
                else:
                    if DR<0:
                        writeAOD(date[i],year_i,month_i,day_i,o3_i,aod,DR)
                        var=True
                    else:
                        aod+=0.025
                k+=1