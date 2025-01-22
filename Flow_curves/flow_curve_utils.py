import yaml
from yaml.loader import FullLoader
from yaml.loader import SafeLoader
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd


def load_yml(alloy, yml_file='flow_curves.yml'):
    
    database = yaml.load(open('flow_curves.yml'), Loader=SafeLoader)[alloy]
    # LOAD EXPT DATA
    try:
        for expt in database['Experiments'].keys():
            for curve_no, curve_metadata in enumerate(database['Experiments'][expt]['Curves']):
                path_to_data = os.path.abspath(database['Experiments'][expt]['Curves'][curve_no]['Curve_location'])
                expt_flow_curve_data = pd.read_csv(path_to_data,
                                             delimiter=",", header=None, names=["Srain[-]", "Stress(MPa)"])
                database['Experiments'][expt]['Curves'][curve_no]['data'] = expt_flow_curve_data
                database['Experiments'][expt]['Curves'][curve_no]['dataset_key'] = expt # include dataset key in curve
    except:
        database['Experiments'] = None

    # LOAD LIT DATA
#     try:
    for paper in database['Papers'].keys():
        for curve_no, curve_metadata in enumerate(database['Papers'][paper]['Curves']):
            path_to_data = os.path.abspath(database['Papers'][paper]['Curves'][curve_no]['Curve_location'])
            lit_flow_curve_data = pd.read_csv(path_to_data,
                                     delimiter=",", header=None, names=["Srain[-]", "Stress(MPa)"])
            database['Papers'][paper]['Curves'][curve_no]['data'] = lit_flow_curve_data
            database['Papers'][paper]['Curves'][curve_no]['dataset_key'] = paper # include dataset key in curve
#     except:
#         database['Papers'] = None
        
    print(f"\nExperiments: \n{database['Experiments']}")
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
    chosen_diameter =       chosen_parameters['sample_diameter_mm']
    chosen_length =         chosen_parameters['sample_length_mm']
    chosen_microstructure = chosen_parameters['microstructure_type']
    chosen_load =           chosen_parameters['load']
    chosen_strainrate =     chosen_parameters['Strain_rate_s-1']
    chosen_temp =           chosen_parameters['Temperature_C']
    chosen_heater =         chosen_parameters['In_situ_heating']
    exclusions =            chosen_parameters['exclusions']
    
    # EACH BOOL TRUE IF MATCHING USER CHOICE OR 'ANY' CHOSEN
    diameter_bool       = curve['sample_diameter_mm']==chosen_diameter        or chosen_diameter=='any'
    length_bool         = curve['sample_length_mm']==chosen_length            or chosen_length=='any'
    microstructure_bool = curve['microstructure_type']==chosen_microstructure or chosen_microstructure=='any'
    loadtype_bool       = curve['load']==chosen_load                          or chosen_load=='any'
    strainrate_bool     = curve['Strain_rate_s-1']==chosen_strainrate         or chosen_strainrate=='any'
    temp_bool           = curve['Temperature_C']==chosen_temp                 or chosen_temp=='any'
    heattype_bool       = curve['In_situ_heating']==chosen_heater             or chosen_heater=='any'
    
    # EXCLUDE IF KEY, TITLE, OR AUTHORS ARE IN EXCLUSIONS LIST:
    exclude = curve['dataset_key'] in exclusions
    
    # IF ALL TRUE INCLUDE DATASET
    if diameter_bool & length_bool &  microstructure_bool & loadtype_bool & strainrate_bool & temp_bool & heattype_bool:
        if exclude:
            print(f"{curve['dataset_key']} IN EXCLUSIONS LIST.")
            include_bool = False
        else:
            include_bool = True
    else:
        include_bool = False
    return include_bool


def curve_filter(database, chosen_parameters):
    print(f"Chosen T:{chosen_parameters['Temperature_C']}, SR:{chosen_parameters['Strain_rate_s-1']}\n") # DEBUG: Inform user of chosen params
    
    # initialise filtered database as empty dict of dicts:
    filtered_database = {'Experiments' : { '':{} },
                         'Papers' : { '':{} }  }
    
    for datasource in ['Papers']: # ['Experiments', 'Papers'] # DEBUG: JUST USE PAPERS FOR NOW...
        for dataset_key in database[datasource]: # idividual expt/paper
            curve_list = [] # initialise empty curve list on looking at new dataset...
            for curve_num, curve in enumerate(database[datasource][dataset_key]['Curves']):
                if include_dataset(curve, chosen_parameters): # If include func returns true:
                    print(f"Including {dataset_key} load:{database[datasource][dataset_key]['Curves'][curve_num]['load']} T:{database[datasource][dataset_key]['Curves'][curve_num]['Temperature_C']} Microstructure: {database[datasource][dataset_key]['Curves'][curve_num]['microstructure_type']} Strain rate:{database[datasource][dataset_key]['Curves'][curve_num]['Strain_rate_s-1']}") # DEBUG
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


def flow_curve_plotter(database):
    plt.figure(dpi=400)
    
    for datasource in ['Papers']: # ['Experiments', 'Papers'] # DEBUG: JUST USE PAPERS FOR NOW...
        for dataset_key in database[datasource]: # idividual expt/paper
            try:
                for curve in database[datasource][dataset_key]['Curves']:
                    plt.plot(curve['data'].iloc[:,0]-curve['data'].iloc[0,0], curve['data'].iloc[:,1], label=dataset_key)
            except:
                pass
                
    plt.title(f'Flow curves')
    plt.xlabel('strain')
    plt.ylabel('Stress/MPa')
    plt.legend()#bbox_to_anchor=[1, 1])

