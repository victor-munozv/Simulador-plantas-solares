import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pvlib
from pvlib import location
from datetime import datetime

################################################################################################
def data_to_pickle(path,name,ext='xlsx'):
    pickle = '.pickle'
    path_name_ext = path+name+'.'+ext
    path_name_picke = path+name+pickle
    error = ['ERROR1: pickle NOT found in path:',
             'ERROR2:','NOT found in:',
             'ERROR3: The picke could NOT be generated in:',
             'ERROR4: Pickle read failed']
    try:
        p = pd.read_pickle(path_name_picke)
        print('Pickle found in:',path_name_picke)
        print('Returning data')
        return p
    except:
        print(error[0],path_name_picke)
        try:
            print('- Tried to read file:',path_name_ext)
            if (ext == 'xlsx'):
                file = pd.read_excel(path_name_ext)
            if (ext == 'csv'):
                file = pd.read_csv(path_name_ext)
            print('    Read file')
            try:
                print('- Trying to generate pickle')
                file.to_pickle(path_name_picke)
                print('    Pickle generated')
                try:
                    print('- Trying to read generated pickle')
                    p = pd.read_pickle(path_name_picke)
                    print('    Pickle read on: ',path_name_picke)
                    print('Returning data')
                    return p
                except:
                    print(eror[4])
            except:
                print(error[3],path_name_picke)       
        except:
            print(error[1],ext,error[2],path_name_ext)
################################################################################################
def filter_hour_from_dataFrame(data=None,
                               names_pv=[], 
                               columns_names=[],
                               column_fecha=None,
                               column_central=None, 
                               first_year=None, 
                               last_year=None,
                               months = [1,2,3,4,5,6,7,8,9,10,11,12],
                               multi = 1,
                               p = False): 
    if not isinstance(data, pd.DataFrame):
        print('ERROR1: Data is not a',pd.DataFrame)
        print('        It is type:',str(type(data)))
        return
    if not isinstance(names_pv, list):
        print('ERROR2: names_pv is not a list')
        return
    elif len(names_pv) == 0:
        print('ERROR3: Names of photovoltaic systems not found')
        print('        List empty')
        return
    if columns_names == []:
        columns_names = ['Hora 1','Hora 2','Hora 3','Hora 4','Hora 5','Hora 6','Hora 7','Hora 8','Hora 9',
                         'Hora 10','Hora 11','Hora 12','Hora 13','Hora 14','Hora 15','Hora 16','Hora 17','Hora 18',
                         'Hora 19','Hora 20','Hora 21','Hora 22','Hora 23','Hora 24']
        print('- Using default ',columns_names,'for columns_names \n')      
    if column_fecha == None:
        column_fecha = 'Fecha'
        print('- Using default',column_fecha,'for column_fecha \n')      
    if column_central == None:
        column_central = 'Central'
        print('- Using default',column_central,'for column_central \n') 
    if first_year == None:
        first_year = 0;
        print('- Using default',first_year,'for first_year \n')
    if last_year == None:
        last_year = 10000;
        print('- Using default',last_year,'for last_year \n')
    systems = {}
    for pv in names_pv:
        systems[pv] = {}
    hours = columns_names
    for pv in systems:                                     # para cada sistema
        filter_data = data.loc[data[column_central] == pv] # se filtra la data para el sistema dado
        for i in range(len(filter_data.iloc[:])):          # para cada registro del sistema
            log = filter_data.iloc[i]                      # extraer el regitro
            date = log[column_fecha]                       # extraer la fecha de cada registro
            year = int(date.split('-')[0])
            month = int(date.split('-')[1])
            if (year >= first_year ) and (year <= last_year) and month in months:
                date_rng = pd.date_range(start=date, freq='H', periods= 24)# crear un arreglo de 'fechas por hora'  
                for h in hours:                                      # para cada hora
                    value = log[h]                                   # extraer el valor del registro para la hora espesificada
                    hour = [int(temp)for temp in h.split() if temp.isdigit()][0]
                    hour_id = int(hour)-1                           # extraer la hora espesificada como id del arreglo de horas
                    date_by_hour = date_rng[hour_id]                # obtener la fecha del arreglo de 'fechas por hora'
                    systems[pv][date_by_hour] = value*multi         # guardar el valor en la 'fecha por hora' correspondiente
                    if p:
                        print('pv:',pv,'year:',year,'Hour:',h,'Date:',date_by_hour,'value:',systems[pv][date_by_hour])
            else:
                continue
    return systems
