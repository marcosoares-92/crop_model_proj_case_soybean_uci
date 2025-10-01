import numpy as np
import pandas as pd
import sklearn
import tensorflow as tf
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class ControlVars:

    language_pt = True # If language_pt = True, responses are shown in Portugues (BR). Otherwise, they are in English
    # default value of start date will be the instant:
    server_start_time = pd.Timestamp(datetime.now())
    simulation_counter = 0 # Count how many simulations were run
    exported_tables = [] # List of exported tables
    cluster_model_path = 'kmeans_model.pkl'
    lstm_model_path = 'lstm.keras'

def create_dataset (start_date, end_date):
  """
  start_date (str): start date of the dataset. Format: '2024-02-21'
  end_date (str): end date of the dataset. Format: '2024-02-21'
  """
  # Convert to datetimes
  start_date = datetime.strptime(start_date, '%Y-%m-%d')
  end_date = datetime.strptime(end_date, '%Y-%m-%d')
  # Create a timedelta and obtain total of days
  timedelta = end_date - start_date
  days = timedelta.days

  # Create an array of dates from the start to the end - one value for each day
  dates = np.linspace(start_date, end_date, num = days).astype('datetime64[D]')
  df = pd.DataFrame(dates, columns = ['timestamp'])

  return df

def include_cultivar_column (df, cultivar):
  """
  cultivar (str): Cultivar name
  """
  dataset = df.copy(deep = True)
  dataset['Cultivar'] = cultivar

  return dataset

def generate_random_values (column, total_values):
  """
  These are random numbers that will be generated to modify the feature selected by the user.
  column (str): name of the feature to generate the random value
  total_values (int): total number of values for the feature
  """
  var_characteristics = {

    'PH': {'min': 47.6, 'max': 94.8, 'max_proba': 63.3, 'std': 9.0},
    'NLP': {'min': 20.2, 'max': 123.0, 'max_proba': 43.0, 'std': 20.1},
    'NGL': {'min': 0.94, 'max': 14.86, 'max_proba': 1.71, 'std': 0.84},
    'NS': {'min': 0.4, 'max': 9.0, 'max_proba': 3.7, 'std': 1.5},
    'IFP': {'min': 7.2, 'max': 26.4, 'max_proba': 16.8, 'std': 3.0},
    'MHG': {'min': 127.1, 'max': 216.0, 'max_proba': 156.7, 'std': 19.6} }

  if column in var_characteristics.keys():
    min = var_characteristics[column]['min']
    max = var_characteristics[column]['max']
    max_proba = var_characteristics[column]['max_proba']
    std = var_characteristics[column]['std']

    # Procedure: let's create a normal distributed variable. But instead of using mu, we use the max probability, and remove values out of the range.
    # Since variables are close to the normal, it will create a normal-like distribution, but with some effects of skewness and kurtosis from original distributions.
    # It will also prevent the generation of data out of the range of model training
    """
    https://numpy.org/doc/stable/reference/random/generated/numpy.random.RandomState.normal.html#numpy.random.RandomState.normal
    loc: float or array_like of floats - Mean (“centre”) of the distribution.
    scale: float or array_like of floats - Standard deviation (spread or “width”) of the distribution. Must be non-negative.
    size: int or tuple of ints, optional - Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn. If size is None (default), a single value is returned
    """
    values = np.random.normal(loc = max_proba, scale = std, size = total_values)
    # Correct values out of range
    values = np.where(values < min, min, values)
    values = np.where(values > max, max, values)

    return values

  else:
    return None

def generate_random_mask (total_values):
  """
  The mask will be used to decide when replace the value for a random value
  total_values (int): total number of values for the feature
  """
  # Generate random values from 0 to 1
  # https://numpy.org/doc/stable/reference/random/generated/numpy.random.random.html#numpy.random.random
  random_values = np.random.random (size = total_values)
  # Generate an array of zeros with same size:
  mask = np.zeros(random_values.shape)
  # If the random_values have a probability >= 0.5, replace by one:
  mask = np.where(random_values >= 0.5, 1, mask)

  return mask

