from .core import ControlVars
from .utils import (create_dataset, include_cultivar_column, generate_numeric_column, calculate_NGP_linear_reg)

def retrieve_vars_from_global_context():
  

def get_dataset (start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG):
  """
  start_date (str): start date of the dataset. Format: '2024-02-21'
  end_date (str): end date of the dataset. Format: '2024-02-21'
  cultivar (str): Cultivar name
  PH (float): pH value
  NLP (float): NLP value
  NGL (float): NGL value
  NS (float): NS value
  IFP (float): IFP value
  MHG (float): MHG value
  """
  df = create_dataset(start_date, end_date)
  df = include_cultivar_column(df, cultivar)
  total_values = len(df)
  df['PH'] = generate_numeric_column(PH, 'PH', total_values)
  df['NLP'] = generate_numeric_column(NLP, 'NLP', total_values)
  df['NGP'] = calculate_NGP_linear_reg (df['NLP'])
  df['NGL'] = generate_numeric_column(NGL, 'NGL', total_values)
  df['NS'] = generate_numeric_column(NS, 'NS', total_values)
  df['IFP'] = generate_numeric_column(IFP, 'IFP', total_values)
  df['MHG'] = generate_numeric_column(MHG, 'MHG', total_values)

  return df
  