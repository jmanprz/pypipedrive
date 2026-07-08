import os
import pprint as pp

if os.environ.get("PIPEDRIVE_API_TOKEN") is None:
    os.environ["PIPEDRIVE_API_TOKEN"] = "your_api_token"

from pypipedrive.api import Api

api = Api()
# print(api)

from pypipedrive.api import V1, V2

from pypipedrive.models import Deals
pp.pprint(Deals.search(term="TEST"), version=V2)

# from pypipedrive.models import ItemSearch
# pp.pprint(ItemSearch.get(params=dict(term="TEST")))

# from pypipedrive.models import Stages

# pp.pprint(Stages.get(id=194).to_record())
# s = Stages.all()
# for e in s:
#     pp.pprint(e.to_record())

# from pypipedrive.models import Subscriptions
# pp.pprint(Subscriptions.get(id=1))

# from pypipedrive.models import ActivityFields
# pp.pprint(ActivityFields.all())

from pypipedrive.models import Activities
a = Activities.get(id=12506, version=V1)
pp.pprint(a.to_record())
a = Activities.get(id=12506, version=V2)
pp.pprint(a.to_record())


# # print(Deals.all())
# d = Deals(id=2282)
# d.probability = 100
# pp.pprint(d.to_record())
# d.fetch()
# pp.pprint(d.to_record())