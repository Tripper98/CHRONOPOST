from data import Data

d = Data()

info_customer = d.get_info_cust("shipments","TELEM SARL")

print(info_customer[0])