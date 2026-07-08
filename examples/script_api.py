import sys
import os
import json
from dotenv import load_dotenv
load_dotenv()
from pypipedrive import Api
from pprint import pprint as pp

from pypipedrive.models import Deals

deal_id = 1
# Repo root (one level above examples/), so fixtures land in tests/sample_data/.
base_path = os.path.dirname(os.path.dirname(__file__))

d1 = Deals.get(deal_id, version="v1")
d2 = Deals.get(deal_id, version="v2")
# dd = Deals.all()
PATH_SAMPLE_DATA = f"{base_path}/tests/sample_data/"
json.dump(d1.to_record(), open(f"{PATH_SAMPLE_DATA}V1/Deal.json", "w"), indent=4)
json.dump(d2.to_record(), open(f"{PATH_SAMPLE_DATA}V2/Deal.json", "w"), indent=4)
pp(d1.to_record())
pp(d2.to_record())
# pp(len(dd))