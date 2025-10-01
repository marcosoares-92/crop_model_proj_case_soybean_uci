from .create import get_dataset
from .modelling import prediction_pipeline
from .idswcopy import export_pd_dataframe_as_excel
from .utils import ControlVars, update_control_vars, retrieve_vars_from_global_context

from datetime import datetime, timedelta
import pandas as pd


def orchestrate_pipelines():
  """Orchestrate all the pipelines to obtain a full simulation.
  At the end, store in a list of dictionaries in ControlVars, that will be used for exporting a 
  consolidated Excel file with all simulations.
  """
  start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG, cluster_model_path, lstm_model_path = retrieve_vars_from_global_context()
  df = get_dataset(start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG)
  df = prediction_pipeline(df, cluster_model_path, lstm_model_path)
  # Update on ControlVars:
  ControlVars.df = df
  # Update the simulation counting:
  ControlVars.simulation_counter = ControlVars.simulation_counter + 1
  # Get list exported_tables:
  exported_tables = ControlVars.exported_tables
  # Get a date now to differentiate from others
  conclusion_time = pd.Timestamp(datetime.now())
  update_control_vars(start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG, cluster_model_path, lstm_model_path)

  # Obtain sheet name:
  # Apply timestamp() method to convert the timestamp to POSIX timestamp as float
  # https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.timestamp.html#pandas.Timestamp.timestamp
  # It will guarantee that each sheet is unique. Also, hours in 00:00:00 format cannot
  # be used as sheet names, due to the ":" non-allowed character.
  sheet_name = "sim" + str(simulation_counter) + "_" + str(conclusion_time.timestamp())
  
  # Get a dictionary for exporting the table:
  table_dict = {'dataframe_obj_to_be_exported': df, 
                    'excel_sheet_name': sheet_name,
                    'conclusion_time': conclusion_time}

  # Append the dictionary on the list of exported tables:
  exported_tables.append(table_dict)
  # Update Global Variables:
  ControlVars.exported_tables = exported_tables

  if (ControlVars.language_pt):
    completion_msg = f"""










      -------------------------------------------------------------------------------
                        CROP SIMULATOR - SIMULAÇÃO DE PRODUÇÃO DE SOJA


      SIMULAÇÃO COMPLETA!


      # RELATÓRIO DE SIMULAÇÃO
      SIMULAÇÃO #{ControlVars.simulation_counter}: IDENTIFICADOR {conclusion_time.timestamp()} 
      - SIMULAÇÃO INICIADA EM (TEMPO DO SERVIDOR) = {ControlVars.server_start_time}
      - SIMULAÇÃO FINALIZADA EM (TEMPO DO SERVIDOR) = {conclusion_time}

      ## PARÂMETROS DE ENTRADA DO USUÁRIO

      DATA DE INÍCIO = {ControlVars.start_date}
      DATA DE TÉRMINO = {ControlVars.end_date}
      HÍBRIDO DE SOJA = {ControlVars.cultivar}
      ALTURA DA PLANTA (PH) = {ControlVars.PH} cm
      INSERÇÃO DA PRIMEIRA VAGEM (IFP) = {ControlVars.IFP} cm
      NÚMERO DE HASTES E RAMOS (NLP) = {ControlVars.NLP} units
      NÚMERO DE GRÃOS POR PLANTA (NGL) {ControlVars.NGL} units
      NÚMERO DE GRÃOS POR VAGEM (NS) = {ControlVars.NS} units
      MASSA DE MIL SEMENTES (MHG) = {ControlVars.MHG} g

      -------------------------------------------------------------------------------

      """

    # CREATE A DATAFRAME WITH THE SIMULATION REPORT:

    parameters = ['SIMULAÇÃO #', 'IDENTIFICADOR', 'SIMULAÇÃO INICIADA EM (TEMPO DO SERVIDOR)',
                  'SIMULAÇÃO FINALIZADA EM (TEMPO DO SERVIDOR)', 'DATA DE INÍCIO',
                  'DATA DE TÉRMINO', 'HÍBRIDO DE SOJA', 'ALTURA DA PLANTA (PH)',
                  'INSERÇÃO DA PRIMEIRA VAGEM (IFP)', 'NÚMERO DE HASTES E RAMOS (NLP)',
                  'NÚMERO DE GRÃOS POR PLANTA (NGL)', 
                  'NÚMERO DE GRÃOS POR VAGEM (NS)', 'MASSA DE MIL SEMENTES (MHG)']
    
    user_input_params = [f"{ControlVars.simulation_counter}", f"{conclusion_time.timestamp()}", 
              f"{ControlVars.server_start_time}", f"{conclusion_time}", f"{ControlVars.start_date}",
              f"{ControlVars.end_date}", f"{ControlVars.cultivar}",
              f"{ControlVars.PH} cm", f"{ControlVars.IFP} cm",
              f"{ControlVars.NLP} units", f"{ControlVars.NGL} units",
              f"{ControlVars.MHG} g"]
  
  else:
    completion_msg = f"""










      -------------------------------------------------------------------------------
                        CROP SIMULATOR - SOYBEAN PRODUCTION


      SIMULATION COMPLETED!


      # SIMULATION REPORT
      SIMULATION #{ControlVars.simulation_counter}: IDENTIFIER {conclusion_time.timestamp()} 
      - STARTED SIMULATION AT (SERVER TIME) = {ControlVars.server_start_time}
      - FINISHED SIMULATION AT (SERVER TIME) = {conclusion_time}

      ## USER INPUT PARAMETERS

      START DATE = {ControlVars.start_date}
      END DATE = {ControlVars.end_date}
      CULTIVAR = {ControlVars.cultivar}
      PLANT HEIGHT (PH) = {ControlVars.PH} cm
      INSERTION OF THE FIRST POD (IFP) = {ControlVars.IFP} cm
      NUMBER OF STEMS (NLP) = {ControlVars.NLP} units
      NUMBER OF GRAINS PER PLANT (NGL) {ControlVars.NGL} units
      NUMBER OF GRAINS PER POD (NS) = {ControlVars.NS} units
      THOUSAND SEED WEIGHT (MHG) = {ControlVars.MHG} g

      -------------------------------------------------------------------------------

      """

    # CREATE A DATAFRAME WITH THE SIMULATION REPORT:

    parameters = ['SIMULATION #', 'IDENTIFIER', 'STARTED SIMULATION AT (SERVER TIME)',
                  'FINISHED SIMULATION AT (SERVER TIME)', 'START DATE',
                  'END DATE', 'CULTIVAR', 'PLANT HEIGHT (PH)',
                  'INSERTION OF THE FIRST POD (IFP)', 'NUMBER OF STEMS (NLP)',
                  'NUMBER OF GRAINS PER PLANT (NGL)', 
                  'NUMBER OF GRAINS PER POD (NS)', 'THOUSAND SEED WEIGHT (MHG)']
    
    user_input_params = [f"{ControlVars.simulation_counter}", f"{conclusion_time.timestamp()}", 
              f"{ControlVars.server_start_time}", f"{conclusion_time}", f"{ControlVars.start_date}",
              f"{ControlVars.end_date}", f"{ControlVars.cultivar}",
              f"{ControlVars.PH} cm", f"{ControlVars.IFP} cm",
              f"{ControlVars.NLP} units", f"{ControlVars.NGL} units",
              f"{ControlVars.MHG} g"]
  
  sim_rep = pd.DataFrame(data = {'SIMULATION_REPORT': parameters, 'USER_INPUT': user_input_params})

  # Get a dictionary for exporting the table:
  table_dict = {'dataframe_obj_to_be_exported': sim_rep, 
                    'excel_sheet_name': ("REP_" + sheet_name)}

  # Append the dictionary on the list of exported tables:
  exported_tables.append(table_dict)

  # Finally, update the list:
  ControlVars.exported_tables = exported_tables
  
  print(completion_msg)
  try:
        # only works in Jupyter Notebook:
        from IPython.display import display
        display(sim_df)
            
  except: # regular mode
        print(sim_df)


