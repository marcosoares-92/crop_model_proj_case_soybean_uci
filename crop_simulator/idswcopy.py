"""
Classes and functions copied and adapted from IDSW: https://github.com/marcosoares-92/IndustrialDataScienceWorkflow/tree/main

"""
from .utils import ControlVars
import pandas as pd
import matplotlib.pyplot as plt


def export_pd_dataframe_as_excel (file_name_without_extension, exported_tables = [{'dataframedataframe_obj_to_be_exported': None, 'excel_sheet_name': None}], file_directory_path = None):
    """
    export_pd_dataframe_as_excel (file_name_without_extension, exported_tables = [{'dataframedataframe_obj_to_be_exported': dataframe_obj_to_be_exported, 'excel_sheet_name': excel_sheet_name}], file_directory_path = None):
    
    This function allows the user to export several dataframes as different sheets from a single
    Excel file.
    WARNING: all files exported from this function are .xlsx

    : param: file_name_without_extension - (string, in quotes): input the name of the 
      file without the extension. e.g. new_file_name_without_extension = "my_file" 
      will export a file 'my_file.xlsx' to notebook's workspace.

    : param: exported_tables is a list of dictionaries.
      User may declare several dictionaries, as long as the keys are always the same, and if the
      values stored in keys are not None.
      
      : key 'dataframe_obj_to_be_exported': dataframe object that is going to be exported from the
      function. Since it is an object (not a string), it should not be declared in quotes.
      example: dataframe_obj_to_be_exported = dataset will export the dataset object.
      ATTENTION: The dataframe object must be a Pandas dataframe.

      : key 'excel_sheet_name': string containing the name of the sheet to be written on the
      exported Excel file. Example: excel_sheet_name = 'tab_1' will save the dataframe in the
      sheet 'tab_1' from the file named as file_name_without_extension.

      examples: exported_tables = [{'dataframe_obj_to_be_exported': dataset1, 'excel_sheet_name': 'sheet1'},]
      will export only dataset1 as 'sheet1';
      exported_tables = [{'dataframe_obj_to_be_exported': dataset1, 'excel_sheet_name': 'sheet1'},
      {'dataframe_obj_to_be_exported': dataset2, 'excel_sheet_name': 'sheet2']
      will export dataset1 as 'sheet1' and dataset2 as 'sheet2'.

      Notice that if the file does not contain the exported sheets, they will be created. If it has,
      the sheets will be replaced.
    
    : param: FILE_DIRECTORY_PATH - (string, in quotes): input the path of the directory 
      (e.g. folder path) where the file is stored. e.g. FILE_DIRECTORY_PATH = "/" 
      or FILE_DIRECTORY_PATH = "/folder"
      If you want to export the file to AWS S3, this parameter will have no effect.
      In this case, you can set FILE_DIRECTORY_PATH = None
    """

    import os

    # Create the complete file path:
    file_path = os.path.join(file_directory_path, file_name_without_extension)
    # Concatenate the extension ".csv":
    file_path = file_path + ".xlsx"

    # Pandas ExcelWriter class:
    # https://pandas.pydata.org/docs/reference/api/pandas.ExcelWriter.html#pandas.ExcelWriter
    # Pandas to_excel method:
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html

    try:
        # The replacement of a Sheet will only occur in the append ('a') mode.
        # 'a' is a mode available for the cases where an Excel file is already present.
        # Let's check if there is an Excel file previously created, so that we will not
        # delete it:
        with pd.ExcelWriter(file_path, date_format = "YYYY-MM-DD",
                            datetime_format = "YYYY-MM-DD HH:MM:SS",
                            mode = 'a', if_sheet_exists = 'replace') as writer:
            
            for storage_dict in exported_tables:
                df, sheet = storage_dict['dataframe_obj_to_be_exported'], storage_dict['excel_sheet_name']
                
                if ((df is not None) & (sheet is not None) & (type(df) == pd.DataFrame)):
                    # Guarantee sheet name is a string
                    sheet = str(sheet)
                    df.to_excel(writer, sheet_name = sheet, na_rep='', 
                                header = True, index = False, 
                                startrow = 0, startcol = 0, merge_cells = False, 
                                inf_rep = 'inf')

    except:
        # The context manager created by class ExcelWriter with 'a' mode returns an error when
        # there is no Excel file available. Since we do not have the risk of overwriting the file,
        # we can open the writer in write ('w') mode to create a new spreadsheet:
        with pd.ExcelWriter(file_path, date_format = "YYYY-MM-DD",
                            datetime_format = "YYYY-MM-DD HH:MM:SS", mode = 'w') as writer:
            
            for storage_dict in exported_tables:
                df, sheet = storage_dict['dataframe_obj_to_be_exported'], storage_dict['excel_sheet_name']
                
                if ((df is not None) & (sheet is not None) & (type(df) == pd.DataFrame)):
                    # Guarantee sheet name is a string
                    sheet = str(sheet)
                    df.to_excel(writer, sheet_name = sheet, index = False, 
                                startrow = 0, startcol = 0, merge_cells = False, 
                                inf_rep = 'inf')

