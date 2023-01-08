import settrade_v2
from settrade_v2 import Investor
from settrade_v2.errors import SettradeError

investor = Investor(
                app_id="xwnx9UK7RXfYIsOM",                                 
                app_secret="AIdXVMSoOZ1mGxGy2aY2QPLbIScI5t6/+an1iW39Cxsc", 
                broker_id="SANDBOX",
                app_code="SANDBOX",
                is_auto_queue = False)

deri = investor.Derivatives(account_no="settrade-D")    
try:
    deri.get_account_info()
except SettradeError as e:
    print("---- error message  ----")
    print(e)
    print("---- error code ----")
    print(e.code)
    print("---- status code ----")
    print(e.status_code)