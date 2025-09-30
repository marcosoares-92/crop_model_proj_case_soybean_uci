"""CROP SIMULATOR
Simulate a Soybean production

Marco Cesar Prado Soares, Data Scientist Specialist @ Bayer Crop Science LATAM
marcosoares.feq@gmail.com
marco.soares@bayer.com
"""


# Check if the correct versions are installed
class CheckVersions:
  """Check if the versions of numpy, pandas, sklearn and tensorflow are correct. If not, set to the correct versions.
    This will prevent the simulator from crashing due to version updates that make the models unable to use
  """

  def __init__(self):
    """
      DEFINE COMMANDS (Bash script) and success messages and set timeout.
      : param: timeout (int): number of seconds to wait for a command to run, before considering error.
    """
    # This should be run before importing packages. That is why command line tools are used
    from subprocess import Popen, PIPE, TimeoutExpired
    # Run pip freeze to get all installed packages and their versions:
    proc = Popen(['pip', 'freeze'], stdout = PIPE, stderr = PIPE)
    out, error = proc.communicate()
    """ Split a package per line, to get a list like:
        ['absl-py==1.4.0', 'absolufy-imports==0.3.1', 'accelerate==1.10.1']
    """
    output = out.decode('utf-8').split("\n")
    pkgs_to_check = ['numpy', 'pandas', 'sklearn', 'tensorflow', 'scikit-learn']
    current_versions = {}

    for line in output:
      try: # Some outputs from Colab pip freeze are not in format pkg==version
        pkg, version = line.split("==")
        if (pkg in pkgs_to_check):
          current_versions[pkg] = version
      except:
        pass

    self.current_versions = current_versions
    # Update packages to check:
    self.pkgs_to_check = list(current_versions.keys())

    self.correct_versions = {
        'numpy': '2.0.2',
        'pandas': '2.2.2',
        'sklearn': '1.6.1',
        'tensorflow': '2.19.0',
        'scikit-learn': '1.6.1'
        }

  def check_versions (self):
    """
    Check if the versions of numpy, pandas, sklearn and tensorflow are correct. If not, set to the correct versions.
    """
    pkgs_to_correct  =[]
    for pkg in self.pkgs_to_check:
      if (self.current_versions[pkg] != self.correct_versions[pkg]):
        pkgs_to_correct.append(pkg)

    self.pkgs_to_correct = pkgs_to_correct
    return self

  def pip_command (self, pkg):
    """
    pkg (str): package name
    correct_version (str): correct version of the package
    """
    self.cmd_line = f"""pip install {pkg}=={self.correct_versions[pkg]} -q -q -q"""
    return self

  def get_cmds (self):
    """Get commands to run."""
    cmds = []
    for pkg in self.pkgs_to_correct:
      self = self.pip_command(pkg)
      cmds.append(self.cmd_line)

    self.cmds = cmds
    return self

  def run_pip (self, cmd_line):
    """Define a process to run from a command:
    """
    from subprocess import Popen, PIPE, TimeoutExpired

    proc = Popen(cmd_line.split(" "), stdout = PIPE, stderr = PIPE)
    """cmd_line = "pip install tensorflow==2.19.0 -q -q -q"
      will lead to the list ['pip', 'install', 'tensorflow==2.19.0', '-q', '-q', '-q']
      after splitting the string in whitespaces, what is done by .split(" ") method.
    """
    output, error = proc.communicate()

    return self

  def correct_package_versions (self):
    """
    Correct the versions of numpy, pandas, sklearn and tensorflow.
    """
    self = self.check_versions()
    self = self.get_cmds()
    for cmd_line in self.cmds:
      self = self.run_pip(cmd_line)

    return self

checker = CheckVersions()
checker = checker.correct_package_versions()

import numpy as np
import pandas as pd
import sklearn
import tensorflow as tf
from dataclasses import dataclass

# Now import other components

from .core import (
    run_simulation,
    visualize_yield,
    download_excel_with_data
)



def start_simulation(PT = True):
  """This function runs the following sequence of command line interface commands, 
    for copying the GitHub repository containing the simulator, models and packages to a local 
    repository named 'steelindustrysimulator' 
  
    It is equivalent to running the following command in a notebook's cell:
  
    ! git clone https://github.com/marcosoares-92/steelindustrysimulator 'steelindustrysimulator'
    
    The git clone documentation can be found in:
    https://git-scm.com/docs/git-clone

    : param: PT (boolean): if True, the start message is shown in Portuguese (BR).
    If False, it is shown in English.

  """

  from subprocess import Popen, PIPE, TimeoutExpired
  
  START_MSG = """Starting steel industry operation."""
  START_MSG_PT = """Iniciando operação da indústria de aço."""
  
  if (PT):
    START_MSG = START_MSG_PT

  proc = Popen(["git", "clone", "https://github.com/marcosoares-92/steelindustrysimulator", "steelindustrysimulator"], stdout = PIPE, stderr = PIPE)
  
  try:
      output, error = proc.communicate(timeout = 15)
      print (START_MSG)
  except:
      # General exception
      output, error = proc.communicate()
      print(f"Process with output: {output}, error: {error}.\n")


