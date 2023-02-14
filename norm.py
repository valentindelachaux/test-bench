import math
import pandas as pd
import numpy as np

# [a0,a1,a2,a3,a4,a5,a6,a7,a8]

def to_K(T):
    return T+273.15

def to_C(T):
    return T-273.15

def to_kg_per_s(flow_rate): # hypothèse rho = 1000 g/L 
    return flow_rate/3600

def comp_point_norm(coeff,A_G,m_dot,Cp,G,Gp,T_fluid_in,T_amb,u):
    T_fluid_out = (1/(m_dot*Cp+(A_G/2)*(coeff[1]+coeff[3]*(u-3))))*(A_G*((coeff[0]-coeff[6]*(u-3))*G-(coeff[1]+coeff[3]*(u-3))*(T_fluid_in/2 - T_amb)-coeff[4]*Gp-coeff[7]*(u-3)*Gp)+m_dot*Cp*T_fluid_in)
    return T_fluid_out

def comp_power(m_dot,Cp,T_fluid_out,T_fluid_in):
    return m_dot*Cp*(T_fluid_out-T_fluid_in)

def comp_power_coeff(coeff,A_G,T_fluid_out,G,Gp,T_fluid_in,T_amb,u):
    return A_G*((coeff[0]-coeff[6]*(u-3))*G-(coeff[1]+coeff[3]*(u-3))*((T_fluid_in+T_fluid_out)/2 - T_amb)-coeff[4]*Gp-coeff[7]*(u-3)*Gp)

def find_SK(df,m_dot,A_G):

    tab = pd.DataFrame()

    tab['DT'] = df['T_fluid_out'] - df['T_fluid_in']
    tab['G'] = df['G']
    tab['T_m'] = (df['T_fluid_out'] + df['T_fluid_in'])/2
    tab['T_m - T_a'] = tab['T_m'] - df['T_amb']
    tab['(T_m - T_a)^2'] = tab['T_m - T_a']**2
    tab['up x (T_m - T_a)'] = (df['u'] - 3) * tab['T_m - T_a']
    # tab['Gp/G'] = df['Gp']/df['G']
    tab['Gp'] = df['G'] * 0. # * df['Gp'] à la place de 0 a4
    tab['up x G'] = (df['u'] - 3) * df['G']
    tab['up x Gp'] = (df['u'] - 3) * 0. # df['Gp'] à la place de 0 a7
    tab['(T_m - T_a)^4'] = tab['T_m - T_a']**4 

    tab['T_m en °C'] = tab['T_m']

    coeff_density = [999.85,0.05332,-0.007564,0.00004323,-1.673e-7,2.447e-10]
    coeff_density = list(reversed(coeff_density))

    coeff_c_p = [4.2184,-0.0028218,0.000073478,-9.4712e-7,7.2869e-9,-2.8098e-11,4.4008e-14]
    coeff_c_p = list(reversed(coeff_c_p))

    tab['density(T)'] = np.polyval(coeff_density,tab['T_m en °C'])
    tab['c_p(T)'] = np.polyval(coeff_c_p,tab['T_m en °C'])*1000

    tab['m_dot'] = tab['density(T)']*(m_dot/1000)

    tab['Q_dot'] = tab['m_dot']*tab['c_p(T)']*tab['DT']
    tab['Q_dot / A_G'] = tab['Q_dot']/A_G

    # tab_mat = tab[['G','T_m - T_a','(T_m - T_a)^2','up x (T_m - T_a)','Gp','up x G','up x Gp','(T_m - T_a)^4']]
    tab_mat = tab[['G','T_m - T_a','up x (T_m - T_a)']]

    matrice = tab_mat.to_numpy()
    B = tab['Q_dot / A_G'].to_numpy()

    X=np.linalg.lstsq(matrice, B, rcond = -1)

    return [tab,X]