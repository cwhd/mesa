from mesa import Agent
from cooperation.random_walk import RandomWalker

# you can have a greedy cow or a cooperative cow
# note that instead of the individual methods in NetLogo everything ends up going into the step function
class Cow(RandomWalker):

    def __init__(self, unique_id, pos, model, moore, energy=None, is_greedy=False):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.greedy = is_greedy

    def step(self):
        #  MOVE FUNCTION
        self.random_move()
        living = True
        self.energy -= 1 #TODO this should include metabolism

        #EAT
        # If there is grass available, eat it
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in this_cell
                        if isinstance(obj, GrassPatch)][0]
        if grass_patch.fully_grown:
            #TODO this should come from a variable?
            #self.energy += self.model.sheep_gain_from_food
            self.energy += 5
            grass_patch.fully_grown = False
            if self.greedy:
                #greedy cow
                grass_patch.countdown = 0
            else:
                grass_patch.countdown -= 1

        # Death
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            living = False

        #Reproduce
        if living and self.random.random() < self.model.reproduction_threshold:
            # Create a new sheep:
            self.energy /= 2
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
