from .transform import feature_eng_pipeline
from .utils import (run_model, update_df)

def prediction_pipeline(df, cluster_model_path, lstm_model_path):
  """
  df: dataframe that will be prepared for the LSTM Modelling
  cluster_model_path (str): path for the KMeans pkl file
  lstm_model_path (str): path for the .keras model file
  """
  transformed_df = feature_eng_pipeline (df, cluster_model_path)
  y_pred = run_model (lstm_model_path, transformed_df)
  dataset = update_df (df, y_pred)

  if (ControlVars.language_pt):
    # Modify columns labels
    """
    - Altura da planta (PH, cm) – determinada da superfície do solo até a inserção da última folha com régua milimetrada
    - Inserção da primeira vagem (IFP, cm) – determinada da superfície do solo até a inserção do primeiro vegetal
    - Número de hastes e ramos (NLP, unidade) – por contagem manual
    - Número de leguminosas por planta (NGP, unidade) – por contagem manual
    - Número de grãos por planta (NGL, unidade) – por contagem manual
    - Número de grãos por vagem (NS, unidade) – por contagem manual
    - Massa de mil sementes (MHG, g)
    - Produtividade de grãos (GY, kg/ha) – determinada pela colheita da área útil da parcela e padronizada para um teor de umidade dos grãos de 13
    """
    dataset = dataset.rename(columns = {'timestamp': 'dia', 'Cultivar': 'hibrido_de_soja', 'PH': 'altura_da_planta',
                                        'NLP': 'hastes_e_ramos', 'NGP': 'leguminosas_por_planta',
                                        'NGL': 'graos_por_planta', 'NS': 'graos_por_vagem',
                                        'IFP': 'insercao_da_primeira_vagem', 'MHG': 'massa_de_mil_sementes',
                                        'GY': 'produtividade_de_graos'})

  try:
    print("\n")
    # only works in Jupyter Notebook:
    from IPython.display import display
    display(dataset.head(10))

  except: pass

  return dataset