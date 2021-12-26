import random
from route import Route
import configparser
from copy import deepcopy


class Evolution:

    def __init__(self, instance):
        config = configparser.ConfigParser()
        config.read('files/params.ini')
        ga_params = config['GA_PARAMS']
        self.PopulationSize = int(ga_params['population_size'])
        self.MutationProbability = float(ga_params['mutation_probability'])
        self.BcrcProbability = float(ga_params['bcrc_probability'])
        self.GenerationCount = int(ga_params['generation_count'])
        self.EliteCount = int(float(ga_params['elite_percentage']) * self.PopulationSize)
        if ((self.PopulationSize % 2) == 0 and ((self.EliteCount % 2) != 0)) or \
                ((self.PopulationSize % 2) != 0 and ((self.EliteCount % 2) == 0)):
            self.EliteCount = self.EliteCount - 1
        self.RouletteCount = self.PopulationSize - self.EliteCount
        self.Population = {}
        self.Parent = {}
        self.Offspring = {}
        self.create_population(instance)

        print("Starting Evolution")

        for generation in range(self.GenerationCount):
            print(f'-- Generation {generation} --')
            print("01")
            print(len(self.Population[0].Trip), self.Population[0].Fitness,self.Population[0].Unassigned_Customers)
            print(len(self.Population[1].Trip), self.Population[1].Fitness,self.Population[1].Unassigned_Customers)
            print(len(self.Population[2].Trip), self.Population[2].Fitness,self.Population[2].Unassigned_Customers)
            print(len(self.Population[3].Trip), self.Population[3].Fitness,self.Population[3].Unassigned_Customers)
            print(len(self.Population[4].Trip), self.Population[4].Fitness,self.Population[4].Unassigned_Customers)
            self.roulette_selection()
            #print("02")
            #print(len(self.Population[0].Trip), self.Population[0].Fitness,self.Population[0].Unassigned_Customers)
            #print(len(self.Population[1].Trip), self.Population[1].Fitness,self.Population[1].Unassigned_Customers)
            #print(len(self.Population[2].Trip), self.Population[2].Fitness,self.Population[2].Unassigned_Customers)
            #print(len(self.Population[3].Trip), self.Population[3].Fitness,self.Population[3].Unassigned_Customers)
            #print(len(self.Population[4].Trip), self.Population[4].Fitness,self.Population[4].Unassigned_Customers)
            #print(len(self.Parent))
            crossover_choice = random.random()
            if crossover_choice < self.BcrcProbability:
                self.route_crossover_bcrc(instance)
            #print("03")
            #print(len(self.Population[0].Trip), self.Population[0].Fitness, self.Population[0].Unassigned_Customers)
            #print(len(self.Population[1].Trip), self.Population[1].Fitness, self.Population[1].Unassigned_Customers)
            #print(len(self.Population[2].Trip), self.Population[2].Fitness, self.Population[2].Unassigned_Customers)
            #print(len(self.Population[3].Trip), self.Population[3].Fitness, self.Population[3].Unassigned_Customers)
            #print(len(self.Population[4].Trip), self.Population[4].Fitness, self.Population[4].Unassigned_Customers)
            mutation_choice = random.random()
            if mutation_choice < self.MutationProbability:
                self.route_mutant(instance)
            #print("04")
            ##print(len(self.Population[0].Trip), self.Population[0].Fitness,self.Population[0].Unassigned_Customers)
            #print(len(self.Population[1].Trip), self.Population[1].Fitness,self.Population[1].Unassigned_Customers)
            #print(len(self.Population[2].Trip), self.Population[2].Fitness,self.Population[2].Unassigned_Customers)
            #print(len(self.Population[3].Trip), self.Population[3].Fitness,self.Population[3].Unassigned_Customers)
            #print(len(self.Population[4].Trip), self.Population[4].Fitness,self.Population[4].Unassigned_Customers)
            #print("before e")
            # print(self.Offspring)
            #print((self.Offspring[0].Fitness))
            #print((self.Offspring[1].Fitness))
            #print((self.Offspring[2].Fitness))
            #print((self.Offspring[3].Fitness))
            self.elite_selection()
            # print("04")
            # print(self.Offspring)
            #print("after e")
            ##print((self.Offspring[0].Fitness))
            #print((self.Offspring[1].Fitness))
            #print((self.Offspring[2].Fitness))
            #print((self.Offspring[3].Fitness))
            #print((self.Offspring[4].Fitness))
            _, best_route = self.best_selection()
            self.Population = deepcopy(self.Offspring)
            self.Offspring = {}


            instance.GaStats[generation] = {}
            instance.GaStats[generation]['Best Route'] = ','.join(map(str, best_route.Trip))
            # instance.GaStats[generation]['Assigned'] = ','.join(map(str, best_route.Assigned_Customers))
            # instance.GaStats[generation]['Unassigned'] = ','.join(map(str, best_route.Unassigned_Customers))
            instance.GaStats[generation]['Max_Fitness'] = best_route.Fitness
        print("Completed Evolution")
        instance.GaRoute = best_route

    def create_population(self, instance):
        # #print("pop")
        cl = instance.CustomerList
        for i in range(self.PopulationSize):
            random.shuffle(cl)
            self.Population[i] = Route(instance, cl)

    def roulette_selection(self):
        population_copy = deepcopy(self.Population)
        sum_fit = sum([route.Fitness for route_id, route in self.Population.items()])
        for i in range(self.RouletteCount):
            pick = random.uniform(0, sum_fit)
            prob = 0
            for j in sorted(population_copy, key=lambda x: population_copy[x].Fitness):
                prob += population_copy[j].Fitness
                if prob >= pick:
                    self.Parent[i] = population_copy[j]
                    break

    def best_selection(self, routes=None):
        if routes is None:
            routes = self.Population
        #print("b")
        #print((routes[0].Fitness))
        #print((routes[1].Fitness))
        #print((routes[2].Fitness))
        #print((routes[3].Fitness))
        #print((routes[4].Fitness))
        max_fit = max([route.Fitness for route_id, route in routes.items()])
        for route_id, route in routes.items():
            #print("e1",route_id)
            if route.Fitness == max_fit:
                return route_id, route

    def elite_selection(self):
        elite_input = deepcopy(self.Population)
        #print("e",list(range(self.RouletteCount, self.PopulationSize)))
        for i in range(self.RouletteCount, self.PopulationSize):
            #print(i)
            route_id, route = self.best_selection(elite_input)
            self.Offspring[i] = route
            elite_input.pop(route_id)


    def route_crossover_bcrc(self, instance):
        #print("02.1")
        #print(len(self.Population[0].Trip), self.Population[0].Fitness, self.Population[0].Unassigned_Customers)
        #print(len(self.Population[1].Trip), self.Population[1].Fitness, self.Population[1].Unassigned_Customers)
        #print(len(self.Population[2].Trip), self.Population[2].Fitness, self.Population[2].Unassigned_Customers)
        #print(len(self.Population[3].Trip), self.Population[3].Fitness, self.Population[3].Unassigned_Customers)
        #print(len(self.Population[4].Trip), self.Population[4].Fitness, self.Population[4].Unassigned_Customers)
        offspring_pos = 0
        l1 = list(sorted(self.Parent.keys()))[::2]
        l2 = list(sorted(self.Parent.keys()))[1::2]
        random.shuffle(l1)
        random.shuffle(l2)
        #print(l1)
        #print(l2)
        parents = deepcopy(self.Parent)
        for p1, p2 in zip(l1, l2):
            #print(p1)
            #print(p2)
            self.Offspring[offspring_pos] = parents[p1]
            self.Offspring[offspring_pos + 1] = parents[p2]
            random_trip_1 = random.randint(0, len(self.Offspring[offspring_pos].Trip) - 1)
            random_trip_2 = random.randint(0, len(self.Offspring[offspring_pos + 1].Trip) - 1)
            locations1 = self.Offspring[offspring_pos].Trip[random_trip_1]['Location']
            locations2 = self.Offspring[offspring_pos + 1].Trip[random_trip_2]['Location']
            customers1 = [location for location in locations1 if location[0] == "C"]
            customers2 = [location for location in locations2 if location[0] == "C"]
            for c1, c2 in zip(customers1, customers2):
                self.Offspring[offspring_pos].remove_customer(instance, c2)
                self.Offspring[offspring_pos + 1].remove_customer(instance, c1)
            for c1, c2 in zip(customers1, customers2):
                self.Offspring[offspring_pos].insert_customer(instance, c2)
                self.Offspring[offspring_pos + 1].insert_customer(instance, c1)
            #print("After Insert")
            #print(self.Offspring[offspring_pos].Trip)
            #print(self.Offspring[offspring_pos + 1].Trip)
            offspring_pos = offspring_pos + 2
            #print("02.2")
            #print(len(self.Population[0].Trip), self.Population[0].Fitness, self.Population[0].Unassigned_Customers)
            #print(len(self.Population[1].Trip), self.Population[1].Fitness, self.Population[1].Unassigned_Customers)
            #print(len(self.Population[2].Trip), self.Population[2].Fitness, self.Population[2].Unassigned_Customers)
            #print(len(self.Population[3].Trip), self.Population[3].Fitness, self.Population[3].Unassigned_Customers)
            #print(len(self.Population[4].Trip), self.Population[4].Fitness, self.Population[4].Unassigned_Customers)
    def route_mutant(self, instance):
        for i, offspring in self.Offspring.items():
            current_customers = [location for key,value in offspring.Trip.items() for location in value['Location'] if
                                 location[0] =="C"]
            start, stop = sorted(random.sample(range(1, len(current_customers)), 2))
            customers = current_customers[:start] + current_customers[stop:start - 1:-1] + current_customers[stop + 1:]
            self.Offspring[i] = Route(instance, customers)
