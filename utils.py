import yaml
from yaml.loader import FullLoader
from yaml.loader import SafeLoader
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def sort_curve(curve):
    sorted_curve = np.zeros(np.shape(curve))
    ind = np.argsort(curve, axis=0)
    for i in range(len(curve)):
        sorted_curve[i,0]= curve[ind[i,0],0]
        sorted_curve[i,1]= curve[ind[i,0],1]
    return sorted_curve


def curve_filter(lit_data,
                 Temperature_C='any', 
                 Strain_rate='any', 
                 microstructure='any', 
                 heater='any',
                 sample_diameter='any',
                 sample_length='any'):
    no_curves = 0
    curve_list = []
    Paper_list =[]
    Author_list =[]
    for paper in lit_data['Papers'].keys():
        for curve in lit_data['Papers'][paper]['Curves']:
            temp_bool = curve['Temperature_C'] == Temperature_C or Temperature_C == 'any'
            strain_bool = curve['Strain_rate_s-1'] == Strain_rate or Strain_rate =='any'
            micro_bool = curve['microstructure_type'] == microstructure or microstructure == 'any'
            heat_bool = curve['In_situ_heating'] == heater or heater == 'any'
            diameter_bool = curve['sample_diameter_mm'] == sample_diameter or sample_diameter == 'any'
            length_bool = curve['sample_length_mm'] == sample_diameter or sample_diameter =='any'
            if temp_bool & strain_bool & micro_bool & diameter_bool & length_bool:
                flow_curve = np.loadtxt('Flow_curves/'+curve['Curve_location'], delimiter=",")
                flow_curve = sort_curve(flow_curve)
                curve_list.append(flow_curve)
                Author_list.append(lit_data['Papers'][paper]['Authors'])
                Paper_list.append(lit_data['Papers'][paper]['Title'])
                no_curves +=1
    return curve_list, no_curves, Paper_list, Author_list
    

def curve_filter_pd(Temperature_C='any', 
                 Strain_rate='any', 
                 microstructure='any', 
                 heater='any',
                 sample_diameter='any',
                 sample_length='any'):
    no_curves = 0
    curve_list = []
    Paper_list =[]
    Author_list =[]
    for paper in lit_data['Papers']:
        for curve in paper['Curves']:
            temp_bool = curve['Temperature_C'] == Temperature_C or Temperature_C == 'any'
            strain_bool = curve['Strain_rate_s-1'] == Strain_rate or Strain_rate =='any'
            micro_bool = curve['microstructure_type'] == microstructure or microstructure == 'any'
            heat_bool = curve['In_situ_heating'] == heater or heater == 'any'
            diameter_bool = curve['sample_diameter_mm'] == sample_diameter or sample_diameter == 'any'
            length_bool = curve['sample_length_mm'] == sample_diameter or sample_diameter =='any'
            if temp_bool & strain_bool & micro_bool & diameter_bool & length_bool:
                flow_curve = pd.read_csv('Flow_curves/'+curve['Curve_location'])
                curve_list.append(flow_curve)
                Author_list.append(lit_data['Papers'][paper]['Authors'])
                Paper_list.append(lit_data['Papers'][paper]['Title'])
                no_curves +=1
    return curve_list, no_curves, Paper_list, Author_list


def flow_curve_plotter(curve_list, fig_no, Authors, Temperature_C='any', Strain_rate='any', microstructure='any', heater='any'):
    for n, curve in enumerate(curve_list):
        plt.plot(curve[:,0], curve[:,1], label=Authors[n])
    Title = 'Flow curves of Ti64 with ' + microstructure +' at ' + str(Temperature_C) + 'C and ' + str(Strain_rate)+ 's-1 strain rate'
    plt.title(Title)
    plt.xlabel('strain')
    plt.ylabel('Stress/MPa')
    plt.legend(bbox_to_anchor=[1, 1])