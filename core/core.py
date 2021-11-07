# 
# Main class for core 
# 

# libs
import json
from core.mysql import Mysql_Connect
from core.request import RQ

class Parser:

    # constructor
    def __init__(self, start_from:int, amount_items:int):
        
        # init modules
        self.DB = Mysql_Connect("db", "root", "dbnmjr031193", "boligsiden")
        self.RQ = RQ()

        # variable for page number
        self.page_number = start_from

        # variable for items amount 
        self.amount_items = amount_items

        # Data to process (response from server)
        self.data_to_process = []

        # buffered data (to db)
        self.sql_requests = []
        self.data_storage = self.DB.IO("SELECT link, price FROM houses")

        # loop for load pages
        while True:

            # Main app link for download data
            link = "https://www.boligsiden.dk/address/api/addressresultproperty/getdata?p=%d&i=%d&s=12&sd=false&searchId=be399cf9cb1f4109aee64bd45f649156" % (self.page_number, self.amount_items)

            # load data
            self.json = json.loads(self.RQ.Load(link))

            # check for amount af houses in response
            if len(self.json["result"]["items"]) > 0:
                self.data_to_process += self.json["result"]["items"]
                #print("Loaded page %d | Length %d" % (self.page_number, len(self.json["result"]["items"])))
                self.page_number += 1

            else:
                break


        # process all data
        self.Process_All(self.data_to_process)

        # Update data in db
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
        self.sql_requests.append([link, price, sql_request])

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

        # write all records to db
        for item in data_dict:

            # main variable for deleting controll
            not_exist = True

            # load data from db
            for storage_item in self.data_storage:
                if item[0] in storage_item:
                    # change main controll variable
                    not_exist = False

                    # check for price and if exist contiue
                    if item[1] in storage_item:
                        break
                    # update
                    else:
                        self.DB.I("UPDATE houses SET price = '%d' WHERE link = '%s'" % (item[1], item[0]))
                        break
                
            # item not exist
            if not_exist:
                # requests to db
                self.DB.I(item[2])

        # delete houses that not exist
        for storage_item in self.data_storage:

            # main variable for deleting controll
            not_exist = True

            # second loop for searching
            for item in data_dict:
                if storage_item[0] in item:
                    # item exist
                    not_exist = False
                    break
            
            # if item not exist, delete
            if not_exist:
                self.DB.I("DELETE FROM houses WHERE link = '%s'" % (storage_item[0]))


