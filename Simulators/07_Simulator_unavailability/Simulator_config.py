Location = {
    'lat' : -33.5587,
    'long' : -70.87498,
    'tz' : 'America/Santiago',
    'alt' : 401
}

TSM_TEG14 = {
#'BIPV': 'N',              # está en el techo o no
#'Date': '1/1/2018',       # para saber la "depreciación"
#'T_NOCT': 45.1,           # temperatura de operacion
#'A_c': 1.835,             # corriente directa
#'N_s': 72,                # numero de celdas
#'I_sc_ref': 9.14,         # intensida de corto circuito
#'V_oc_ref': 46.9,         # voltaje de circuito abierto
#'I_mp_ref': 8.74,         # corriente de maxima potencia
#'V_mp_ref': 38.2,          # voltaje de maxima potencia
#'alpha_sc': 0.005694,     # coefiente de temperatura del cortocircuito [w]
#'beta_oc': -0.14351,      # coeficiente de temperatura del voltaje
#'a_ref': 1.8746,          # 
#'I_L_ref': 9.233,         #
#'I_o_ref': 0.0,           #
#'R_s': 0.406,             #
#'R_sh_ref': 2746.51,      #
#'Adjust': 9.374,          #
#'gamma_r': -0.41,         #
#'Version': 'NRELv1',      #
#'PTC': 302.8,             #
'gamma_pdc': -0.004,       #-0.36
#'p_mp' : 330,             #
'pdc0': 340,               # potencia del modulo
#'Technology': 'Mono-c-Si'#
 'Name': 'TSM_TEG14'     # name
}

INGETEAM_POWER_TECHNOLOGY_S_A___Ingecon_Sun_1600TL_U_B615_Indoor__450V_ = {
    'pdc': 340,                     #
    'pdc0': 1641550.625,            #entrada limite de CC
    #'eta_inv_nom': 0.96,
    #'eta_inv_ref': 0.9637,
    #"Vac": 6.900000e+02,            # nominal ac voltage
    #"Paco": 1.500000e+06,           #
    #"Pdco": 1.553870e+06,           #
    #"Vdco": 7.460000e+02,           #
    #"Pso": 6.610500e+03,            # 20, se mide en watts
    #"C0": -1.716470e-08,            #
    #"C1": -4.558320e-05,            #
    #"C2": -4.476540e-04,            #
    #"C3": -1.059060e-03,            #
    #"Pnt": 4.301000e+02,            #
    #"Vdcmax": 8.000000e+02 ,        #
    #"Idcmax": 2.082930e+03,         #
    #"Mppt_low": 5.850000e+02,       # la entrada minima de voltaje por entrada de mppt
    #"Mppt_high": 8.000000e+02,      # 
    "Name": "INGETEAM_POWER_TECHNOLOGY_S_A___Ingecon_Sun_1600TL_U_B615_Indoor__450V_" 
}

System = {
    'azimuth': 90,
    'tilt': 20,
    'm_p_s': 20,    #20
    's_p_i': 221    #288 #126
}
