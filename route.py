import random


class Route:

    def __init__(self, instance, customers):
        self.Trip = {}
        self.Assigned_Vehicles = []
        self.Assigned_Customers = []
        ##print(customers)
        for customer in customers:
            store_id = instance.Customer[customer].Store_Id
            store = [store for store, store_values in instance.Store.items() if store_values.Store_Id == store_id][0]
            ##print("CI:", customer, store)
            store_trips = [trip for trip, trip_values in self.Trip.items() if store in trip_values['Store']]
            other_trips = [trip for trip, trip_values in self.Trip.items() if trip not in store_trips]
            ##print("CI:", store_trips, other_trips)
            store_trip_exists = True if len(store_trips) > 0 else False
            other_trip_exists = True if len(other_trips) > 0 else False
            pack_size = instance.Customer[customer].Pack_Size
            penalty_time = 0
            customer_not_assigned = True
            while customer_not_assigned and penalty_time < 120:
                if store_trip_exists:
                    ##print("1")
                    for trip in store_trips:
                        vehicle = self.Trip[trip]['Vehicle']
                        estimated_distance = self.Trip[trip]['Distance'] + \
                                             instance.Distance[(self.Trip[trip]['Location'][-1], customer)]
                        estimated_time = self.Trip[trip]['Time'] + \
                                         instance.Time[(self.Trip[trip]['Location'][-1], customer)]
                        store_leg = self.Trip[trip]['Location_Load'][self.Trip[trip]['Location'].index(store):]
                        new_trip_load = [i + pack_size if i in store_leg else i
                                         for i in self.Trip[trip]['Location_Load']]
                        capacity_available = True if max(new_trip_load) <= instance.Vehicle[vehicle].Capacity else False
                        within_time = True if instance.Customer[customer].Due_Time + penalty_time >= estimated_time \
                            else False
                        if capacity_available and within_time:
                            self.Trip[trip]['Time'] = self.Trip[trip]['Time'] + estimated_distance
                            self.Trip[trip]['Distance'] = self.Trip[trip]['Distance'] + estimated_time
                            self.Trip[trip]['Location'].append(customer)
                            self.Trip[trip]['Location_Due_Time'].append(instance.Customer[customer].Due_Time)
                            self.Trip[trip]['Location_Arrival_Time'].append(round(estimated_time))
                            new_trip_load.append(new_trip_load[-1] - pack_size)
                            self.Trip[trip]['Location_Load'] = new_trip_load
                            penalty_cost = penalty_time * instance.Customer[customer].Customer_Priority
                            mileage_cost = estimated_distance * instance.Vehicle[vehicle].Mileage_Cost
                            fixed_cost = (estimated_time / 60) * instance.Vehicle[vehicle].Fixed_Cost
                            self.Trip[trip]['Cost'] = self.Trip[trip]['Cost'] + penalty_cost + mileage_cost + fixed_cost
                            self.Trip[trip]['Position'] = instance.Customer[customer].Position
                            self.Assigned_Customers.append(customer)
                            ##print("Assigned")
                            customer_not_assigned = False
                            break
                if customer_not_assigned and other_trip_exists:
                    ##print("2")
                    for trip in other_trips:
                        vehicle = self.Trip[trip]['Vehicle']
                        store_estimated_distance = self.Trip[trip]['Distance'] + \
                                                   instance.Distance[(self.Trip[trip]['Location'][-1], store)]
                        estimated_distance = store_estimated_distance + instance.Distance[(store, customer)]
                        store_estimated_time = self.Trip[trip]['Time'] + \
                                               instance.Time[(self.Trip[trip]['Location'][-1], store)]
                        estimated_time = store_estimated_time + instance.Time[(store, customer)]
                        capacity_available = True if self.Trip[trip]['Location_Load'][-1] + pack_size <= \
                                                     instance.Vehicle[vehicle].Capacity else False
                        within_time = True if instance.Customer[customer].Due_Time + penalty_time >= estimated_time \
                            else False
                        ##print(self.Trip[trip]['Location_Load'][-1] + pack_size)
                        ##print(instance.Vehicle[vehicle].Capacity)
                        ##print(instance.Customer[customer].Due_Time + penalty_time)
                        ##print(estimated_time)
                        if capacity_available and within_time:
                            self.Trip[trip]['Store'].append(store)
                            self.Trip[trip]['Time'] = self.Trip[trip]['Time'] + estimated_time
                            self.Trip[trip]['Distance'] = self.Trip[trip]['Distance'] + estimated_distance
                            self.Trip[trip]['Location'].extend([store, customer])
                            self.Trip[trip]['Location_Arrival_Time'].extend([round(store_estimated_time),
                                                                             round(estimated_time)])
                            self.Trip[trip]['Location_Due_Time'].extend([0, instance.Customer[customer].Due_Time])
                            self.Trip[trip]['Location_Load'].extend \
                                ([self.Trip[trip]['Location_Load'][-1] + pack_size,
                                  self.Trip[trip]['Location_Load'][-1]])
                            penalty_cost = penalty_time * instance.Customer[customer].Customer_Priority
                            mileage_cost = estimated_distance * instance.Vehicle[vehicle].Mileage_Cost
                            fixed_cost = (estimated_time / 60) * instance.Vehicle[vehicle].Fixed_Cost
                            self.Trip[trip]['Cost'] = self.Trip[trip]['Cost'] + penalty_cost + mileage_cost + fixed_cost
                            self.Trip[trip]['Position'] = instance.Customer[customer].Position
                            self.Assigned_Customers.append(customer)
                            customer_not_assigned = False
                            ##print("Assigned")
                            break
                if customer_not_assigned:
                    ##print("3")
                    ##print(self.Assigned_Vehicles)
                    vehicle_list = [v for v in list(instance.Vehicle.keys()) if v not in self.Assigned_Vehicles]
                    random.shuffle(vehicle_list)
                    next_trip = len(self.Trip)
                    for vehicle in vehicle_list:
                        store_estimated_distance = instance.Distance[(vehicle, store)]
                        estimated_distance = store_estimated_distance + instance.Distance[(store, customer)]
                        store_estimated_time = instance.Time[(vehicle, store)]
                        estimated_time = store_estimated_time + instance.Time[(store, customer)]
                        capacity_available = True if pack_size <= instance.Vehicle[vehicle].Capacity else False
                        within_time = True if instance.Customer[customer].Due_Time + penalty_time >= estimated_time \
                            else False
                        if capacity_available and within_time:
                            self.Assigned_Vehicles.append(vehicle)
                            self.Trip[next_trip] = {}
                            self.Trip[next_trip]['Vehicle'] = vehicle
                            self.Trip[next_trip]['Store'] = [store]
                            self.Trip[next_trip]['Time'] = estimated_time
                            self.Trip[next_trip]['Distance'] = estimated_distance
                            self.Trip[next_trip]['Location'] = [store, customer]
                            self.Trip[next_trip]['Location_Arrival_Time'] = [round(store_estimated_time),
                                                                             round(estimated_time)]
                            self.Trip[next_trip]['Location_Due_Time'] = [0, instance.Customer[customer].Due_Time]
                            self.Trip[next_trip]['Location_Load'] = [pack_size, 0]
                            penalty_cost = penalty_time * instance.Customer[customer].Customer_Priority
                            mileage_cost = estimated_distance * instance.Vehicle[vehicle].Mileage_Cost
                            fixed_cost = (estimated_time / 60) * instance.Vehicle[vehicle].Fixed_Cost
                            self.Trip[next_trip]['Cost'] = penalty_cost + mileage_cost + fixed_cost
                            self.Trip[next_trip]['Position'] = instance.Customer[customer].Position
                            self.Assigned_Customers.append(customer)
                            customer_not_assigned = False
                            ##print("Assigned")
                            break
                penalty_time = penalty_time + 30

        self.Unassigned_Customers = [customer for customer in instance.CustomerList if customer not in
                                     self.Assigned_Customers]
        # ##print(self.Unassigned_Customers)
        unassigned_cost = len(self.Unassigned_Customers) * 1000
        self.Cost = unassigned_cost + sum([value['Cost'] for trip, value in self.Trip.items()])
        self.Fitness = 1 / self.Cost

    def insert_customer(self, instance, customer):
        store_id = instance.Customer[customer].Store_Id
        customer_store = \
            [store for store, store_values in instance.Store.items() if store_values.Store_Id == store_id][0]
        additional_load = instance.Customer[customer].Pack_Size
        minimum_additional_distance = 9999
        location_insert = False
        insert_position = 0
        new_arrival_time = []
        new_trip_load = []
        for trip_pos, trip in self.Trip.items():
            trip_stores = [i for i in trip['Location'] if i[0] == "S"]
            if customer_store in trip_stores:
                customer_store_pos = trip['Location'].index(customer_store)
                for i, _ in enumerate(trip['Location']):
                    if i <= customer_store_pos:
                        continue
                    else:
                        new_leg1_distance = instance.Distance[(trip['Location'][i - 1], customer)]
                        new_leg2_distance = instance.Distance[(customer, trip['Location'][i])]
                        new_leg_distance = new_leg1_distance + new_leg2_distance
                        old_leg_distance = instance.Distance[(trip['Location'][i - 1], trip['Location'][i])]
                        additional_distance = new_leg_distance - old_leg_distance

                        new_leg1_time = instance.Time[(trip['Location'][i - 1], customer)]
                        new_leg2_time = instance.Time[(customer, trip['Location'][i])]
                        new_leg_time = new_leg1_time + new_leg2_time
                        old_leg_time = instance.Time[(trip['Location'][i - 1], trip['Location'][i])]
                        additional_time = new_leg_time - old_leg_time
                        ##print(trip)
                        ##print(trip['Location_Arrival_Time'])
                        ##print(i)
                        ##print(trip['Location_Arrival_Time'][i:])
                        new_arrival_time = [l + additional_time if l in trip['Location_Arrival_Time'][i:]
                                            else l for l in trip['Location_Arrival_Time']]
                        customer_estimated_time = new_arrival_time[i - 1] + new_leg1_time

                        new_trip_load = [m + additional_load if m in trip['Location_Load'][customer_store_pos:i - 1]
                                         else m for m in trip['Location_Load']]
                        customer_estimated_load = new_trip_load[i - 1] - additional_load
                        capacity_available = True if max(new_trip_load) <= instance.Vehicle[
                            trip['Vehicle']].Capacity else False
                        other_customer_due_time_cnt = 0
                        for k, l in enumerate(trip['Location']):
                            if l[0] == "S":
                                other_customer_due_time_cnt += 1
                            else:
                                if trip['Location_Due_Time'][k] > new_arrival_time[k]:
                                    other_customer_due_time_cnt += 1

                        other_customer_within_time = True if other_customer_due_time_cnt == len(trip['Location']) \
                            else False
                        this_customer_within_time = True if instance.Customer[customer].Due_Time > \
                                                            customer_estimated_time else False

                        within_time = other_customer_within_time and this_customer_within_time

                        if capacity_available and within_time and additional_distance < minimum_additional_distance:
                            insert_position = i
                            minimum_additional_distance = additional_distance
                            location_insert = True

            if location_insert:
                self.Trip[trip_pos]['Location'].insert(insert_position, customer)
                self.Trip[trip_pos]['Location_Due_Time'].insert(insert_position, additional_load)
                new_arrival_time.insert(insert_position, customer_estimated_time)
                self.Trip[trip_pos]['Location_Arrival_Time'] = new_arrival_time
                new_trip_load.insert(insert_position, customer_estimated_load)
                self.Trip[trip_pos]['Location_Load'] = new_trip_load

                additional_mileage_cost = additional_distance * instance.Vehicle[self.Trip[trip_pos]['Vehicle']].Mileage_Cost
                additional_fixed_cost = (additional_time / 60) * instance.Vehicle[self.Trip[trip_pos]['Vehicle']].Fixed_Cost
                self.Trip[trip_pos]['Cost'] = self.Trip[trip_pos]['Cost'] + additional_mileage_cost + additional_fixed_cost
                self.Assigned_Customers.append(customer)
                break

        if not location_insert:
            vehicle_list = [v for v in list(instance.Vehicle.keys()) if v not in self.Assigned_Vehicles]
            random.shuffle(vehicle_list)
            next_trip = len(self.Trip)
            for vehicle in vehicle_list:
                store_estimated_distance = instance.Distance[(vehicle, customer_store)]
                estimated_distance = store_estimated_distance + instance.Distance[(customer_store, customer)]
                store_estimated_time = instance.Time[(vehicle, customer_store)]
                estimated_time = store_estimated_time + instance.Time[(customer_store, customer)]
                capacity_available = True if instance.Customer[customer].Pack_Size <= instance.Vehicle[vehicle].Capacity \
                    else False
                within_time = True if instance.Customer[customer].Due_Time >= estimated_time \
                    else False
                if capacity_available and within_time:
                    next_trip_pos = len(self.Trip)
                    self.Trip[next_trip_pos] = {}
                    ###print(self.Trip)
                    self.Trip[next_trip_pos]['Vehicle'] = vehicle
                    self.Trip[next_trip_pos]['Store'] = [customer_store]
                    self.Trip[next_trip_pos]['Location'] = [customer_store, customer]
                    self.Trip[next_trip_pos]['Location_Due_Time'] = [0, instance.Customer[customer].Due_Time]
                    self.Trip[next_trip_pos]['Location_Arrival_Time'] = [0, instance.Time[(customer_store, customer)]]
                    self.Trip[next_trip_pos]['Location_Load'] = [additional_load, 0]
                    mileage_cost = (store_estimated_distance + estimated_distance) * instance.Vehicle[
                        self.Trip[next_trip_pos]['Vehicle']].Mileage_Cost
                    fixed_cost = ((store_estimated_time + estimated_time) / 60) * instance.Vehicle[
                        self.Trip[next_trip_pos]['Vehicle']].Fixed_Cost
                    self.Trip[next_trip_pos]['Cost'] = mileage_cost + fixed_cost
                    self.Assigned_Customers.append(customer)
                    self.Assigned_Vehicles.append(vehicle)
                    break
        self.Unassigned_Customers = [customer for customer in instance.CustomerList if customer not in
                                     self.Assigned_Customers]
        unassigned_cost = len(self.Unassigned_Customers) * 1000
        self.Cost = unassigned_cost + sum([value['Cost'] for trip, value in self.Trip.items()])
        self.Fitness = 1 / self.Cost


    def remove_customer(self, instance, customer):
        ###print(self.Trip)
        for trip_pos, trip in self.Trip.items():
            if customer in trip['Location']:
                store_id = instance.Customer[customer].Store_Id
                customer_store = \
                    [store for store, store_values in instance.Store.items() if store_values.Store_Id == store_id][0]
                customer_pos = trip['Location'].index(customer)
                customer_store_pos = trip['Location'].index(customer_store)

                remove_pack_size = instance.Customer[customer].Pack_Size

                if customer_pos == len(self.Trip[trip_pos]['Location_Arrival_Time']) - 1:
                    self.Trip[trip_pos]['Location'].pop(customer_pos)
                    self.Trip[trip_pos]['Location_Due_Time'].pop(customer_pos)
                    self.Trip[trip_pos]['Location_Arrival_Time'].pop(customer_pos)
                    distance_saved = instance.Distance[(trip['Location'][customer_pos - 1],customer)]
                    time_saved = instance.Time[(trip['Location'][customer_pos - 1], customer)]
                else:
                    new_time = instance.Time[(trip['Location'][customer_pos - 1], trip['Location'][customer_pos + 1])]
                    old_time = instance.Time[(trip['Location'][customer_pos - 1], customer)] \
                               + instance.Time[(customer, trip['Location'][customer_pos + 1])]
                    time_saved = old_time - new_time

                    new_distance = instance.Distance[(trip['Location'][customer_pos - 1], trip['Location'][customer_pos + 1])]
                    old_distance = instance.Distance[(trip['Location'][customer_pos - 1], customer)] \
                               + instance.Distance[(customer, trip['Location'][customer_pos + 1])]
                    distance_saved = old_distance - new_distance

                    self.Trip[trip_pos]['Location'].pop(customer_pos)
                    self.Trip[trip_pos]['Location_Due_Time'].pop(customer_pos)

                    self.Trip[trip_pos]['Location_Arrival_Time'] = [i -time_saved if i in self.Trip[trip_pos][
                                                                            'Location_Arrival_Time'][customer_pos + 1:]
                                                                    else i for i in
                                                                    self.Trip[trip_pos]['Location_Arrival_Time']]
                    self.Trip[trip_pos]['Location_Arrival_Time'].pop(customer_pos)
                self.Trip[trip_pos]['Location_Load'] = [
                    i - remove_pack_size if i in self.Trip[trip_pos]['Location_Load'][
                                                 customer_store_pos:customer_pos]
                    else i for i in self.Trip[trip_pos]['Location_Load']]
                self.Trip[trip_pos]['Location_Load'].pop(customer_pos)

                saved_mileage_cost = distance_saved * instance.Vehicle[
                    self.Trip[trip_pos]['Vehicle']].Mileage_Cost
                saved_fixed_cost = (time_saved / 60) * instance.Vehicle[
                    self.Trip[trip_pos]['Vehicle']].Fixed_Cost
                self.Trip[trip_pos]['Cost'] = self.Trip[trip_pos][
                                                  'Cost'] + saved_mileage_cost + saved_fixed_cost
                assigned_pos = self.Assigned_Customers.index(customer)
                self.Assigned_Customers.pop(assigned_pos)
                break
        self.Unassigned_Customers = [customer for customer in instance.CustomerList if customer not in
                                     self.Assigned_Customers]
        unassigned_cost = len(self.Unassigned_Customers) * 1000
        self.Cost = unassigned_cost + sum([value['Cost'] for trip, value in self.Trip.items()])
        self.Fitness = 1 / self.Cost