def generate_numeric_column (setpoint, column, total_values):
  """
  These are random numbers that will be generated to modify the feature selected by the user.
  Function is run each time for variable to assure that the random distributions are not the same.
  setpoint (float): numeric value defined by the user for the variable
  column (str): name of the feature to generate the random value
  total_values (int): total number of values for the feature
  """
  random_values = generate_random_values(column, total_values)
  mask = generate_random_mask (total_values)

  # Create an array for the setpoint:
  values = np.zeros(total_values)
  # Where mask ==  1, use setpoint; otherwise, use the correspondent random value
  values = np.where(mask == 1, setpoint, random_values)

  return values

def apply_encoding(df):
  """
  df: dataframe with column 'Cultivar' to be encoded"""

  dataset = df.copy(deep = True)
  dataset['Cultivar_82I78RSF IPRO_OneHotEnc'] = np.where(dataset['Cultivar'] == '82I78RSF IPRO', 1, 0)
  dataset['Cultivar_83IX84RSF I2X_OneHotEnc'] = np.where(dataset['Cultivar'] == '83IX84RSF I2X', 1, 0)
  dataset['Cultivar_96R29 IPRO_OneHotEnc'] = np.where(dataset['Cultivar'] == '96R29 IPRO', 1, 0)
  dataset['Cultivar_97Y97 IPRO_OneHotEnc'] = np.where(dataset['Cultivar'] == '97Y97 IPRO', 1, 0)
  dataset['Cultivar_BRASMAX OLIMPO IPRO_OneHotEnc'] = np.where(dataset['Cultivar'] == 'BRASMAX OLIMPO IPRO', 1, 0)
  dataset['Cultivar_FORTALECE L090183 RR_OneHotEnc'] = np.where(dataset['Cultivar'] == 'FORTALECE L090183 RR', 1, 0)
  dataset['Cultivar_FTR 3179 IPRO_OneHotEnc'] = np.where(dataset['Cultivar'] == 'FTR 3179 IPRO', 1, 0)
  dataset['Cultivar_GNS7900 IPRO - AMPLA_OneHotEnc'] = np.where(dataset['Cultivar'] == 'GNS7900 IPRO - AMPLA', 1, 0)
  dataset['Cultivar_MONSOY 8330I2X_OneHotEnc'] = np.where(dataset['Cultivar'] == 'MONSOY 8330I2X', 1, 0)
  dataset['Cultivar_NK 7777 IPRO_OneHotEnc'] = np.where(dataset['Cultivar'] == 'NK 7777 IPRO', 1, 0)
  dataset['Cultivar_SUZY IPRO_OneHotEnc'] = np.where(dataset['Cultivar'] == 'SUZY IPRO', 1, 0)
  dataset['Cultivar_TMG 22X83I2X_OneHotEnc'] = np.where(dataset['Cultivar'] == 'TMG 22X83I2X', 1, 0)

  dataset = dataset.drop(columns = 'Cultivar')

  return dataset

