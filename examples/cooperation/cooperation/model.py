from cooperation.agents import Cow, GrassPatch
from cooperation.schedule import RandomActivationByBreed

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np

'''
Create a new greedy cow model

Args:
    init_cows: Number of cows to start with
    stride_length: 
    cooperative_probabilty:
    metabolism: 
    reproduction_cost:
    reproduction_threshold:

'''
class Cooperate(Model):
    """
    This is a mesa implementation of the greedy cows model
    """
    # grid height
    grid_h = 20
    # grid width
    grid_w = 20

    description = 'A model for simulating greedy cows. Written by Christopher Davis as a tutorial for SYSC-535.'

    #cooperative_probabilty should be between 0-100
    def __init__(self, height=grid_h, width=grid_w, init_cows=10, stride_length=1, 
                cooperative_probabilty=1, metabolism=1, reproduction_cost=1, 
                reproduction_threshold=1, grass_energy=1):

        self.height = height
        self.width = width
        #have to initialize the grid
        self.grid = MultiGrid(self.width, self.height, torus=True)
        self.init_cows = init_cows
        self.stride_length = stride_length
        self.cooperative_probabilty = cooperative_probabilty
        self.metabolism = metabolism
        self.reproduction_cost = reproduction_cost
        self.reproduction_threshold = reproduction_threshold
        self.grass_regrowth_time = 3
        self.grass_energy = grass_energy

        #note reporter has to be aware of what type of class we're using
        self.datacollector = DataCollector(model_reporters={
                                            "Greedy": lambda m: m.schedule.get_greedy_cows(Cow),
                                            "Cooperative": lambda m: m.schedule.get_cooperative_cows(Cow)}
                                        )

        #don't forget to init the super, otherwise you'll get strange errors
        super().__init__()
        #set the scheduler
        self.schedule = RandomActivationByBreed(self)

        energy = metabolism * 4
        is_greedy = False

        #Generate the cows. 
        for i in range(self.init_cows):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            is_greedy = False
            greedy_range = self.random.randrange(0, 100)
            if(greedy_range < self.cooperative_probabilty):
                is_greedy = True

            cow = Cow(self.next_id(), (x, y), self, True, energy, is_greedy)
            self.grid.place_agent(cow, (x, y))
            self.schedule.add(cow)         
                         
        #Generate the grass
        for agent, x, y in self.grid.coord_iter():
            fully_grown = self.random.choice([True, False])
            if fully_grown:
                countdown = self.grass_regrowth_time
            else:
                countdown = self.random.randrange(self.grass_regrowth_time)
            patch = GrassPatch(self.next_id(), (x, y), self,
                                fully_grown, countdown)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)

    def step(self):
        # tell all the agents in the model to run their step function
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self):
        for i in range(self.run_time):
            self.step()

