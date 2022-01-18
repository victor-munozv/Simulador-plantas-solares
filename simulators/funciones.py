import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pvlib
from pvlib import location
from datetime import datetime
################################################################################################
def filter_day_by_year(year, data):
    filter_data = data[['Fecha', 'año', 'Total']]
    filter_data = filter_data.loc[filter_data['año'] == year]
    #filter_data = filter_data.set_index('Fecha')
    filter_data = filter_data[['Fecha','Total']]
    return filter_data
################################################################################################
def plot(x,y,y2,size,save,name_file,color,title,x_label,y_label):
    fig=plt.figure(figsize=size)
    if color == 'none':
        plt.plot(pd.to_datetime(x),y)
    else:
        plt.plot(pd.to_datetime(x),y,c=color)
    
    plt.plot(pd.to_datetime(x),y2)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if save == 'si':
        plt.savefig(name_file+'.'+'png',
                   dpi=400,
                   format='png')
    plt.grid()
    #plt.legend()
    plt.tight_layout()   
    plt.show()
################################################################################################
def get_times_weather(s, loc):
    t = pd.date_range(start=s.iloc[0].name,
                      end=s.iloc[-1].name,
                      freq='1h',
                      tz=loc.tz)
    w = s.copy()
    w = w.reset_index()
    w['date'] = t
    w = w.set_index(pd.DatetimeIndex(w['date']))
    columns = ['ghi','dni','dhi','temp_air', 'wind_speed']
    w = pd.DataFrame(w[columns])
    return t,w
################################################################################################
def weather_solcast(r):
    columns = ['utc_time',
               'DateStart',
               'Periodo',
               'temp_air',
               'cloud_opacity',
               'dhi',
               'dni',
               'ghi',
               'relative_humidity',
               'wind_speed']
    ss = pd.read_csv(r,header=0,names=columns)
    format = '%Y-%m-%d %H:%M:%S'
    ss['utc_time'] = pd.to_datetime(ss['utc_time'],infer_datetime_format=True)
    ss = ss.set_index(pd.DatetimeIndex(ss['utc_time']))
    ss = ss.drop(['utc_time'], axis=1)
    return ss
################################################################################################
def days_of_the_year(array_timestamp):
    days = list(set([str(x)[0:10] for x in array_timestamp]))
    return(days)
################################################################################################
def months_of_the_year(array_timestamp):
    months = list(set([str(x)[0:7] for x in array_timestamp]))
    return(months)
################################################################################################
def get_monthly_axes_from_modelChain_object(model,name):
    class_type = ["<class 'pandas.core.frame.DataFrame'>","<class 'pandas.core.series.Series'>"]
    tp = str(type(model.ac))
    if tp in class_type[0]:
        model = model.ac['i_sc']
    elif tp in class_type[1]:
        model = model.ac
    index_months = months_of_the_year(model.index)
    array_months = np.zeros(len(index_months))
    dict_months = {} 
    for m in index_months:
        dict_months[m] = 0;
    for i in model.index:                                
        m = str(i)[0:7]                             
        if m in index_months:                              
            value_of_record = model.loc[i]        
            dict_months[m] = dict_months[m] + value_of_record      
    ac = sorted(dict_months.items())
    x = []
    y = []  
    for i in ac:
        x.append(i[0])
        y.append(i[1])        
    return x,y  
################################################################################################
def get_daily_axes_from_modelChain_object(model,name):
    #print('Iniciando construcción de registros de ac diarios para:',name)
    class_type = ["<class 'pandas.core.frame.DataFrame'>","<class 'pandas.core.series.Series'>"]
    tp = str(type(model.ac))  
    if tp in class_type[0]:
       #print('1- Es un dataFrame, transformado a serie ...')
        model = model.ac['i_sc']
    elif tp in class_type[1]:
        #print('Es una serie ...')
        model = model.ac      
    #print("2- Extrayendo los dias que tiene la serie de tiempo ...")   
    index_days = days_of_the_year(model.index)
    #print("   Dias encontrados: ", len(index_days))   
    array_days = np.zeros(len(index_days))
    dict_days = {}   
    # prellenamos el diccionario de dias encontrados con ceros
    for d in index_days:
        dict_days[d] = 0;
    #print("3- Agregando valores de ac al diccionario de dias para el sistema ...")
    for i in model.index:                                
        d = str(i)[0:10]                             
        if d in index_days:                              
            value_of_record = model.loc[i]        
            dict_days[d] = dict_days[d] + value_of_record          
    #print("4- Ordenando diccionario")
    ac = sorted(dict_days.items())
    x = []
    y = []  
    #print("5- Generando registros agrupados por dia ...")
    for i in ac:
        x.append(i[0])
        y.append(i[1])        
    #print("Finalizado con éxito. \n")
    return x,y
################################################################################################
def buscador(textos_inversores,textos_modulos):  
    # busca modulos cec y sandia
    nombres_modulos = ['cecmod','sandiamod']
    modulos = [pvlib.pvsystem.retrieve_sam(nombres_modulos[0]),
                     pvlib.pvsystem.retrieve_sam(nombres_modulos[1])]
    arreglo_modulos_cec = []
    for m in modulos[0].columns.values:
        if (textos_modulos[0] in m) and(textos_modulos[1] in m) and (textos_modulos[2] in m):
            arreglo_modulos_cec.append(m)
    arreglo_modulos_sandia = []
    for m in modulos[1].columns.values:
        if (textos_modulos[0] in m) and(textos_modulos[1] in m) and (textos_modulos[2] in m):
            arreglo_modulos_sandia.append(m)            
    # busca inversores cec y sandia
    nombres_inversores = ['cecinverter', 'sandiainverter']
    inversores = [pvlib.pvsystem.retrieve_sam(nombres_inversores[0]),
                     pvlib.pvsystem.retrieve_sam(nombres_inversores[1])]
    arreglo_inversores_cec = []
    for i in inversores[0].columns.values:
        if (textos_inversores[0] in i) and (textos_inversores[1] in i) and (textos_inversores[2] in i):
            arreglo_inversores_cec.append(i)
    arreglo_inversores_sandia = []
    for i in inversores[1].columns.values:
        if (textos_inversores[0] in i) and (textos_inversores[1] in i) and (textos_inversores[2] in i):
            arreglo_inversores_sandia.append(i)
    return {'modulos_cec': arreglo_modulos_cec,'modulos_sandia' : arreglo_modulos_sandia,
           'inversores_cec': arreglo_inversores_cec,'inversores_sandia' : arreglo_inversores_sandia}