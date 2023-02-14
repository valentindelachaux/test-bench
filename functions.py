import math
import copy
import pandas as pd
import numpy as np
import datetime

import norm as nm

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import h5py
import tables

import os


# BTP
def dict_preproc_btp():

    # Dictionnaire de renommage VBus-Dataframe
    dict_rename_btp = {'Date / Time':'Datetime', 'T out PVT1 [ °C]':'T_out_PVT1', 'T bas ballon [ °C]':'T_tank_bottom', 'T in PVT1 [ °C]':'T_in_PVT1', 'T haut ballon [ °C]':'T_tank_top', 'T out PVT2 [ °C]':'T_out_PVT2', 'T in PVT2 [ °C]':'T_in_PVT2', 'T out PVT3 [ °C]':'T_out_PVT3', 'T in PVT3 [ °C]':'T_in_PVT3', 'T out PVT4 [ °C]':'T_out_PVT4', 'T in PVT4 [ °C]':'T_in_PVT4', 'T out PVT5 [ °C]':'T_out_PVT5', 'T in PVT5 [ °C]':'T_in_PVT5', 'Irradiation solaire [ W/m²]':'G', 'T out PVT6 [ °C]':'T_out_PVT6', 'T in PVT6 [ °C]':'T_in_PVT6', 'T extérieure [ °C]':'T_amb', 'T out PVT7 [ °C]':'T_out_PVT7', 'T in PVT7 [ °C]':'T_in_PVT7', 'T out PVT8 [ °C]':'T_out_PVT8', 'T in PVT8 [ °C]':'T_in_PVT8', 'T out PVT9 [ °C]':'T_out_PVT9', 'T in PVT9 [ °C]':'T_in_PVT9', 'T out PVT10 [ °C]':'T_out_PVT10', 'T in PVT10 [ °C]':'T_in_PVT10', 'Pression entrée PVT [ bar]':'P_in', 'Pression sortie PVT [ bar]':'P_out', 'T entrée PVT RPS [ °C]':'T_fluid_in', 'T sortie PVT RPS [ °C]':'T_fluid_out', 'T sortie PVT VFD [ °C]':'T_fluid_out_VFD', 'Débit VFD [ l/h]':'Flow_rate', 'débit IMP [ l/h]':'Flow_rate_IMP', 'Relais 1 [ %]':'Relais_1', 'Signal PWM [ %]':'PWM_signal', 'Vitesse du vent [ m/s]':'u'}
    # Ordre des colonnes
    order_btp = ['Datetime','G','T_amb','u','Flow_rate','Flow_rate_IMP','T_fluid_in','T_fluid_out','T_fluid_out_VFD','T_tank_bottom','T_tank_top','P_in','P_out','Relais_1','PWM_signal']
    # Unités des colonnes
    dict_unit_btp = {'Datetime':'datetime', 'T_out_PVT1':'°C', 'T_tank_bottom':'°C', 'T_in_PVT1':'°C', 'T_tank_top':'°C', 'T_out_PVT2':'°C', 'T_in_PVT2':'°C', 'T_out_PVT3':'°C', 'T_in_PVT3':'°C', 'T_out_PVT4':'°C', 'T_in_PVT4':'°C', 'T_out_PVT5':'°C', 'T_in_PVT5':'°C', 'G':'W/m2', 'T_out_PVT6':'°C', 'T_in_PVT6':'°C', 'T_amb':'°C', 'T_out_PVT7':'°C', 'T_in_PVT7':'°C', 'T_out_PVT8':'°C', 'T_in_PVT8':'°C', 'T_out_PVT9':'°C', 'T_in_PVT9':'°C', 'T_out_PVT10':'°C', 'T_in_PVT10':'°C', 'P_in':'bar', 'P_out':'bar', 'T_fluid_in':'°C', 'T_fluid_out':'°C', 'T_fluid_out_VFD':'°C', 'Flow_rate':'L/h', 'Flow_rate_IMP':'L/h', 'Relais_1':'%', 'PWM_signal':'%', 'u':'m/s'}

    return dict_rename_btp,order_btp,dict_unit_btp