def run_simulation(start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG):
  """
  Set all user defined parameters, update the global context and actuate the pipeline orchestration
  : params start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG: user defined parameters.
  """
  update_control_vars(start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG)
  orchestrate_pipelines()

def visualize_yield (export_images = True):
  """Plot the GY (yield) for the simulations
  : param: export_images = True keep True to
  export the image files and download them.
  """

  exported_tables = ControlVars.exported_tables
  # Loop through each simulation:
  for table_dict in exported_tables:
    # Check if it is not a Report table. These tables have 4 initial 
    # characters "REP_" in their sheet names.
    if (table_dict['excel_sheet_name'][:4] != "REP_"):
      
      if (ControlVars.language_pt):

        msg = f"""
      
      
        ----------------------------------------------------------------------
                      CROP SIMULATOR - SIMULAÇÃO DE PRODUÇÃO DE SOJA


                              PRODUTIVIDADE DE GRÃOS (kg/ha)


        DADOS DE SIMULAÇÃO ARMAZENADOS EM {table_dict['excel_sheet_name']}
        
        ------------------------------------------------------------------------

        """
      
      else:
        msg = f"""
        
        
          ----------------------------------------------------------------------
                            CROP SIMULATOR - SIMULATING SOYBEAN PRODUCTION


                                GRAIN YIELD (kg/ha)


          SIMULATION DATA STORED IN {table_dict['excel_sheet_name']}
          
          ------------------------------------------------------------------------

          """

      print(msg)
      
      df = table_dict['dataframe_obj_to_be_exported']
      if (ControlVars.language_pt):
        x = df['dia']
        y = df['produtividade_de_graos']
      
      else:
        x = df['timestamp']
        y = df['GY']

      plot_title = table_dict['excel_sheet_name']

      time_series_vis (x, y, plot_title)

      if (export_images):
        # Download the png file saved in Colab environment:
        ACTION = 'download'
        FILE_TO_DOWNLOAD_FROM_COLAB = (table_dict['excel_sheet_name'] + ".png")
        upload_to_or_download_file_from_colab (action = ACTION, file_to_download_from_colab = FILE_TO_DOWNLOAD_FROM_COLAB)

    else:
      pass

def download_excel_with_data():
  """Download Excel file containing all the tables generated from simulations."""
  
  # Create Excel file and store it in Colab's memory:
  FILE_NAME_WITHOUT_EXTENSION = "soybean_crop_simulations"
  EXPORTED_TABLES = ControlVars.exported_tables
  FILE_DIRECTORY_PATH = ""
  export_pd_dataframe_as_excel (file_name_without_extension = FILE_NAME_WITHOUT_EXTENSION, exported_tables = EXPORTED_TABLES, file_directory_path = FILE_DIRECTORY_PATH)

  # Download the file:
  ACTION = 'download'
  FILE_TO_DOWNLOAD_FROM_COLAB = "soybean_crop_simulations.xlsx"
  upload_to_or_download_file_from_colab (action = ACTION, file_to_download_from_colab = FILE_TO_DOWNLOAD_FROM_COLAB)