def digitaltwin_start_msg(PT = True):
    """When the Steel Industry Digital Twin is started, the following message is shown."""

    start_msg = """
        ----------------------------------------------------------------------
                          STEEL INDUSTRY DIGITAL TWIN TERMINAL


        Welcome to the Steel Industry Digital Twin!

        This simulator applies advanced AI (deep learning) technologies to reproduce the
        operation of a small-scale steel industry.

        The digital twin is designed to reproduce the behavior from a DAEWOO Steel Co. Ltd
        facility in Gwangyang, South Korea, which made its data public. 
        - This factory produces several types of coils, steel plates, and iron plates. 
        - The information on electricity consumption is held in a cloud-based system. 
        - The information on energy consumption of the industry is stored on the website of the 
        Korea Electric Power Corporation (pccs.kepco.go.kr); and the perspectives on daily, monthly, 
        and annual data are calculated and shown.

        All this information was used for creating the algorithms that will reproduce the energy
        consume behavior based on your user inputs.

        YOUR GOAL HERE IS TO MINIMIZE THE ENERGY CONSUMPTION, WHICH IS SHOWN IN kWh.


        ## For that, you will define:

        - The day of starting the plant simulation (which can be today).
        - The total days and hours for running the plant in the defined conditions
            - Default is 1 day and 0 hours, i.e., 24h of operation.
        
        - Plant operation parameters:
            - Lagging Current reactive power, in kVArh; 
            - Leading Current reactive power, in kVArh; 
            - tCO2(CO2), in ppm; 
            - Lagging Current power factor, in %;
            - Load Type: Light Load, Medium Load, Maximum Load.


        ## And will obtain the Response variable:
            - Energy consumption, in kWh

        - The simulator returns also the following information:
            - Leading Current Power factor, in %; 
            - Number of Seconds from midnight (NSM), in seconds (s); 
            - Week status: if the simulated day is 'Weekend' or 'Weekday'; 
            - Day of week: 'Sunday', 'Monday', ..., 'Saturday'. 
  
        ------------------------------------------------------------------------

    """

    start_msg_pt = """
        ----------------------------------------------------------------------
                          STEEL INDUSTRY DIGITAL TWIN TERMINAL


        Bem-vindo ao gêmeo digital (Digital Twin) da indústria siderúrgica!

         Este simulador aplica tecnologias avançadas de IA (deep learning) para reproduzir o
         operação de uma indústria siderúrgica de pequena escala.

         O gêmeo digital foi projetado para reproduzir o comportamento da fábrica da DAEWOO Steel Co.
         em Gwangyang, Coreia do Sul, que tornou seus dados públicos.
         - Esta fábrica produz diversos tipos de bobinas, chapas de aço e chapas de ferro.
         - As informações sobre o consumo de energia elétrica são mantidas em sistema baseado em nuvem.
         - As informações sobre o consumo de energia da indústria estão armazenadas no site da
         Corporação de Energia Elétrica da Coreia (pccs.kepco.go.kr); e as perspectivas diárias, mensais,
         e os dados anuais são calculados e mostrados.

         Todas essas informações foram utilizadas para a criação dos algoritmos que irão reproduzir o
         comportamento de consumo energético com base nas entradas do usuário.

         SEU OBJETIVO AQUI É MINIMIZAR O CONSUMO DE ENERGIA, QUE É MOSTRADO EM kWh.


         ## Para isso, você definirá:

         - O dia de início da simulação da planta (que pode ser hoje).
         - O total de dias e horas para operar a planta nas condições definidas
             - O padrão é 1 dia e 0 horas, ou seja, 24h de operação.
        
         - Parâmetros de operação da planta:
             - Potência reativa de corrente atrasada, em kVArh;
             - Potência reativa de corrente principal, em kVArh;
             - tCO2(CO2), em ppm;
             - Fator de potência da corrente atrasada, em %;
             - Tipo de Carga: Carga Leve ('Light_Load'), Carga Média ('Medium_Load'), Carga Máxima ('Maximum_Load').


         ## E obterá a variável Response:
             - Consumo de energia, em kWh

         - O simulador retorna também as seguintes informações:
             - Fator de potência de corrente principal, em %;
             - Número de Segundos a partir da meia-noite (NSM), em segundos (s);
             - Status da semana: se o dia simulado é Fim de semana (indicado como 'Weekend') ou 
             'Dia de semana' (indicado como 'Weekday'); 
             - Dia da semana: 'Domingo' (indicado como 'Sunday'), 'Segunda-feira' ('Monday'), 
             'Terça-feira' ('Tuesday'), 'Quarta-feira' ('Wednesday'), 'Quinta-feira' ('Thursday'),
             'Sexta-feira' ('Friday'), 'Sábado' ('Saturday').
   
        ------------------------------------------------------------------------

    """
    
    if (PT):
        start_msg = start_msg_pt

    print("\n")
    print(start_msg)


def start_digital_twin(PT = True):
    """Check if the files are in the directory and start the simulation:"""
    try:
        # In case the simulator was installed in the machine and the GitHub
        # is not downloaded, do it:
        start_simulation(PT = PT)
    
    except:
        pass

    digitaltwin_start_msg(PT = PT)