# PVT-PAC
def dict_preproc_pvtpac():

    # Dictionnaire de renommage VBus-Dataframe
    dict_rename_pvtpac = {'Date / Time': 'Date / Time',
    'T départ PAC (circuit captage) [ °C]': 'T_HP_outlet_HS',
    'T retour solaire [ °C]': 'T_PVT_inlet',
    'T extérieure [ °C]': 'T_amb',
    'T PVT [ °C]': 'T_PVT',
    'T départ solaire [ °C]': 'T_PVT_outlet',
    'T retour PAC (circuit captage) [ °C]': 'T_HP_inlet_HS',
    'T bas de ballon ECS [ °C]': 'T_DHW_tank_bottom',
    'T haut de ballon ECS [ °C]': 'T_DHW_tank_top',
    'T retour vers le solaire du bas de ballon (Décharge ECS) [ °C]': 'T_DHW_PVT_outlet',
    'T entrée EF (ballon ECS) [ °C]': nan,
    'T départ solaire vers le bas de ballon (décharge ECS) [ °C]': 'T_DHW_PVT_inlet',
    'T départ PAC (circuit ECS) [ °C]': 'T_DHW_HP_inlet',
    'T départ PAC (circuit chauffage) [ °C]': 'T_SH_inlet',
    'T retour AU06 (AI12) [ °C]': 'T_air_source_inlet',
    'T départ AU06 [ °C]': 'T_air_source_oulet',
    'Signal PAC - MX  [ °C]': 'HP_MX_signal',
    'Irradiation CS10 [ W/m²]': 'G_CS10',
    'T retour PAC (circuit ECS) [ °C]': 'T_DHW_HP_outlet',
    'T sortie ECS (ballon ECS) [ °C]': 'T_HP_inlet_SH',
    'T retour PAC (circuit chauffage) [ °C]': 'T_SH_outlet',
    'Débit solaire [ l/h]': 'Vdot_PVT',
    'Débit circuit captage PAC [ l/h]': 'Vdot_HS',
    'Débit AU06 [ l/h]': 'Vdot_AS',
    'Débit PAC (circuit ECS) [ l/h]': 'Vdot_DHW',
    'Débit tirage ECS [ l/h]': 'Vdot_HW_tap',
    'Débit PAC (circuit chauffage) [ l/h]': 'Vdot_SH_outlet',
    'Volume au total CAL 1 [ l]': 'E_HP',
    'Vitesse circulateur décharge ECS [ %]': 'Circ_speed_DHW_disch',
    'Etat V3V décharge ECS [ %]': 'V3V_state_DHW_disch',
    'Sortie A [ %]': 'signal_circ_DHW_disch',
    'Conso Elec de la PAC [ W]': 'P_HP_elec',
    'DeltaT PVT [ °C]': 'DT_PVT',
    "Humidité de l'air [ %]": 'air_humidity',
    'Delta T ext-PVT [ °C]': 'DTambPVT',
    'Prod Solaire [ W]': 'P_solar',
    'Prod captage [ W]': 'P_HS',
    'Prod AU06 [ W]': 'P_AS',
    'Prod chauffage [ W]': 'P_SH',
    'Prod ECS [ W]': 'P_DHW'}

    order = {}
    dict_unit = {}
    
    return dict_rename_pvtpac,order,dict_unit


#  Cette fonction récupère un fichier VBus dans le dossier et retourne un pd.DataFrame
def pre_proc(file_name): #
    path = os.getcwd()
    pathout = path+'\\VBus_data\\'
    data_file = pathout+file_name
    res = pd.read_csv(data_file, delimiter=";",encoding="utf-8", header=1)
    return res

# Cette fonction répare la colonne "Date / Time"
def clean_date_time(df,str):
    # Ajuste le Date/Time

    df[str] = df[str].apply(lambda dat: dat[0:6]+dat[8:10]+" "+dat[11:])
    df[str] = df[str].apply(lambda dat: datetime.datetime.strptime(dat, '%m/%d/%y %H:%M:%S'))

    # Crée deux colonnes, une pour la date et une pour le time

    # df.insert(loc = 1,
    #         column = 'Date',
    #         value = df[str].apply(lambda dat: datetime.datetime.date(dat)))

    # df.insert(loc = 2,
    #         column = 'Time',
    #         value = df[str].apply(lambda dat: datetime.datetime.time(dat)))

    return df

# Cette fonction supprime les colonnes qui n'ont pas de donnéee et retourne le dataframe
def drop(df):

    column_headers = list(df.columns.values)
    print('tous les noms des colonnes',column_headers)

    to_drop = []

    for i in range(len(column_headers)):
        first_value = df[column_headers[i]][0]
        if first_value == 888.8 or first_value == 999.9:
            to_drop.append(column_headers[i])
        else:
            pass

    print('colonnes à droper',to_drop)

    df = df.drop(columns=to_drop)

    return df