################################################################################################
def filter_day_from_dataFrame(data=None,
                              names_pv=None,
                              column_fecha=None,
                              column_total=None, 
                              column_central=None, 
                              first_year=None, 
                              last_year=None,
                              months = [1,2,3,4,5,6,7,8,9,10,11,12],
                              multi = 1,
                              p = False): 
    if not isinstance(data, pd.DataFrame):
        print('ERROR1: Data is not a',pd.DataFrame)
        print('        It is type:',str(type(data)))
        return
    if not isinstance(names_pv, list):
        print('ERROR2: names_pv is not a list')
        return
    elif len(names_pv) == 0:
        print('ERROR3: Names of photovoltaic systems not found')
        print('        List empty')
        return
    if column_fecha == None:
        column_fecha = 'Fecha';
        print('- Using default',column_fecha,'for column_fecha \n')
    if column_total == None:
        column_total = 'Total'
        print('- Using default',column_total,'for column_total \n')         
    if column_central == None:
        column_central = 'Central'
        print('- Using default',column_central,'for column_central \n')   
    if first_year == None:
        first_year = 0;
        print('- Using default',first_year,'for first_year \n')
    if last_year == None:
        last_year = 10000;
        print('- Using default',last_year,'for last_year \n')
    systems = {}
    for pv in names_pv:
        systems[pv] = {}
    for pv in systems:                                     # para cada sistema
        filter_data = data.loc[data[column_central] == pv] # se filtra la data para el sistema dado
        for i in range(len(filter_data.iloc[:])):          # para cada registro del sistema
            log = filter_data.iloc[i]                      # extraer el regitro
            date = log[column_fecha]                       # extraer la fecha de cada registro
            year = int(date.split('-')[0])
            month = int(date.split('-')[1])
            if (year >= first_year ) and (year <= last_year) and month in months:
                date_rng = pd.date_range(start=date,end=date, freq='D')  # crear un arreglo de 'fechas por dia'
                value = log[column_total] * multi                        # obtener el valor diario
                systems[pv][date_rng[0]] = value                         # guardar el valor en la 'fecha por dia' correspondiente
                if p:
                    print('pv:',pv,'year:',year,'Date',date_rng[0],'value',systems[pv][date_rng[0]])
            else:
                continue
    return systems
################################################################################################
def filter_month_from_dataFrame(data=None,
                                names_pv=None,
                                column_fecha=None,
                                column_total=None, 
                                column_central=None, 
                                first_year=None, 
                                last_year=None,
                                months = [1,2,3,4,5,6,7,8,9,10,11,12],
                                p = False): 

    if not isinstance(data, pd.DataFrame):
        print('ERROR1: Data is not a',pd.DataFrame)
        print('        It is type:',str(type(data)))
        return
    if not isinstance(names_pv, list):
        print('ERROR2: names_pv is not a list')
        return
    elif len(names_pv) == 0:
        print('ERROR3: Names of photovoltaic systems not found')
        print('        List empty')
        return
    if column_fecha == None:
        column_fecha = 'Fecha';
        print('- Using default',column_fecha,'for column_fecha \n')
    if column_total == None:
        column_total = 'Total'
        print('- Using default',column_total,'for column_total \n')         
    if column_central == None:
        column_central = 'Central'
        print('- Using default',column_central,'for column_central \n')   
    if first_year == None:
        first_year = 0;
        print('- Using default',first_year,'for first_year \n')
    if last_year == None:
        last_year = 10000;
        print('- Using default',last_year,'for last_year \n')
    systems = {}
    for pv in names_pv:
        systems[pv] = {}
    for pv in systems:                                     # para cada sistema
        filter_data = data.loc[data[column_central] == pv] # se filtra la data para el sistema dado
        for i in range(len(filter_data.iloc[:])):          # para cada registro del sistema
            log = filter_data.iloc[i]                      # extraer el regitro
            date = log[column_fecha]                       # extraer la fecha de cada registro
            year = int(date.split('-')[0])
            month = int(date.split('-')[1])
            if (year >= first_year ) and (year <= last_year) and month in months:
                f = str(year)+'-'+str(month)
                #date_rng = pd.period_range(start=f, end=f, freq='M')
                value = log[column_total]                     # obtener el valor diario
                try:
                    systems[pv][f] = systems[pv][f] + value
                except:
                    systems[pv][f] = value 
                if p:
                    print('pv:',pv,'year:',year,'Date',f,'value',systems[pv][f])
            else:
                continue
    return systems
################################################################################################
def graph(data=None,x_label= 'Year [ ]',y_label='Power [MW/ ]',name=None):
    if not isinstance(data, dict):
        print('ERROR1: Data is not a',dict)
        print('        It is type:',str(type(data)))
        return
    if name == None:
        print('ERROR2: Name not defined')
        return
    
    for pv in data:
        print(pv,'len:',len(data[pv]))
        pv_series = pd.Series(data=data[pv])
        plt.figure(figsize=(12,6))
        plt.plot(pv_series,label=pv)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.grid()
        plt.title(pv)
        plt.savefig(pv+'_'+name+'.png',dpi=400)
        plt.show()
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
################################################################################################
def filter_day_by_year(year, data):
    filter_data = data[['Fecha', 'año', 'Total']]
    filter_data = filter_data.loc[filter_data['año'] == year]
    #filter_data = filter_data.set_index('Fecha')
    filter_data = filter_data[['Fecha','Total']]
    return filter_data
################################################################################################
def plot_2(x,y,y2,size,save,name_file,color,title,x_label,y_label):
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
    plt.legend()
    plt.tight_layout()   
    plt.show()
################################################################################################
def plot_1(x,y,size,save,name_file,color,title,x_label,y_label):
    fig=plt.figure(figsize=size)
    if color == 'none':
        plt.plot(pd.to_datetime(x),y)
    else:
        plt.plot(pd.to_datetime(x),y,c=color)
    
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
def get_times_weather(s, loc, c):
    print('primer dia',s.iloc[0].name)
    print('ultimo dia',s.iloc[-1].name)
    t = pd.date_range(start=s.iloc[0].name,
                      end=s.iloc[-1].name,
                      freq='1h',
                      tz=loc.tz)
    w = s.copy()
    w = w.reset_index()
    w['date'] = t
    w = w.set_index(pd.DatetimeIndex(w['date']))
    w = pd.DataFrame(w[c])
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
def weather_solcast_2(r):
    columns = ['utc_time',
               'DateStart',
               'Periodo',
               'temp_air',
               'azimuth',
               'cloud_opacity',
               'dhi',
               'dni',
               'ebh',
               'ghi',
               'relative_humidity',
               'wind_speed',
               'zenith']
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