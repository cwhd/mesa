from mesa import Agent
from cooperation.random_walk import RandomWalker
from cooperation.fcmwrapper import FCMAgent

"""
A cow that uses a mental model to decide what to do
Here are some model ids:
        #666-99-6969
        #123456789
        #75-325
"""
class FCMCow(RandomWalker):
    def __init__(self, unique_id, pos, model, moore, fcm_result=None, energy=50, is_greedy=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.greedy = is_greedy
        self.fcm_result = fcm_result

    #this gets called every tick
    def step(self):
        #print("FCM RESULT")
        #print(self.fcm_result)
        self.random_move()
        living = True
        self.energy -= self.model.metabolism

        # Eat if there is grass
        eat_chance =  self.random.randrange(0, 100) / 100
        if self.fcm_result['Food Observation'] < eat_chance:
            #first check for grass
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            grass_patch = [obj for obj in this_cell
                            if isinstance(obj, GrassPatch)][0]
            if grass_patch.fully_grown:
                eat_amount = grass_patch.countdown * self.fcm_result['Eat']
                grass_patch.countdown -= eat_amount
                self.energy += self.fcm_result['Energy'] * self.model.grass_energy
                grass_patch.fully_grown = False

        # Death
        if self.energy < 0: #self.fcm_result['Energy']
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # Reproduce
        if living and self.random.random() < self.model.reproduction_threshold:
            self.energy -= self.model.reproduction_cost

            calf = FCMCow(self.model.next_id(), self.pos, self.model, 
                            self.moore, self.fcm_result, self.energy, self.greedy)
            self.model.grid.place_agent(calf, self.pos)
            self.model.schedule.add(calf)

# you can have a greedy cow or a cooperative cow
# note that instead of the individual methods in NetLogo everything ends up going into the step function
class Cow(RandomWalker):

    def __init__(self, unique_id, pos, model, moore, energy=None, is_greedy=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.greedy = is_greedy

    #this gets called every tick
    def step(self):
        self.random_move()
        living = True
        self.energy -= self.model.metabolism

        #Eat if there is grass
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in this_cell
                        if isinstance(obj, GrassPatch)][0]
        if grass_patch.fully_grown:
            self.energy += self.model.grass_energy
            grass_patch.fully_grown = False
            if self.greedy:
                grass_patch.countdown = 0
            else:
                grass_patch.countdown -= 1

        # Death
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        # Reproduce
        if living and self.random.random() < self.model.reproduction_threshold:
            self.energy -= self.model.reproduction_cost
            calf = Cow(self.model.next_id(), self.pos, self.model,
                         self.moore, self.energy)
            self.model.grid.place_agent(calf, self.pos)
            self.model.schedule.add(calf)

#I borrowed this from the wolf and sheep model.
class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    '''

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