# Cette fonction renomme les colonnes avec les clés indiquées dans dict, et remet les colonnes dans l'ordre 
def rename_and_sort(df,dict,order):

    column_headers = list(df.columns.values)

    for i in range(len(column_headers)):
        head = column_headers[i]
        if dict[head]!=0:
            df.rename(columns = {head:dict[head]}, inplace = True)

    df = df[order]

    return df

def select(df, start_datetime,end_datetime):
    dfbis = df.loc[df['Datetime']>=start_datetime]
    dfter = dfbis.loc[dfbis['Datetime']<=end_datetime]
    return dfter

def save_h5(address,df,dict_unit): # address = file.h5 
    # c'est une procédure, ça crée carrément le fichier .h5

    # Crée le fichier

    columns_headers = list(df.columns.values)
    f = h5py.File(address, "w")
    f.close()

    # Transfère le dataframe dans le HDF5

    index_to_hdf5 = [0,1,4,13,15]
    groups = ["","Meteo","System","Control"]

    for i in range(len(index_to_hdf5)-1):
        for name in columns_headers[index_to_hdf5[i]:index_to_hdf5[i+1]]:
            if name!='Date' and name!='Time':
                df[name].to_hdf(address,key="/"+groups[i]+"/"+name,mode="r+")

    # Ajouter les attributs "Unit"

    f = h5py.File(address, "r+")
    grp_list = list(f.keys())
    for grp in grp_list:
        if grp!='Datetime':
            columns_list = list(f['/'+grp].keys())
            for col in columns_list:
                    f['/'+grp+'/'+col+'/values'].attrs['Unit'] = dict_unit[col]

    f.close()

def read_h5(address,order):
    df_again = pd.read_hdf(address,key="/Datetime")

    grp_list = list(h5py.File(address, "r").keys())
    for grp in grp_list:
        if grp!='Datetime':
            columns_list = list(h5py.File(address, "r")['/'+grp].keys())
            for col in columns_list:
                df_again = pd.concat((df_again,pd.read_hdf(address,key='/'+grp+'/'+col)),axis=1)

    df_again = df_again[order]

    return df_again


def find_steady_states(df):

    # coeff_S375SB = [0.4419,19.65,0.,1.85,0.,20.8,0.0180,0.]
    coeff_S425 = [0.382,16.64,0.,0.838,0.,0.,0.0129,0.]

    df_t = df

    nb_dots = 15

    dev_G = 50
    dev_T_amb = 0.5
    dev_u = 0.3
    dev_T_fluid_in = 0.05
    dev_T_fluid_out = 0.05
    tol_T_fluid_in = 2/100
    tol_T_fluid_out = 2/100

    quasi_list = []
    time_list = []
    flag = 0

    ss_list = []

    VFD = 0

    test_VFD = True


    for i in range(len(df_t)):
        flag = 0
        
        cop = df_t.iloc[i:i+nb_dots,:]
        fr_mn = cop['Flow_rate'].mean()
        G_mn = cop['G'].mean()
        T_amb_mn = cop['T_amb'].mean()
        u_mn = cop['u'].mean()
        T_fin_mn = cop['T_fluid_in'].mean()

        if test_VFD == True:
            T_fout_mn = cop['T_fluid_out_VFD'].mean()
            T_fout_mn_nVFD = cop['T_fluid_out'].mean()
            T_fout_mn_VFD = T_fout_mn
        else:
            T_fout_mn = cop['T_fluid_out'].mean()
            T_fout_mn_VFD = cop['T_fluid_out_VFD'].mean()
            T_fout_mn_nVFD = T_fout_mn

        ind = cop.index

        for j in range(len(cop)):
            jp = ind[j]
            dif_G = abs(cop.loc[jp,'G'] - G_mn)
            dif_T_amb = abs(cop.loc[jp,'T_amb'] - T_amb_mn)
            dif_u = abs(cop.loc[jp,'u'] - u_mn)
            dif_T_fin = abs(cop.loc[jp,'T_fluid_in'] - T_fin_mn)
            if test_VFD == True:
                dif_T_fout = abs(cop.loc[jp,'T_fluid_out_VFD'] - T_fout_mn)
            else:    
                dif_T_fout = abs(cop.loc[jp,'T_fluid_out'] - T_fout_mn)
            
        
            # if dif_G<=dev_G and dif_T_amb<=dev_T_amb and dif_u <= dev_u and dif_T_fin <= tol_T_fluid_in*T_fin_mn and dif_T_fout <= tol_T_fluid_out*T_fout_mn:
            if dif_G<=dev_G and dif_T_amb<=dev_T_amb and dif_u <= dev_u and dif_T_fin <= dev_T_fluid_in and dif_T_fout <= dev_T_fluid_out :
                # if  dif_T_fout_VFD <= dev_T_fluid_out:
                #     flag+=1
                # else:
                #     VFD+=1
                #     break
                flag+=1
        
        if flag==nb_dots:
            print("steady")
            quasi_list.append(ind)
            time_list.append(cop['Datetime'])
            pow_meas = nm.comp_power(nm.to_kg_per_s(fr_mn),Cp,T_fout_mn,T_fin_mn)
            pow_sk = nm.comp_power_coeff(coeff_S425,2.08,T_fout_mn,G_mn,0.,T_fin_mn,T_amb_mn,u_mn)
            err = (pow_meas-pow_sk)/pow_sk

            ss_list.append([df_t.loc[df_t.index[i],'Datetime'],fr_mn,G_mn,T_amb_mn,u_mn,T_fin_mn,T_fout_mn_nVFD,T_fout_mn_VFD,pow_meas,pow_sk,err])
        else:
            pass

    return time_list,quasi_list,ss_list


