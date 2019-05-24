from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from cooperation.agents import Cow, GrassPatch, FCMCow
from cooperation.model import Cooperate

"""
Citation:
The following code was adapted from the NetLogo example Cooperation:
Wilensky, U. (1997). NetLogo Cooperation model. 
http://ccl.northwestern.edu/netlogo/models/Cooperation. 
Center for Connected Learning and Computer-Based Modeling, 
Northwestern University, Evanston, IL.

Author of original code: cwhd
"""

# Red
COOPERATIVE_COLOR = "#FF3C33"
# Blue
GREEDY_COLOR = "#3349FF"

def coop_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # update portrayal characteristics for each Cow
    if type(agent) is Cow or type(agent) is FCMCow:
        portrayal["Shape"] = "circle"
        portrayal["r"] = .5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        if agent.greedy:
            color = GREEDY_COLOR
        else:
            color = COOPERATIVE_COLOR

        portrayal["Color"] = color

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


# dictionary of user settable parameters - these map to the model __init__ parameters
model_params = {
    "use_fcm": UserSettableParameter('checkbox', 'Use FCM', False),
    "init_cows": UserSettableParameter("slider", "cows", 25, 1, 200,
                                                    description="Cows..."),
                "stride_length": UserSettableParameter("slider", "Stride Length", 10, 1, 20,
                                                   description="Length of stride..."),
                "cooperative_probabilty": UserSettableParameter("slider", "Cooperative Propability", 50, 1, 100,
                                                    description="Prob.."),
                "metabolism": UserSettableParameter("slider", "metabolism", 50, 1, 100,
                                                    description="How much energy is used when walking"),
                "reproduction_cost": UserSettableParameter("slider", "Reproduction Cost", 10, 1, 100,
                                                    description="How much energy it takes to reproduce"),
                "reproduction_threshold": UserSettableParameter("slider", "Reproduction Threshold", 80, 1, 100,
                                                    description="Threshold to reproduce"),
                "grass_energy": UserSettableParameter("slider", "Grass Energy", 50, 1, 100,
                                                    description="Energy gained from eating")

                }

# set the portrayal function and size of the canvas for visualization
canvas_element = CanvasGrid(coop_portrayal, 20, 20, 500, 500)

# map data to chart in the ChartModule
chart_element = ChartModule([{"Label": "Greedy", "Color": GREEDY_COLOR},
                             {"Label": "Cooperative", "Color": COOPERATIVE_COLOR}])

# create instance of Mesa ModularServer
server = ModularServer(Cooperate, [canvas_element, chart_element],
                       "Cooperation",
                       model_params=model_params
                       )
