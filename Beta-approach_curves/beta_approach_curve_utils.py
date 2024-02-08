import yaml
from yaml.loader import FullLoader
from yaml.loader import SafeLoader
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def load_yml(alloy, yml_file='beta-approach_curves.yml'):
    
    database = yaml.load(open('beta-approach_curves.yml'), Loader=SafeLoader)[alloy]
    # LOAD EXPT DATA
    for expt in database['Experiments'].keys():
        for curve_no, curve_metadata in enumerate(database['Experiments'][expt]['Curves']):
            path_to_data = os.path.abspath(database['Experiments'][expt]['Curves'][curve_no]['Curve_location'])
            expt_curve_data = pd.read_csv(path_to_data,
                                         delimiter=",")
            database['Experiments'][expt]['Curves'][curve_no]['data'] = expt_curve_data
            database['Experiments'][expt]['Curves'][curve_no]['dataset_key'] = expt # include dataset key in curve

    # LOAD LIT DATA
#     try:
    for paper in database['Papers'].keys():
        for curve_no, curve_metadata in enumerate(database['Papers'][paper]['Curves']):
            path_to_data = os.path.abspath(database['Papers'][paper]['Curves'][curve_no]['Curve_location'])
            lit_curve_data = pd.read_csv(path_to_data,
                                     delimiter=",")
            database['Papers'][paper]['Curves'][curve_no]['data'] = lit_curve_data
            database['Papers'][paper]['Curves'][curve_no]['dataset_key'] = paper # include dataset key in curve
#     except:
#         database['Papers'] = None
        
    print(f"\nExperiments: \n{database['Experiments'].keys()}")
    print(f"\nPapers: \n{database['Papers'].keys()}")
    return database


def sort_curve(curve):
    sorted_curve = np.zeros(np.shape(curve))
    ind = np.argsort(curve, axis=0)
    for i in range(len(curve)):
        sorted_curve[i,0]= curve[ind[i,0],0]
        sorted_curve[i,1]= curve[ind[i,0],1]
    return sorted_curve


def include_dataset(curve, chosen_parameters):

    # USER DEFINED PARAMS
    chosen_heatrate =       chosen_parameters['heating_rate']
    chosen_strainrate =     chosen_parameters['Strain_rate_s-1']
    chosen_heater =         chosen_parameters['In_situ_heating']
    exclusions =            chosen_parameters['exclusions']
    
    # EACH BOOL TRUE IF MATCHING USER CHOICE OR 'ANY' CHOSEN
    heatrate_bool       = curve['heating_rate']==chosen_heatrate              or chosen_heatrate=='any'
    strainrate_bool     = curve['Strain_rate_s-1']==chosen_strainrate         or chosen_strainrate=='any'
    heattype_bool       = curve['In_situ_heating']==chosen_heater             or chosen_heater=='any'
    
    # EXCLUDE IF KEY, TITLE, OR AUTHORS ARE IN EXCLUSIONS LIST:
    exclude = curve['dataset_key'] in exclusions
    
    # IF ALL TRUE INCLUDE DATASET
    if heatrate_bool & strainrate_bool & heattype_bool:
        if exclude:
            print(f"{curve['dataset_key']} IN EXCLUSIONS LIST.")
            include_bool = False
        else:
            include_bool = True
    else:
        include_bool = False
    return include_bool


def curve_filter(database, chosen_parameters):
    print(f"Chosen heating rate:{chosen_parameters['heating_rate']}\n") # DEBUG: Inform user of chosen params
    
    # initialise filtered database as empty dict of dicts:
    filtered_database = {'Experiments' : {  },
                         'Papers' : {  }  }
    
    for datasource in ['Experiments', 'Papers']: # ['Experiments', 'Papers'] # DEBUG: JUST USE PAPERS FOR NOW...
        for dataset_key in database[datasource]: # idividual expt/paper
            curve_list = [] # initialise empty curve list on looking at new dataset...
            for curve_num, curve in enumerate(database[datasource][dataset_key]['Curves']):
                if include_dataset(curve, chosen_parameters): # If include func returns true:
                    print(f"Including {dataset_key}") # DEBUG
                    curve_list.append(curve)
                    # only add dataset_key to dict if curve contains chosen params
                    filtered_database[datasource][dataset_key] = {
                                                                  'Title' : database[datasource][dataset_key]['Title'],
                                                                  'Authors' : database[datasource][dataset_key]['Authors'],
                                                                  'year_of_publication' : database[datasource][dataset_key]['Title'],
                                                                  'Curves': curve_list
                                                                 }
                else:
#                     print(f"Excluding {dataset_key} curve {curve_no}") # DEBUG
                    pass # if not included, move on...
        
    return filtered_database


def curve_plotter(database):
    marker_list = ['s', '^', 'h', 'X', '*', '+', 'o', '.', 'P']
    
    for datasource in ['Papers']: # ['Experiments', 'Papers'] # DEBUG: JUST USE PAPERS FOR NOW...
        for p, dataset_key in enumerate(database[datasource]): # idividual expt/paper
            for curve in database[datasource][dataset_key]['Curves']:
                plt.plot(curve['data'].iloc[:,0], curve['data'].iloc[:,1], label=dataset_key,
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