def calculate_frequency_features(df):
  """
  df: dataframe with column 'timestamp' to be converted to frequency
  """

  important_frequencies = [{'value': 0.3000, 'unit': 'year', 'col': 'f1'},
                         {'value':0.4125, 'unit': 'year', 'col': 'f2'},
                         {'value': 0.4500, 'unit': 'year', 'col': 'f3'},
                         {'value':0.6000, 'unit': 'year', 'col': 'f4'},
                         {'value':0.9000, 'unit': 'year', 'col': 'f5'},
                         {'value':2.1000, 'unit': 'year', 'col': 'f6'},
                         {'value': 4.2000, 'unit': 'year', 'col': 'f7'},
                         {'value':6.0000, 'unit': 'year', 'col': 'f8'}
                         ]
  # 0.300 per year is the 1st freq

  # the Date Time column is very useful, but not in this string form.
  # Start by converting it to seconds:

  # Start a local copy of the dataframe:
  DATASET = df.copy(deep = True)

  # Guarantee that the timestamp column has a datetime object, and not a string
  DATASET['timestamp'] = DATASET['timestamp'].astype('datetime64[ns]')

  # Return POSIX timestamp as float
  # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
  # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.timestamp.html#pandas.Timestamp.timestamp
  # It is a variation of UNIX timestamp]
  # Pandas Timestamp.timestamp() function return the time expressed as the number of seconds that have passed.
  # https://www.geeksforgeeks.org/python-pandas-timestamp-timestamp/
  # since January 1, 1970. That zero moment is known as the epoch.
  timestamp_s = DATASET['timestamp'].map(pd.Timestamp.timestamp)
  # the time in seconds is not a useful model input.
  # It may have daily and yearly periodicity, for instance.
  # To deal with periodicity, you can get usable signals by using sine and cosine transforms
  # to clear "Time of day" and "Time of year" signals:


  for freq_dict in important_frequencies:

      value = 1/freq_dict['value']
      # period.
      column = freq_dict['col']
      # All frequencies are in year^-1 = 1/year
      # convert to seconds, considering a (365.2425)-day year:
      factor = 60 * 60 * 24 * (365.2425)

      if (value is not None):

          column_name1 = column + "_sin"
          column_name2 = column + "_cos"

          # Convert to total of seconds and so use the frequency in Hertz to obtain the periodic functions.
          # Since timestamp_s is already in seconds, it is necessary to make it adimensional.
          # X days correspond to X * 60 * 60 * 24 seconds, for instance, where X == value.
          DATASET[column_name1] = np.sin(timestamp_s * (2 * np.pi / (factor * value)))
          DATASET[column_name2] = np.cos(timestamp_s * (2 * np.pi / (factor * value)))

          # cos(2pi* t/T), where t is the total time in seconds since Jan 1, 1970
          # T is the period, the inverse of the frequency. If the frequency is 2x a year,
          # so the period = 1/2 year. If frequency is once a year, period = 1/1 = 1 year.

  # Drop original timestamps
  DATASET = DATASET.drop(columns = 'timestamp')

  return DATASET

def obtain_log_transformed_features(df):
  """
  df: dataframe with columns to be log-transformed
  """

  dataset = df.copy(deep = True)
  dataset['PH_log'] = np.log(dataset['PH'])
  dataset['NLP_log'] = np.log(dataset['NLP'])
  dataset['NGL_log'] = np.log(dataset['NGL'])
  dataset['NS_log'] = np.log(dataset['NS'])
  dataset['IFP_log'] = np.log(dataset['IFP'])
  dataset['MHG_log'] = np.log(dataset['MHG'])
  dataset = dataset.drop(columns = ['PH', 'NLP', 'NGL', 'NS', 'IFP', 'MHG'])

  return dataset

def obtain_cluster_feature(df, model_path):
  """
  df: dataframe with columns to be clustered with the pretrained KMeans cluster
  model_path (str): path for the KMeans pkl file
  """
  import pickle

  dataset = df.copy(deep = True)

  with open(model_path, 'rb') as opened_file:

    model = pickle.load(opened_file)

  X = np.array(dataset[['PH_log', 'IFP_log', 'NLP_log', 'NGL_log', 'NS_log', 'MHG_log']])
  dataset['cluster'] = model.predict(X)

  return dataset

def get_dataframe_for_lstm(df):
  """
  df: dataframe for feeding LSTM, with feature engineering steps performed
  """
  dataset = df.copy(deep = True)
  dataset = dataset[['f1_sin', 'f1_cos', 'f2_sin',
                    'f2_cos', 'f3_sin', 'f3_cos', 'f4_sin', 'f4_cos', 'f5_sin', 'f5_cos',
                    'f6_sin', 'f6_cos', 'f7_sin', 'f7_cos', 'f8_sin', 'f8_cos', 'cluster',
                    'Cultivar_82I78RSF IPRO_OneHotEnc', 'Cultivar_83IX84RSF I2X_OneHotEnc', 'Cultivar_96R29 IPRO_OneHotEnc', 'Cultivar_97Y97 IPRO_OneHotEnc',
                    'Cultivar_BRASMAX OLIMPO IPRO_OneHotEnc', 'Cultivar_FORTALECE L090183 RR_OneHotEnc', 'Cultivar_FTR 3179 IPRO_OneHotEnc',
                    'Cultivar_GNS7900 IPRO - AMPLA_OneHotEnc', 'Cultivar_MONSOY 8330I2X_OneHotEnc', 'Cultivar_NK 7777 IPRO_OneHotEnc',
                    'Cultivar_SUZY IPRO_OneHotEnc', 'Cultivar_TMG 22X83I2X_OneHotEnc',
                    'PH_log', 'NLP_log', 'NGL_log', 'NS_log']]

  return dataset