def time_series_vis (x, y, plot_title):
    """
    SIMPLIFIED VERSION FROM ORIGINAL IDSW FUNCTION

    time_series_vis (data_in_same_column = False, df = None, column_with_predict_var_x = None, column_with_response_var_y = None, column_with_labels = None, list_of_dictionaries_with_series_to_analyze = [{'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}, {'x': None, 'y': None, 'lab': None}], x_axis_rotation = 70, y_axis_rotation = 0, grid = True, add_splines_lines = True, add_scatter_dots = False, horizontal_axis_title = None, vertical_axis_title = None, plot_title = None, export_png = False, directory_to_save = None, file_name = None, png_resolution_dpi = 330):
    
    matplotlib.colors documentation:
     https://matplotlib.org/3.5.0/api/colors_api.html?msclkid=94286fa9d12f11ec94660321f39bf47f
    
    Matplotlib list of colors:
     https://matplotlib.org/stable/gallery/color/named_colors.html?msclkid=0bb86abbd12e11ecbeb0a2439e5b0d23
    Matplotlib colors tutorial:
     https://matplotlib.org/stable/tutorials/colors/colors.html
    Matplotlib example of Python code using matplotlib.colors:
     https://matplotlib.org/stable/_downloads/0843ee646a32fc214e9f09328c0cd008/colors.py
    Same example as Jupyter Notebook:
     https://matplotlib.org/stable/_downloads/2a7b13c059456984288f5b84b4b73f45/colors.ipynb

    """
    LINE_STYLE = '-'
    # Alternatively: LINE_STYLE = '' not to show spline lines
    MARKER = ''
    # Alternatively: MARKER = 'o' to show scatter dots
    x_axis_rotation = 70
    y_axis_rotation = 0 
    grid = True

    if (ControlVars.language_pt == True):
      vertical_axis_title = "Produtividade de Grãos (kg/ha)"
      horizontal_axis_title = "Data"
    
    else:
      vertical_axis_title = "Grain Yield (kg/ha)"
      horizontal_axis_title = "Date"

    # Matplotlib linestyle:
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html?msclkid=68737f24d16011eca9e9c4b41313f1ad
        
    # Let's put a small degree of transparency (1 - OPACITY) = 0.05 = 5%
    # so that the bars do not completely block other views.
    OPACITY = 0.95
    COLOR = 'fuchsia'
        
    #Set image size (x-pixels, y-pixels) for printing in the notebook's cell:
    fig = plt.figure(figsize = (12, 8))
    ax = fig.add_subplot()

    # Scatter plot:
    ax.plot(x, y, linestyle = LINE_STYLE, 
                  marker = MARKER, color = COLOR, alpha = OPACITY, 
                  # label = label
                  )
    # Axes.plot documentation:
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html?msclkid=42bc92c1d13511eca8634a2c93ab89b5
            
    # x and y are positional arguments: they are specified by their position in function
    # call, not by an argument name like 'marker'.
            
    # Matplotlib markers:
    # https://matplotlib.org/stable/api/markers_api.html?msclkid=36c5eec5d16011ec9583a5777dc39d1f
            
    # Now we finished plotting all of the series, we can set the general configuration:
        
    #ROTATE X AXIS IN XX DEGREES
    plt.xticks(rotation = x_axis_rotation)
    # XX = 0 DEGREES x_axis (Default)
    #ROTATE Y AXIS IN XX DEGREES:
    plt.yticks(rotation = y_axis_rotation)
    # XX = 0 DEGREES y_axis (Default)

    ax.set_title(plot_title)
    ax.set_xlabel(horizontal_axis_title)
    ax.set_ylabel(vertical_axis_title)

    ax.grid(grid) # show grid or not
    ### ax.legend(loc = 'upper left')
    # position options: 'upper right'; 'upper left'; 'lower left'; 'lower right';
    # 'right', 'center left'; 'center right'; 'lower center'; 'upper center', 'center'
    # https://www.statology.org/matplotlib-legend-position/
    
    # Image will be exported to root directory
    import os
    directory_to_save = ""
    file_name = plot_title
    png_resolution_dpi = 330
    #Get the new_file_path
    new_file_path = os.path.join(directory_to_save, file_name)
    new_file_path = new_file_path + ".png"
    # supported formats = 'png', 'pdf', 'ps', 'eps' or 'svg'
    #Export the file to this new path:
    plt.savefig(new_file_path, dpi = png_resolution_dpi, transparent = False) 

    plt.show()

