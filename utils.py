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
                curve = pd.read_csv(curve['Curve_location'], delimiter=",")
#                 curve = sort_curve(curve)
                curve_list.append(curve)
                Author_list.append(lit_data['Papers'][paper]['Authors'][0])
                Paper_list.append(lit_data['Papers'][paper]['Title'])
                no_curves +=1
    return curve_list, no_curves, Paper_list, Author_list


def beta_approach_curve_filter(lit_data,
                              authors_list=[],
                              year_of_publication=[],
                              heating_rate='any', 
                              Strain_rate='any',  
                              heater='any'
                             ):
    filtered_data = {}
    filtered_data['Papers'] = {}
    for paper in lit_data['Papers'].keys():
        filtered_data['Papers'][paper] = {}
        
        authors_bool = lit_data['Papers'][paper]['Authors'][0] in authors_list or authors_list==[]
        year_of_publication_bool = lit_data['Papers'][paper]['year_of_publication'] in year_of_publication or year_of_publication==[]
        
        filtered_data['Papers'][paper]['Curves'] = []
        for curve_num, curve in enumerate(lit_data['Papers'][paper]['Curves']):
            
            heating_rate_bool = curve['heating_rate'] == heating_rate or heating_rate=='any' or heating_rate=='check'
            Strain_rate_bool = curve['Strain_rate_s-1'] == Strain_rate or Strain_rate =='any' or Strain_rate=='check'
            heater_bool = curve['In_situ_heating'] == heater or heater == 'any' or heater=='check'
            
            if authors_bool & year_of_publication_bool & heating_rate_bool & Strain_rate_bool & heater_bool:
                filtered_data['Papers'][paper]['Curves'].append( lit_data['Papers'][paper]['Curves'][curve_num]['data'] )
                filtered_data['Papers'][paper]['Title'] = lit_data['Papers'][paper]['Title']
                filtered_data['Papers'][paper]['Authors'] = lit_data['Papers'][paper]['Authors']
                filtered_data['Papers'][paper]['year_of_publication'] = lit_data['Papers'][paper]['year_of_publication']
                
    return filtered_data


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
        plt.plot(curve.iloc[:,0], curve.iloc[:,1], label=Authors[n])
    Title = 'Flow curves of Ti64 with ' + microstructure +' at ' + str(Temperature_C) + 'C and ' + str(Strain_rate)+ 's-1 strain rate'
    plt.title(Title)
    plt.xlabel('strain')
    plt.ylabel('Stress/MPa')
    plt.legend(bbox_to_anchor=[1, 1])


def beta_approach_curve_plotter(filtered_data):
    marker_list = ['s', '^', 'h', 'X', '*', '+', 'o', '.', 'P']
    
    for p, paper in enumerate(filtered_data['Papers']):
        for c, curve in enumerate(filtered_data['Papers'][paper]['Curves']):
            plt.plot(curve.iloc[:,0], curve.iloc[:,1], label=f"{paper}",
                     marker=marker_list[p], linestyle='none', color='k'
                    )
    plt.title('Beta approach curves of Ti64')
    plt.xlim([None,1000])
    plt.xlabel(f"Temperature [C]")
    plt.ylim([0,100])
    plt.ylabel(f"% Vol frac β")
    plt.yticks([0,10,20,30,40,50,60,70,80,90,100],
           ["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"])
    plt.grid()
    plt.legend(bbox_to_anchor=[1.1, 1])