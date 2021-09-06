# 
# Main class for core 
# 

# libs
import json
from core.mysql import Mysql_Connect
from core.request import RQ

class Parser:

    # constructor
    def __init__(self, link:str):
        
        # init modules
        self.DB = Mysql_Connect("192.168.111.37", "root", "dbnmjr031193", "boligsiden")
        self.RQ = RQ()

        # load data
        self.json = json.loads(self.RQ.Load(link))

        # buffered data
        self.sql_requests = []

        # process all data
        self.Process_All(self.json["result"]["items"])

        # send to db
        self.Send_To_Db(self.sql_requests)
    

    # Method for process all data array
    def Process_All(self, data):

        # loop for process array
        for item in data:
            self.Parse_One(item)

    # Method for parse one item data
    def Parse_One(self, item):
        # getting info
        link = self.Get_Dict_String('redirectLink', item)
        house_photo = self.Get_Dict_String('imageLink600X400', item)
        street = self.Get_Dict_String('address', item)
        post_index = self.Get_Dict_String('postal', item)
        city = self.Get_Dict_String('city', item)
        sell_period = self.Get_Dict_Int('salesPeriod', item)
        build_year = item['buildYear']
        energy_class = self.Get_Dict_String('energyMark', item)
        house_area = self.Get_Dict_Int('areaResidential', item)
        terittory_area = self.Get_Dict_Int('areaParcel', item)
        house_type = self.Get_Dict_String('itemTypeName', item)
        amount_rooms = self.Get_Dict_Int('numberOfRooms', item)
        price = self.Get_Dict_Int('paymentCash', item)
        price_per_meter = self.Get_Dict_Int('areaPaymentCash', item)
        price_tax = self.Get_Dict_Int('paymentExpenses', item)
        price_changes = self.Get_Dict_String('priceDevelopment', item)
        first_payment = self.Get_Dict_Int('downPayment', item)

        # create sql request
        sql_request = "INSERT INTO houses VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (link, house_photo, street, post_index,city, sell_period, build_year, energy_class, house_area, terittory_area,house_type, amount_rooms, price, price_per_meter, price_tax, price_changes, first_payment)
        
        # add data to buffer
        self.sql_requests.append(sql_request)

    # Getting string from dict
    def Get_Dict_String(self,key, checked_dict):

        # result (CPU model)
        result = ""

        # check for key
        if key in checked_dict:
            preprocess_string = checked_dict[key].replace("'", "")
            result = preprocess_string
        
        # result
        return result

    # Getting int from dict
    def Get_Dict_Int(self,key, checked_dict):

        # result (CPU model)
        result = 0

        # check for key
        if key in checked_dict:
            try:
                preprocess_string = checked_dict[key].replace(".", "")
                result = int(preprocess_string)
            except:
                print("Can not convert %s to int" % (checked_dict[key]))
        
        # result
        return result

    # update data in db
    def Send_To_Db(self, data_dict):
        # delete all old data from mysql database
        self.DB.I("DELETE FROM houses")

        # write all records to db
        for item in data_dict:

            # requests to db
            self.DB.I(item)





