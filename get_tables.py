]]# API REFERENCE
# https://comtrade.un.org/data/doc/api

# API EDITOR
# https://comtrade.un.org/api/swagger/ui/index#!/Data/Data_GetData

# REGULAR SEARCH
# https://comtrade.un.org/data/



import pandas as pd
import requests
# GETTING REPORTER AREAS
# r
REPORTER_AREAS_URL = "https://comtrade.un.org/data/cache/reporterAreas.json"
reporter_areas_request = requests.get(url = REPORTER_AREAS_URL)
reporter_areas_data = reporter_areas_request.json()
# all_reporter_areas = list(filter(lambda x: x["id"] != "all", reporter_areas_data["results"]))
all_reporter_areas = list(filter(lambda x: x["id"], reporter_areas_data["results"]))
all_reporter_areas
len(all_reporter_areas)

# GETTING PARTNER AREAS
# p
PARTNER_AREAS_URL = "https://comtrade.un.org/data/cache/partnerAreas.json"
partner_areas_request = requests.get(url = PARTNER_AREAS_URL)
partner_areas_data = partner_areas_request.json()
# all_partner_areas = list(filter(lambda x: x["id"] != "all", partner_area_data["results"]))
all_partner_areas = list(filter(lambda x: x["id"], partner_area_data["results"]))
all_partner_areas

# GETTING TRADE REGIMES
# rg
TRADE_REGIMES_URL = "https://comtrade.un.org/data/cache/tradeRegimes.json"
trade_regimes_request = requests.get(url = TRADE_REGIMES_URL)
trade_regimes_data = trade_regimes_request.json()
all_trade_regimes = list(filter(lambda x: x["id"] != "all", trade_regimes_data["results"]))
all_trade_regimes

# TRADE DATA TYPE (commodities / services)
# type
["C", "S"]


# CLASSIFICATION CODES - CUSTOM MAKE
["TOTAL", "AG1", "AG2", "AG3", "AG4", "AG5", "AG6", "ALL"]

# CLASSIFICATION
# px
["HS", "H0", "H1", "H2", "H3", "H4", "ST", "S1", "S2", "S3", "S4", "BEC", "EB02"]


# TIME PERIOD - CUSTOM MAKE
# ps



# FREQUENCY
# freq
["A", "M"]

# FORMAT
# fmt
["json", ]







PEW = "https://comtrade.un.org/api/get?"
PARAMS = {"r": 56,
            "px": "HS",
            "ps": 2017,
            "p": 0,
            "rg": 1,
            "cc": "All",
            "max": 50000,
            "fmt": "json",
            "type": "C",
            "freq": "A",
            "head": "H"
            }
request_bod = requests.get(url = PEW, params = PARAMS)
main_data = request_bod.json()
main_data
len(main_data["dataset"])
# main_data
pew = pd.DataFrame(main_data["dataset"])
pew.info()



for i in pew.select_dtypes(include = ["object"]).columns:
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(i)
        print(pew[i].unique())
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

pew["rtTitle"].unique().shape
# for i in data.drop(["Признаки незнания бизнеса", "name"], axis = 1).select_dtypes(include = ["object"]).columns:
#     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#         print(data.groupby([i])["TypeClient"].count())
#     print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