def load_lstm (model_path):
  """"
  model_path(str): path of the .keras model file
  """

  model = tf.keras.models.load_model(model_path)
  return model

def get_lstm_preds (model_object, df_transformed):

  """
  df_transformed: dataframe that passed through the feature engineering pipeline and is read to obtain model predictions
  model_object: LSTM model object
  """
  dataset = df_transformed.copy(deep = True)
  X = np.array(dataset)

  # Get predictions for training, testing, and validation:

  if (ControlVars.language_pt):
    print("Calculando produtividade de grãos (kg/ha) – determinada pela colheita da área útil da parcela e padronizada para um teor de umidade dos grãos de 13%...\n")
  else:
    print("Grain yield (GY, kg/ha) – determined by harvesting the useful area of the plot and standardized to a grain moisture level of 13%...\n")

  y_pred = np.array(model_object.predict(X))
  total_dimensions = len(y_pred.shape)
  last_dim = y_pred.shape[(total_dimensions - 1)]
  if (last_dim == 1): # remove last dimension
    if (total_dimensions == 4):
      y_pred = y_pred[:,:,:,0]
    elif (total_dimensions == 3):
      y_pred = y_pred[:,:,0]
    elif (total_dimensions == 2):
      y_pred = y_pred[:,0]

  return y_pred

def run_model (model_path, df_transformed):
  """
  Run model pipeline
  """
  model_object = load_lstm(model_path)
  y_pred = get_lstm_preds(model_object, df_transformed)

  return y_pred

def calculate_NGP_linear_reg (NLP):
  """Add the linear correlation between NLP and NGP to calculate NGP
      Linear regression for NGP x NLP: 
      NGP = 2056079224.54*(NLP) + 55.46, R² = 0.4651

      : param NLP: array-like containing NLP data
  """
  NGP = np.array(NLP) * 2056079224.54 + 55.46
  ControlVars.NGP = NGP
  return NGP

def reverse_log_transform (y_pred):
  """
  Apply exponential transform to reverse log transformation
  y_pred: array with model predictions in log-scale
  """
  y = np.exp(y_pred)
  return y

def update_df (df, y_pred):
  """
  Update dataframe df with the predictions y_pred
  """
  dataset = df.copy(deep = True)
  y = reverse_log_transform(y_pred)
  dataset['GY'] = y

  return dataset

def update_control_vars(start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG):
  """Update control variables with user defined inputs.
  : params start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG: user defined parameters.
  """
  ControlVars.start_date = start_date
  ControlVars.end_date = end_date
  ControlVars.cultivar = cultivar
  ControlVars.PH = PH
  ControlVars.NLP = NLP
  ControlVars.NGL = NGL
  ControlVars.NS = NS
  ControlVars.IFP = IFP
  ControlVars.MHG = MHG

def retrieve_vars_from_global_context ():
  """Retrieve variables stored in global context"""
  start_date = ControlVars.start_date
  end_date = ControlVars.end_date
  cultivar = ControlVars.cultivar
  PH = ControlVars.PH
  NLP = ControlVars.NLP
  NGL = ControlVars.NGL
  NS = ControlVars.NS
  IFP = ControlVars.IFP
  MHG = ControlVars.MHG
  cluster_model_path = ControlVars.cluster_model_path
  lstm_model_path = ControlVars.lstm_model_path

  return start_date, end_date, cultivar, PH, NLP, NGL, NS, IFP, MHG, cluster_model_path, lstm_model_path
