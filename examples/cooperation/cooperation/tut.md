# Project Mesa Tutorial

[project mesa](https://github.com/projectmesa/mesa) is a python based Agent Based Modeling (ABM) platform designed to compete against [Netlogo](https://ccl.northwestern.edu/netlogo/). Part of the power of ABM is it's ability to create visualizations so model authors can watch things emerge as the model runs. Mesa can run in a notebook but to take advantage of mesa's web based interface  you should run it outside the notebook environment. This tutorial will walk you through my recreation of the Netlogo model *Cooperation*. To see it in action feel free to get the [code from github](https://github.com/cwhd/mesa).

## Running the model

Firt you'll want to download the latest code from github. Open up your favorite terminal and put in the following code:

``` bash

git clone https://github.com/cwhd/mesa

```

Note that I'm pointing you to my branch of mesa that has my example code. If you want to start off clean just get mesa from the source:

``` bash

git clone https://github.com/projectmesa/mesa

```

Also make sure that you install mesa as a python library. You can do that with pip like this:

```bash

pip install mesa

```

Mesa comes with several samples in the *examples* folder. To run the example in this tutorial run the following from the command line in my fork of the mesa project:

```bash

mesa runserver .\examples\cooperation\

```

Give it a few seconds and mesa should open up in your web browser with the cooperation model. Feel free to play around with it. When you're done come back here and I'll explain everything that's going on.

## Mesa components

Now that you have a working example in front of you I'll walk through the components of mesa that you'll need to know about to build your own model. I'll use the cooperation model as an example but if you're building your own model feel free to follow along and create your own model by building out all the same components.

### Basic stuff

The first thing you'll need are some basic components for your project. If you look in the examples/cooperation directory you'll see the following files:

- cooperation/
- README.md
- requirements.txt
- run.py

The cooperation folder has most of the code for the model in it. You should create a directory with the same name as your project so it's easy to remember.

The README file has any instructions to run your project and a description of the project. Treat this like a basic manual or README that you'd find anywhere else.

requirements.txt is a regular python requirements.txt file Mesa will run this to install any dependancies that you need for your project. You can just copy mine to start with.

run.py is what mesa calls to startup your model. It's going to call the mesa server that you'll extend in the next step of the tutorial. For now you can just copy the code I have, but change 'cooperation.server' to '*your_project_folder_name*.server'

### Server

Mesa is a web-based platform for visualizing ABM. Because of this if you want to see visualizations you need to use a *server* to run your project. Under the hood mesa uses [tornado](https://www.tornadoweb.org/en/stable/) as it's web framework which uses [asyncio](https://docs.python.org/3/library/asyncio.html) for asynchronous functionality. As a modeler this probably doesn't matter, but it's good to know if you want to extend the platform at some point or run your model in a container somwhere other than your local machine.

The *server* object extends a tornado application server and creates a container for your model. If you scroll down to the bottom of the code in server.py you can see that you can pass the following parameters into the server:

- model_cls
- visualization_elements
- name="Mesa Model"
- model_params={}

*model_cls* is the class for your model. In this case I have a file called model.py with the class *Cooperate* in it so I pass that in. We'll create a model class in the next step, but if you know what you want to name it go ahead and pass it in here.

*visualization_elements* is an array of elements to display on your page. Typically you'll need a canvas and a chart, but feel free to check out the other examples to see what else you could do.

*name* is the name of your mode. This is used for display purposes, so call it whatever you want.

*model_params* are all the elements that you use to tweak the parameters of your model. If you ran the cooperation model earlier you noticed the sliders on the page - those are input parameters that the user can change. You can create a bunch of different parameters by creating a dictionary of *UserSettableParameter* objects as shown below. User parameters map to different types of input types that you can find on web sites; sliders, toggles, etc. The example below shows a few of them with example parameters:

Check out the *UserParam.py* class in mesa for full documentation and details.

```python

model_params = {
    "use_fcm": UserSettableParameter('checkbox', 'Use FCM', False),
    "init_cows": UserSettableParameter("slider", "cows", 25, 1, 200,
                                                    description="Cows...")
}
```

If you're running the server on your localhost it runs on port 8521. 

#### Portrayals

Portrayal is mesa terminology for how a cell is displayed, what it looks like and where it is on the grid. A portrayal is called every tick to determine how to display each individual cell. A portral should return a dictionary in python like this:

```python

return {
    "Shape": "rect",
    "w": 1,
    "h": 1,
    "Filled": "true",
    "Layer": 0,
    "x": cell.x,
    "y": cell.y,
    "Color": "black" if cell.isAlive else "white"
}

```

In the exampe above some of the parameters are determined dynamically based on what parameters get passed into the agent. Here are the parameters you can set in a portrayal dictionary:

"x", "y": Coordinates for the cell in which the object is placed.
"Shape": Can be either "circle", "rect" or "arrowHead"
    For Circles:
        "r": The radius, defined as a fraction of cell size. r=1 will
             fill the entire cell.
    For Rectangles:
        "w", "h": The width and height of the rectangle, which are in
                  fractions of cell width and height.
    For arrowHead:
    "scale": Proportion scaling as a fraction of cell size.
    "heading_x": represents x direction unit vector.
    "heading_y": represents y direction unit vector.
"Color": The color to draw the shape in; needs to be a valid HTML
         color, e.g."Red" or "#AA08F8"
"Filled": either "true" or "false", and determines whether the shape is
          filled or not.
"Layer": Layer number of 0 or above; higher-numbered layers are drawn
         above lower-numbered layers.
"text": The text to be inscribed inside the Shape. Normally useful for
        showing the unique_id of the agent.
"text_color": The color to draw the inscribed text. Should be given in
              conjunction of "text" property.

### Agents

An agent is an individual component in your model. When you define your agents you define how your agent interacts with it's environment or other agents. Any properties or actions of your agent is defined in your agent classes. Each agent extends the *Agent* class in mesa.

Maybe we should have started with Agents. Agents are the actors in your model, they're the ones doing whatever is done in your model and what you're monitoring. In mesa typically you'll see an agents.py file with all the agents defined in it. You can organize your code anyway you like, I'm following the examples that mesa already comes with.

In your agents.py file define your agents as classes that extend the *Agent* class. If you take a look at the cooperation model.py you'll see that there are a few agents that extend the RandomWalker base class in the random_walk file, I stole that from a few other models that were doing the same thing. For an extremely simple agent take a look at the GrassPatch class, which represents a patch of grass that grows up to a certain height. Note that it just needs an _init function and a step function. The step function will get called on every tick or step in your model, so that's what happens as time passes in your ABM. of course __init__ does whatever you need to do in order to initialize your model. In your __init__ function don't forget to call super().__init__(unique_id, model), mesa uses that to keep track of your agents.

Go ahead and try to create a simple agent and we'll add it into the model in the next step.

### Model

The model specifically extends the *Model* object in mesa. This class is where you define what happens during a step, what your data collectors are, and visualizations you have, and sets up your agents. This is the core class where you define how things work.

In Mesa you need to define your model and your agents in code. Both your model and your agents need to have a *step* function defined. This function will automatically be called by Mesa, and will be the action that happens when every time a step occurs in your model.

Now that you have some agents defined we can add them to the model. Your model sets everything up and there are a few elements that you need to be aware of.

#### Setting up a Scheduler

The scheduler extends the *RandomActivation* class and is responsible for adding and removing agents. It represents the current time as the model runs, so it can also be accessed to get data regarding the current state of the model and your agents. If you take a look at schedule.py you'll see that the *RandomActivation* class has been extended; we not only define what happens every step, but we also have functions that get state parameters that we want to report on while the model runs.

#### Auditing with DataCollector

As your model runs you'll want to collect data so you can display it in charts or use it for analysis. For this you would use the built in *DataCollector* class. The data collector can be used after the model is run to get data from your model.

The DataCollector, as it's name implies, is used to collect data while the model is running. DataCollectors can collect variables from the model, agents, or tables. You define your data collectors somewhere outside your model, in your model you can define a dictionary of methods that can be used for data collection. You can access your *Scheduler* from your *DataCollector*. Here are a few snippets that show what the data collection method could look like and how to add it in you model, go ahead and find them in the cooperation example to see them in context.

```python

# define the method used for data collection in your scheduler
def get_greedy_cows(self, breed_class):
    r_count = 0
    for key, value in self.agents_by_breed[breed_class].items():
        if value.greedy:
            r_count += 1
    return r_count

# in your model implementation set dictionary of reporters
self.datacollector = DataCollector(model_reporters={
                                    "Greedy": lambda m: m.schedule.get_greedy_cows(Cow),
                                    "Cooperative": lambda m: m.schedule.get_cooperative_cows(Cow)}
                                )

```

You are probably going to want to collect a few different things to get decent data from your model.

### Batch Runs

Sometimes you don't care about vizualization and you just want to collect data from your model. You can do this by creating a batch run. With a batch run you hard code all of your parameters, run the batch, and your results get dumped into a CSV file that you can use for analysis. There is a great example of running batch jobs in the *bank_reserves* example. Note in there that instead of *run.py* which references a model class, there is a *batch_run.py* that has all the setup and stuff you would normally put in the model. Since you hard-code your parameters and do a long run, you really don't need to set up a server with interface elements, instead you can put it all in one file, run your model from there, and work with your results.

### Enjoy Your Model

Now that we've reviewed all the components of an ABM using mesa you're ready to start building models! When I start to build models using mesa I'll usually fork the mesa repo, create a new directory in the examples folder and start hacking away. You can probably find some great starting points from some of the existing examples. If you can't it's not that tough to translate code from NetLogo into mesa. 

*Have fun!*

### Project structure good practice

Since you have to write your own code you can do it however you like. Based on the examples that come with Mesa a typical project structure contains a run.py file, a directory for your project, and any files specific to your model in the directory. Here are a few tips for making your model easier to read and understand by other modelers.

A basic project structure should look something like this:

|- run.py
|- your_project_directory
|-- server.py
|-- agents.py
|-- model.py

run.py simply imports the rest of the project and starts the server.
It's a good idea to name *your_project_directory* to something that describes your model. For example if you have a model that tests the decoy effect, maybe you should name it *decoy_effect* or something like that.

Agents are defined in the *agents.py* file.

The model is defined in *model.py*.

*server.py* typically contains parameters for the model and the server definition. You pass your model into server.

Check out [the examples](https://github.com/projectmesa/mesa/tree/master/examples) in github for different ways to modularize and structure projects as they get more complex.
