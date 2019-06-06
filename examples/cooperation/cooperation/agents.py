from mesa import Agent
from cooperation.random_walk import RandomWalker

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
