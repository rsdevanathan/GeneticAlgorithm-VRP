import pandas as pd
from instance import Instance
from evolution import Evolution
import json

customer = pd.read_csv("files/customer.csv")
store = pd.read_csv("files/store.csv")
vehicle = pd.read_csv("files/vehicle.csv")

instance = Instance(customer, store, vehicle)
Evolution(instance)
print(instance.GaStats)
print(instance.GaRoute.Trip)
print(instance.GaRoute.Assigned_Vehicles)
print(instance.GaRoute.Assigned_Customers)
print(instance.GaRoute.Unassigned_Customers)


assigned_customers = [instance.Customer[i].Customer_Id for i in instance.GaRoute.Assigned_Customers]
unassigned_customers = [instance.Customer[i].Customer_Id for i in instance.GaRoute.Unassigned_Customers]
assigned_vehicles = [instance.Vehicle[i].Vehicle_Id for i in instance.GaRoute.Assigned_Vehicles]

total_trips = len(instance.GaRoute.Trip)
assigned_vehicles_str = ','.join(map(str, instance.GaRoute.Assigned_Vehicles))


route_summary = pd.DataFrame({'Total_Customers':[instance.CustomerCount]
                                ,'Total_Vehicles':[instance.VehicleCount]
                                ,'Assigned_Vehicles':[len(instance.GaRoute.Assigned_Vehicles)]
                                ,'Assigned_Vehicles_List':[assigned_vehicles_str]
                                ,'Assigned_Customer_Count':[len(assigned_customers)]
                                ,'Unssigned_Customer_Count':[len(unassigned_customers)]
                                ,'Cost':[instance.GaRoute.Cost]})

route_summary.to_csv("files/route_summary.csv")