def plot_system(df,tank=False):

    # Create figure with secondary y-axis
    fig = go.Figure()

    # Add traces
    fig.add_trace(
        go.Scatter(x=df['Datetime'], y=df['T_fluid_in'], name="T_fluid,in",line=dict(color="#0000ff"))
    )

    fig.add_trace(
        go.Scatter(x=df['Datetime'], y=df['T_fluid_out'], name="T_fluid,out",line=dict(color='#ff0000'))
    )

    if tank==True:
            fig.add_trace(
                go.Scatter(x=df['Datetime'], y=df['T_tank_bottom'], name="T_tank bottom",line=dict(color="#778899"))
            )

            fig.add_trace(
                go.Scatter(x=df['Datetime'], y=df['T_tank_top'], name="T_tank top",line=dict(color="#ee82ee"))
            )


    fig.add_trace(
        go.Scatter(x=df['Datetime'], y=df['Flow_rate'], name="Débit (L/h)",line=dict(color='#00ff00'),
        yaxis="y2")
    )

    # Create axis objects
    fig.update_layout(

        xaxis=dict(
            domain=[0.1, 0.95]                 #Sets the domain of this axis (in plot fraction). Play with the numbers to see how it affects the plot
        ),
        
        yaxis=dict(
            title="Temperature (°C)",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            )
        ),
        yaxis2=dict(
            title="Flow rate (L/h)",
            anchor="x",     # specifying x - axis has to be the fixed
            overlaying="y",  # specifyinfg y - axis has to be separated
            side="right"
        ),
    )


    # Set x-axis title
    fig.update_xaxes(title_text="Time")


    # Update layout properties
    fig.update_layout(
        title_text="System",
    )

    fig.update_layout(
        autosize=False,
        width=2000,
        height=500,
        margin=dict(
            l=0,
            r=0,
            b=50,
            t=50,
            pad=1
        ),
    )

    # changing orientation of the legend
    fig.update_layout(legend=dict(
        orientation="h",
    
    ))

    return fig

def plot_meteo(df):
    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(x=df['Datetime'], y=df['u'], name="Wind (m/s)",
        )
    )

    fig2.add_trace(
        go.Scatter(x=df['Datetime'], y=df['G'], name="G (W/m2)",
        yaxis='y2')
    )

    fig2.add_trace(
        go.Scatter(x=df['Datetime'], y=df['T_amb'], name="Ambient temperature (°C)",
    yaxis='y3')
    )


    fig2.update_layout(
        xaxis=dict(
            domain=[0.1, 0.95]                 #Sets the domain of this axis (in plot fraction). Play with the numbers to see how it affects the plot
        ),

            yaxis=dict(
            title="Wind (m/s)",
        ),
            yaxis2=dict(
            title="G (W/m2)",
            anchor="free",  # specifying x - axis has to be the fixed
            overlaying="y",  # specifyinfg y - axis has to be separated
            side="left",  # specifying the side the axis should be present
            position=0.05
        ),

            yaxis3=dict(
            title="Ambient temperature (°C)",
            anchor="x",  # specifying x - axis has to be the fixed
            overlaying="y",
            side="right",  # specifying the side the axis should be present
        ),
    )

    fig2.update_layout(
        autosize=False,
        width=2000,
        height=500,
        margin=dict(
            l=0,
            r=0,
            b=50,
            t=50,
            pad=1
        ),
    )

    fig2.update_xaxes(title_text="Time")

    # changing orientation of the legend
    fig2.update_layout(legend=dict(
        orientation="h",
    
    ))

    return fig2

