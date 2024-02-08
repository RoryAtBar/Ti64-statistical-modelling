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

def expt_data_filter():
    # Experimental data filter
    for expt_key in database['Experiments'].keys():
        authors_bool = database['Experiments'][expt_key]['Authors'][0] in authors_list or authors_list==[]
        year_of_publication_bool = database['Experiments'][expt_key]['year_of_publication'] in year_of_publication or year_of_publication==[]
        # exclusion bool true if in list
        exclusion_bool = database['Experiments'][expt_key]['Authors'][0] in exclsuions or database['Experiments'][expt_key]['year_of_publication'] in exclusions
        
        if authors_bool & year_of_publication_bool:
            for curve_num, curve in enumerate(database['Experiments'][expt_key]['Curves']):
                # must sort curve by T for fitting to work:
                sorted_curve = database['Experiments'][expt_key]['Curves'][curve_num]['data'].sort_values(by=['T'])
            
                heating_rate_bool = curve['heating_rate'] == heating_rate or heating_rate=='any' or heating_rate=='check'
                Strain_rate_bool = curve['Strain_rate_s-1'] == Strain_rate or Strain_rate =='any' or Strain_rate=='check'
                heater_bool = curve['In_situ_heating'] == heater or heater == 'any' or heater=='check'
            
                if heating_rate_bool & Strain_rate_bool & heater_bool:
                    filtered_data['Experiments'][expt_key]['Curves'].append( sorted_curve )
                    filtered_data['Experiments'][expt_key]['Title'] = database['Experiments'][expt_key]['Title']
                    filtered_data['Experiments'][expt_key]['Authors'] = database['Experiments'][expt_key]['Authors']
                    filtered_data['Experiments'][expt_key]['year_of_publication'] = database['Experiments'][expt_key]['year_of_publication']

    return filtered_data


def lit_data_filter(database):
    for paper_key in database['Papers'].keys():
        authors_bool = database['Papers'][paper_key]['Authors'][0] in authors_list or authors_list==[]
        year_of_publication_bool = database['Papers'][paper_key]['year_of_publication'] in year_of_publication or year_of_publication==[]
        # exclusion bool true if any in list # NOT YET IMPLEMENTED!
        exclusion_bool = database['Experiments'][expt_key]['Authors'][0] in exclsuions or database['Experiments'][expt_key]['year_of_publication'] in exclusions
        
        if authors_bool & year_of_publication_bool:
            for curve_num, curve in enumerate(database['Papers'][paper_key]['Curves']):
                # must sort curve by T for fitting to work:
                sorted_curve = database['Papers'][paper_key]['Curves'][curve_num]['data'].sort_values(by=['T'])
            
                heating_rate_bool = curve['heating_rate'] == heating_rate or heating_rate=='any' or heating_rate=='check'
                Strain_rate_bool = curve['Strain_rate_s-1'] == Strain_rate or Strain_rate =='any' or Strain_rate=='check'
                heater_bool = curve['In_situ_heating'] == heater or heater == 'any' or heater=='check'
            
                if heating_rate_bool & Strain_rate_bool & heater_bool:
                    filtered_data['Papers'][paper_key]['Curves'].append( sorted_curve )
                    filtered_data['Papers'][paper_key]['Title'] = database['Papers'][paper_key]['Title']
                    filtered_data['Papers'][paper_key]['Authors'] = database['Papers'][paper_key]['Authors']
                    filtered_data['Papers'][paper_key]['year_of_publication'] = database['Papers'][paper_key]['year_of_publication']
                
    return filtered_data


def curve_filter(database, keys_list=[], authors_list=[], year_of_publication=[], exclusions=[],
                 heating_rate='any', Strain_rate='any', heater='any',
                 ):
    filtered_data = {}
    filtered_data['Papers'] = {}
    filtered_data['Papers'][paper_key] = {'Curves':[]}
    
    filtered_data['Experiments'] = {}
    filtered_data['Experiments'][expt_key] = {'Curves':[]}
    
    # Experimental data filter
    filtered_data = expt_data_filter(database)
    
    # Literature data filter
    filtered_data = lit_data_filter(database)
    
    return filtered_data


def curve_plotter(filtered_data):
    marker_list = ['s', '^', 'h', 'X', '*', '+', 'o', '.', 'P']
    
    for e, expt in enumerate(filtered_data['Experiments']):
        for c, curve in enumerate(filtered_data['Experiments'][expt]['Curves']):
            plt.plot(curve.iloc[:,0], curve.iloc[:,1], label=f"{expt}",
                     marker=marker_list[e], linestyle='none', color='k'
                    )
    
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