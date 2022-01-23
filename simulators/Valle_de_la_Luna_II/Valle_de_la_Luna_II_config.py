Location = {
    'lat' : -25.4065,
    'long' : -70.4803,
    'tz' : 'America/Santiago',
    'alt' : 46
}

JAM60S03 = {
'BIPV': 'N',              # está en el techo o no
'Date': '1/1/2018',       # para saber la "depreciación"
'T_NOCT': 45,             # temperatura de operacion
'A_c': 2.0,               # corriente directa
'N_s': 72,                # numero de celdas
'I_sc_ref': 10.22,        # intensida de corto circuito
'V_oc_ref': 40.56,        # voltaje de circuito abierto
'I_mp_ref': 9.66,         # corriente de maxima potencia
'V_mp_ref': 33.65,        # voltaje de maxima potencia
'alpha_sc': 0.051,        # coefiente de temperatura del cortocircuito [w]
'beta_oc': -0.289,        # coeficiente de temperatura del voltaje
'a_ref': 1.842,           # 
'I_L_ref': 9.207,         #
'I_o_ref': -0.0,          #
'R_s': 0.42,              #
'R_sh_ref': 732.18,       #
'Adjust': 5.86,           #
'gamma_r': -0.41,         #
#'Version': 'NRELv1',     #
#'PTC': 368.4,            #
'gamma_pdc': -0.36,       #
'pdc0': 325,              # potencia del modulo
#'Technology': 'Mono-c-Si'
 'Name': 'JAM60S03'
}

MV_Power_Station_1600SC = {
    #"Vac": ,            # nominal ac voltage
    "Paco": 1.760e+06,   #
    "Pdco": 1.796e+06,   #
    "Vdco": 1.0e+03,     #
    "Pso": 3.235010e+03, # 20, se mide en watts
    "C0": 0.0,           #
    "C1": 0.000017,      #
    "C2": 0.002165,      #
    "C3": 0.000719,
    "Pnt": 222.6,
    #"Vdcmax": ,
    #"Idcmax": ,
    "Mppt_low": 500,     # la entrada minima de voltaje por entrada de mppt
    "Mppt_high": 530,    # 
    "Name": "MV_Power_Station_1600SC" 
}

System = {
    'azimuth': 0,
    'tilt': 10,
    'm_p_s': 20, #126
    's_p_i': 140   #20
}