def download_file_from_colab (file):
    """
    FUNCTION ADAPTED AND SIMPLIFIED FROM IDSW - SIMPLER CASE: NO DRIVE MOUNTED, ONLY DOWNLOAD
    """
    from google.colab import files
    files.download(file)

class LoadCropSimulator:
  """Load Crop Simulator on your environment without installing with pip install."""

  def __init__(self):
    """
      DEFINE COMMANDS (Bash script) and success messages and set timeout.
    """
    # Clone git repository:
    self.cmd_line1 = """git clone https://github.com/marcosoares-92/crop_model_proj_case_soybean_uci crop_model_proj_case_soybean_uci"""

    # Move crop_simulator directory to root (Python workspace):
    self.cmd_line2 = """mv crop_model_proj_case_soybean_uci/crop_simulator ."""
    # Move KMeans model to root
    self.cmd_line3 = """mv crop_model_proj_case_soybean_uci/models_and_encodings/kmeans_model.pkl ."""
    # Move LSTM model to root
    self.cmd_line4 = """mv crop_model_proj_case_soybean_uci/models_and_encodings/lstm.keras ."""



  def set_process (self, cmd_line):
    """Define a process to run from a command:
    : param: cmd_line (str): command that is passed to a command line interface.
      Attention: different parts and flags must be separated by single whitespaces.
    """
    from subprocess import Popen, PIPE, TimeoutExpired

    proc = Popen(cmd_line.split(" "), stdout = PIPE, stderr = PIPE)
    """cmd_line = "git clone https://github.com/marcosoares-92/IndustrialDataScienceWorkflow IndustrialDataScienceWorkflow"
      will lead to the list ['git', 'clone', 'https://github.com/marcosoares-92/IndustrialDataScienceWorkflow', 'IndustrialDataScienceWorkflow']
      after splitting the string in whitespaces, what is done by .split(" ") method.
    """
    return proc
  

  def run_process (self, proc, msg = ''):
    """Run process defined by method set_process.
      : param: proc: process execution object returned from set_process.
      : param: msg (str): user-defined confirmation method.
      : param: timeout (int): number of seconds to wait for a command to run, before considering error.
    """

    try:
        output, error = proc.communicate()
        if len(msg > 0):
          print (msg)
    except:
        # General exception
        output, error = proc.communicate()
        
    return output, error


  def clone_repo(self):
    """Clone GitHub Repository."""
    
    # SET PROCESS:
    self.proc1 = self.set_process (self.cmd_line1)
    # RUN PROCESS:
    self.output1, self.error1 = self.run_process(self.proc1)

    return self

  
  def move_pkg(self):
    """Move package and models to the working directory, to make it available."""
    
    # SET PROCESS:
    self.proc2 = self.set_process (self.cmd_line2)
    # RUN PROCESS:
    self.output2, self.error2 = self.run_process(self.proc2)
    # SET PROCESS:
    self.proc3 = self.set_process (self.cmd_line3)
    # RUN PROCESS:
    self.output3, self.error3 = self.run_process(self.proc3)
    # SET PROCESS:
    self.proc4 = self.set_process (self.cmd_line4)
    # RUN PROCESS:
    self.output4, self.error4 = self.run_process(self.proc4)


    return self
  

  def move_pkg_alternative(self):
    """Alternative using the Bash utils module (shutil)"""
    # importing shutil module  
    import shutil
    
    # Source path  
    source = 'crop_model_proj_case_soybean_uci/models_and_encodings'  
    # Destination path  
    destination = '.'
    # Move the content of source to destination  
    dest = shutil.move(source, destination)
    
    return self

def load_simulator ():
  
  loader = LoadCropSimulator()
  loader = loader.clone_repo()
  loader = loader.move_pkg()
