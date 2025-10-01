"""CROP SIMULATOR
Simulate a Soybean production

Marco Cesar Prado Soares, Data Coordinator @ Bayer Crop Science LATAM
marcosoares.feq@gmail.com
marco.soares@bayer.com
"""

import numpy as np
import pandas as pd
import sklearn
import tensorflow as tf

# Now import other components

from .core import (
    ControlVars,
    run_simulation,
    visualize_yield,
    download_excel_with_data
 )

from .utils import update_control_vars


def cropsim_start_msg(PT = True):

    if (PT == False):
      ControlVars.language_pt = False
    
    if (ControlVars.language_pt == True):
      start_msg = """
        ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                          CROP SIMULATOR - PRODUÇÃO DE SOJA


          Bem-vindo ao Crop Simulator!

          Este simulador aplica tecnologias avançadas de IA (deep learning) para reproduzir o
          operação de uma produção de soja.

          O simulador foi projetado para reproduzir o comportamento do campo na Fazenda Pequizeiro, na Estação Experimental da Accert Pesquisa e Consultoria Agronômica, localizada a 10 km do município de Balsas, MA, Brasil.
          A localização geográfica é: latitude 07°31'57" S, longitude 46°02'08" W e altitude de aproximadamente 283 m.
          Os dados foram obtidos para a safra 2022/2023.
          - Artigo original em: https://doi.org/10.46420/TAES.e230005
          - Dados em: https://archive.ics.uci.edu/dataset/913/forty+soybean+cultivars+from+subsequent+harvests (doado em 28/10/2023)

          Alguns detalhes sobre a produção real:
          - O clima da região, segundo a classificação de Köppen, é tropical quente e úmido (Aw), com verões chuvosos e invernos secos.
          - A precipitação pluvial total anual atinge valores médios de 1175 mm.
          - O solo da área experimental foi classificado como Latossolo Amarelo de textura arenosa, com base no sistema brasileiro de classificação de solos.
          - A composição química do solo está descrita no artigo.
          - A dessecação foi realizada utilizando os produtos glifosato + Haloxifope P metil.
          - Após 15 dias, a soja foi semeada mecanicamente, utilizando semeadeira adubadora com mecanismo sulcador tipo haste (facão) para sistemas de plantio direto, a uma profundidade de aproximadamente 3 cm, com espaçamento de 0,50 m, e a quantidade de sementes variou conforme recomendação para cada cultivar.
          - A adubação de base consistiu apenas na aplicação de 200 kg/ha de fosfato monoamônio (MAP). Aos 30 DAE das plantas de soja, foram aplicados 120 kg/ha de K2O, cuja fonte foi o cloreto de potássio.
          - As sementes de soja foram tratadas com piraclostrobina + tiofanato metílico + fipronil na dose de 2 mL p.c./kg de semente inoculada com Bradyrhizobium japonicum. O inoculante líquido comercial Simbiose Nod Soja® foi utilizado na dose de 150 mL para 50 kg de sementes.
          - Durante o desenvolvimento da planta, os seguintes produtos foram utilizados para o manejo de plantas daninhas, pragas e doenças: glifosato, haloxifope p metil, piraclostrobina + epoxiconazol, picoxistrobina + benzovindiflupir, mancozebe, azoxistrobina + ciproconazol, teflubenzuron, clorpirifós, cipermetrina e imidacloprida + beta-ciflutrina.

          ## Para simular esta produção, você definirá:
          - O dia de início da simulação.
          - O dia de término da simulação.
          - O híbrido de soja utilizado - selecione uma entre 40 opções: 'NEO 760 CE', 'MANU IPRO', '77HO111I2X - GUAPORÉ', 'NK 7777 IPRO', 'GNS7900 IPRO - AMPLA', 'LTT 7901 IPRO', 'BRASMAX BÔNUS IPRO', '97Y97 IPRO', 'BRASMAX OLIMPO IPRO', 'LYNDA IPRO', 'NK 8100 IPRO', '82HO111 IPRO - HO COXIM IPRO', '83IX84RSF I2X', 'ADAPTA LTT 8402 IPRO', '98R30 CE', 'FORTALEZA IPRO', 'MONSOY 8330I2X', 'SUZY IPRO', 'TMG 22X83I2X', 'EXPANDE LTT 8301 IPRO', 'FORTALECE L090183 RR', '96R29 IPRO', '74K75RSF CE', 'FTR 3868 IPRO', 'GNS7700 IPRO', 'ELISA IPRO', '79I81RSF IPRO', 'NEO 790 IPRO', 'PAULA IPRO', 'FTR 3179 IPRO', 'LAT 1330BT', 'FTR 4280 IPRO', 'ATAQUE I2X', 'SYN2282IPRO', '82I78RSF IPRO', 'M 8644 IPRO', 'MONSOY M8606I2X', 'NK 8770 IPRO', 'FTR 4288 IPRO', 'FTR 3190 IPRO'
          
          ## Alguns parâmetros de cultivo que o usuário deve definir:
            - Altura da planta (PH, cm) - determinada da superfície do solo até a inserção da última folha com régua milimetrada
            - Inserção da primeira vagem (IFP, cm) - determinada da superfície do solo até a inserção do primeiro vegetal
            - Número de hastes e ramos (NLP, unidade) - por contagem manual
            - Número de grãos por planta (NGL, unidade) - por contagem manual
            - Número de grãos por vagem (NS, unidade) - por contagem manual
            - Massa de mil sementes (MHG, g)
            
          ## E irá obter a seguinte variável resposta:
              - Produtividade de grãos (GY, kg/ha) - determinada pela colheita da área útil da parcela e padronizada para um teor de umidade dos grãos de 13
          
          ## O simulador também retornará a seguinte informação:
            - Número de leguminosas por planta (NGP, unidade) – por contagem manual

        ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

      """

    else:

      start_msg = """
          ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                            CROP SIMULATOR - SOYBEAN PRODUCTION


          Welcome to the Crop Simulator!

          This simulator applies advanced AI (deep learning) technologies to reproduce the
          operation of a soybean production.

          The simulator is designed to reproduce the behavior the field at farm ‘Pequizeiro’, at the Experimental Station of
          “Accert Pesquisa e Consultoria Agronomica”, located 10 km from the municipality of Balsas, MA, Brazil.
          The geographic location is: latitude of 07°31’57” S, longitude 46° 02’08” W and an altitude of approximately 283 m. 
          Data was obtained for the harvest 2022/2023.
           - Original paper in: https://doi.org/10.46420/TAES.e230005
           - Data in: https://archive.ics.uci.edu/dataset/913/forty+soybean+cultivars+from+subsequent+harvests (donated in 28-10-2023)

          Some details regarding the real production:
          - The region's climate, according to Köppen’s classification, is hot and humid tropical (Aw), with rainy summers and dry winters. 
          - The total annual rainfall reaches average values of 1175 mm. 
          - The soil in the experimental area was classified as a Yellow Oxisol with a sandy texture based on the Brazilian soil classification system.
          - Soil chemical composition is described in the article
          - Desiccation was carried out using the products glyphosate + Haloxyfope P methyl. 
          - After 15 days, soybean was sown mechanically using a fertilizer seeder with a rod type furrowing mechanism (machete) for nil tillage systems at a depth of approximately 3 cm, with a spacing of 0.50 m and the quantity of seeds varied depending on recommendation for each cultivar.
          - Base fertilization consisted only of the application of 200 kg/ha of monoammonium phosphate (MAP). At 30 DAE of soybean plants, 120 kg/ha of K2O was applied, the source of which was potassium chloride.
          - Soybean seeds were treated with pyraclostrobin + methyl thiophanate + fipronil at a dose of 2 mL p.c/kg of seed inoculated with Bradyrhizobium japonicum . The commercial liquid inoculant Simbiose Nod Soja ® was used at a dose of 150 mL for 50 kg of seeds.
          - During plant development, the following products were used to manage weeds, pests and diseases: glyphosate, haloxyfop p methyl, pyraclostrobin + epoxiconazole, picoxystrobin + benzovindiflupyr, mancozeb, azoxystrobin + cyproconazole, teflubenzuron, chlorpy rifos, cypermethrin and imidacloprid + beta cyfluthrin.


          ## For simulating this production, you will define:
          - The day of starting the simulation.
          - The day of ending the simulation.
          - The cultivar used - select one from 40 options: 'NEO 760 CE', 'MANU IPRO', '77HO111I2X - GUAPORÉ', 'NK 7777 IPRO', 'GNS7900 IPRO - AMPLA', 'LTT 7901 IPRO', 'BRASMAX BÔNUS IPRO', '97Y97 IPRO', 'BRASMAX OLIMPO IPRO', 'LYNDA IPRO', 'NK 8100 IPRO', '82HO111 IPRO - HO COXIM IPRO', '83IX84RSF I2X', 'ADAPTA LTT 8402 IPRO', '98R30 CE', 'FORTALEZA IPRO', 'MONSOY 8330I2X', 'SUZY IPRO', 'TMG 22X83I2X', 'EXPANDE LTT 8301 IPRO', 'FORTALECE L090183 RR', '96R29 IPRO', '74K75RSF CE', 'FTR 3868 IPRO', 'GNS7700 IPRO', 'ELISA IPRO', '79I81RSF IPRO', 'NEO 790 IPRO', 'PAULA IPRO', 'FTR 3179 IPRO', 'LAT 1330BT', 'FTR 4280 IPRO', 'ATAQUE I2X', 'SYN2282IPRO', '82I78RSF IPRO', 'M 8644 IPRO', 'MONSOY M8606I2X', 'NK 8770 IPRO', 'FTR 4288 IPRO', 'FTR 3190 IPRO'
          
          ## Some crop parameters that the user must define:
              - Plant height (PH, cm) - determined from the soil surface to the insertion of the last leaf using a millimeter ruler 
              - Insertion of the first pod (IFP, cm) - determined from the soil surface to the insertion of the first vegetable 
              - Number of stems (NLP, unit) - through manual counting 
              - Number of grains per plant (NGL, unit) - through manual counting 
              - Number of grains per pod (NS, unit) - through manual counting 
              - Thousand seed weight (MHG, g) 

          ## And will obtain the Response variable:
              - Grain yield (GY, kg/ha) - determined by harvesting the useful area of the plot and standardized to a grain moisture level of 13%

          ## The simulator returns also the following information:
              - Number of legumes per plant (NGP, unit) - through manual counting 
    
          ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      
      """



    print("\n")
    print(start_msg)

cropsim_start_msg(PT = True)
