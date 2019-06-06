from cooperation.agents import Cow, GrassPatch, FCMCow
from cooperation.schedule import RandomActivationByBreed

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
import numpy as np
from cooperation.fcmwrapper import FCMAgent

class CooperationBatch(Model):
    grid_h = 20
    # grid width
    grid_w = 20
