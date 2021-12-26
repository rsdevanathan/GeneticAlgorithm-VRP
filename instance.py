import pandas as pd


class Customer:

    def __init__(self, customer_dict):
        self.__dict__ = customer_dict


class Vehicle:

    def __init__(self, vehicle_dict):
        self.__dict__ = vehicle_dict


class Store:

    def __init__(self, store_dict):
        self.__dict__ = store_dict


class Location:

    def __init__(self, location_dict):
        self.__dict__ = location_dict


class Instance:

    def calculateDistance(self, l1, l2):
        return ((self.Location[l1].Position[0] - self.Location[l2].Position[0]) ** 2
                + (self.Location[l1].Position[1] - self.Location[l2].Position[1]) ** 2) ** 0.5

    def __init__(self, customer, store, vehicle):
        customer["Customer_Index"] = "C" + customer.index.astype(str)
        store["Store_Index"] = "S" + store.index.astype(str)
        vehicle["Vehicle_Index"] = "V" + vehicle.index.astype(str)

        customer['Position'] = list(zip(customer.Latitude, customer.Longitude))
        store['Position'] = list(zip(store.Latitude, store.Longitude))
        vehicle['Position'] = list(zip(vehicle.Latitude, vehicle.Longitude))

        customer = customer.drop(['Latitude', 'Longitude'], axis=1)
        store = store.drop(['Latitude', 'Longitude'], axis=1)
        vehicle = vehicle.drop(['Latitude', 'Longitude'], axis=1)

        customer_location = customer[["Customer_Index", "Position"]]
        customer_location = customer_location.rename(columns={"Customer_Index": "Location_Index"})
        customer_location["Location_Type"] = "Customer"

        store_location = store[["Store_Index", "Position"]]
        store_location = store_location.rename(columns={"Store_Index": "Location_Index"})
        store_location["Location_Type"] = "Store"

        vehicle_location = vehicle[["Vehicle_Index", "Position"]]
        vehicle_location = vehicle_location.rename(columns={"Vehicle_Index": "Location_Index"})
        vehicle_location["Location_Type"] = "Vehicle"

        cust_store = customer.groupby("Store_Id").agg({'Customer_Id': 'count', 'Pack_Size': 'sum',
                                                       'Special_Handling': 'count'}).reset_index(drop=False)
        cust_store.columns = ["Store_Id", "Customer_Count", "Total_Pack_Size", 'Special_Handling_Count']
        store_new = store.merge(cust_store, how="inner", on='Store_Id')

        location = pd.concat([store_location, customer_location,vehicle_location], axis=0).reset_index(drop=True)

        vehicle_dict = vehicle.groupby("Vehicle_Index").apply(lambda dfg: dfg.to_dict(orient='records')[0]).to_dict()
        store_dict = store_new.groupby("Store_Index").apply(lambda dfg: dfg.to_dict(orient='records')[0]).to_dict()
        customer_dict = customer.groupby("Customer_Index").apply(lambda dfg: dfg.to_dict(orient='records')[0]).to_dict()
        location_dict = location.groupby("Location_Index").apply(lambda dfg: dfg.to_dict(orient='records')[0]).to_dict()

        self.VehicleCount = vehicle['Vehicle_Index'].count()
        self.StoreCount = store['Store_Index'].count()
        self.CustomerCount = customer['Customer_Index'].count()
        self.LocationCount = location['Location_Index'].count()
        self.VehicleList = vehicle['Vehicle_Index'].to_list()
        self.StoreList = store['Store_Index'].to_list()
        self.CustomerList = customer['Customer_Index'].to_list()
        self.LocationList = location['Location_Index'].to_list()
        self.Customer = {}
        self.Store = {}
        self.Vehicle = {}
        self.Location = {}
        self.Distance = {}
        self.Time = {}
        self.GaStats = {}
        self.GaRoute = {}
        for key, value in customer_dict.items():
            self.Customer[key] = Customer(value)
        for key, value in store_dict.items():
            self.Store[key] = Store(value)
        for key, value in vehicle_dict.items():
            self.Vehicle[key] = Vehicle(value)
        for key, value in location_dict.items():
            self.Location[key] = Location(value)
        for l1 in self.Location.keys():
            for l2 in self.Location.keys():
                self.Distance[(l1, l2)] = round(self.calculateDistance(l1, l2),1)
                self.Time[(l1, l2)] = round(self.Distance[(l1, l2)] * 5,1)

