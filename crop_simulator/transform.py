from .utils import (
  calculate_frequency_features,
  apply_encoding,
  obtain_log_transformed_features,
  obtain_cluster_feature,
  get_dataframe_for_lstm
)

def feature_eng_pipeline(df, model_path):
  """
  df: dataframe that will be prepared for the LSTM Modelling
  model_path (str): path for the KMeans pkl file
  """
  dataset = df.copy(deep = True)
  dataset = calculate_frequency_features(dataset)
  dataset = apply_encoding(dataset)
  dataset = obtain_log_transformed_features(dataset)
  dataset = obtain_cluster_feature(dataset, model_path)
  dataset = get_dataframe_for_lstm(dataset)

  return dataset
