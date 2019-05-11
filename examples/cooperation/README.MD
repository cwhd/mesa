# Cooperations

This is a translation of the *Cooperation* model from [Netlogo](https://ccl.northwestern.edu/netlogo/) by [Christopher Davis](https://www.researchgate.net/profile/Christopher_Davis50?ev=hdr_xprf&_sg=Rck796knJKvnKrOie9mTg9aiDsUCm7GeA6Raj84vuiLsGl8XJzed-zYkzqNm9iIedSaTriz9kntWFNkIYeLJxfLg) aka [@techchrisdavis](https://twitter.com/techchrisdavis) aka [cwhd](https://github.com/cwhd).

## WHAT IS IT?

This model (and Altruism and Divide the Cake) are part of the EACH unit ("Evolution of Altruistic and Cooperative Habits: Learning About Complexity in Evolution").  See http://ccl.northwestern.edu/rp/each/index.shtml for more information on the EACH unit. The EACH unit is embedded within the BEAGLE (Biological Experiments in Adaptation, Genetics, Learning and Evolution) evolution curriculum. See http://ccl.northwestern.edu/rp/beagle/index.shtml.

This is an evolutionary biology model.  In it, agents (cows) compete for natural resources (grass).  Cows that are more successful in getting grass reproduce more often, and will thus be more evolutionarily successful.  This model includes two kinds of cows, greedy and cooperative.  It shows how these two different strategies do when competing against each other within a population that evolves over time.

## HOW IT WORKS

Every turn, each cow looks at the patch that it is currently on, and eats a unit of grass.  The greedy cows eat the grass regardless of the length of the grass on the current patch.  The cooperative cows won't eat the grass below a certain height.  This behavior is significant because below a certain height (called the "growth threshold"), the grass grows at a far slower rate than above it.  Thus, the cooperative agents leave more food for the overall population at a cost to their individual well-being, while the greedy agents eat the grass down to the nub, regardless of the effect on the overall population.

## HOW TO USE IT

GO: Starts and stops the model.

SETUP: Resets the simulation according to the parameters set by the sliders.

INITIAL-COWS: Sets the number of initial cows.

COOPERATIVE-PROBABILITY: Sets the chance an initial cow will be of the cooperative breed

STRIDE-LENGTH: This value determines the movement of the cows. Each cow will move forward a distance of STRIDE-LENGTH  each turn.  As the value is increased, the cows will move to other patches more frequently.

GRASS-ENERGY: Each time a cow can eat some grass from the patch that it currently occupies, it increases its energy by the value of this slider.

METABOLISM: Every time step, each cow loses the amount of energy set by this slider.  If the cows energy dips below 0, it dies.  Every cow starts with a default energy of 50, which means it can go 50 / METABOLISM turns without eating.

REPRODUCTION-THRESHOLD: If a cow's energy reaches the value of this slider, it reproduces.  This value represents the food-gathering success that a cow would have to have in order to be able to reproduce.

REPRODUCTION-COST: Each time a cow reproduces, it loses the amount of energy set by this slider.  This value represents the energy cost of reproduction.

LOW-GROWTH-CHANCE: This value is the percentage chance that the grass below the growth threshold will grow back.  The higher this value, the less the discrepancy between the behaviors of the cooperative and greedy cows.

HIGH-GROWTH-CHANCE: This value is the percentage chance that the grass above the growth threshold will grow back.  The lower this value, the less the discrepancy between the behaviors of the cooperative and greedy cows.

MAX-GRASS-HEIGHT:  This value sets the highest length to which the grass can grow.

LOW-HIGH-THRESHOLD:  This value sets the grass growth threshold.  At, or above this value, the grass grows back with HIGH-GROWTH-CHANCE.  Below this value, the grass grows back with LOW-GROWTH-CHANCE.

## THINGS TO NOTICE

Run the model with the default settings.  Watch the different growth curves on the population plot.  Which population expands first?  Which population wins in the end?

## THINGS TO TRY

Slowly decrease the STRIDE-LENGTH slider. What happens to the populations?

At what value of STRIDE-LENGTH do the populations' growth rates change dramatically?  What does this indicate about the evolutionary advantages of cooperating versus being greedy?  What are the important environmental factors?

Change the METABOLISM and the GRASS-ENERGY values.  How do these values affect the model?

Change the LOW-GROWTH-CHANCE and the HIGH-GROWTH-CHANCE values.  How do these values affect the model?

How does the LOW-HIGH-THRESHOLD value affect the growth of the populations?

Can you find settings that maximize the advantage of the cooperative cows?

## EXTENDING THE MODEL

This model explores only one type of cooperative behavior, namely eating the grass above the growth threshold (the LOW-HIGH-THRESHOLD value).  What other cooperative, or altruistic, behaviors could be modeled that hurt individual fitness, while helping the group overall?  What environmental conditions other than grass length could be used to affect the health of a population?

This model relies primarily upon population "viscosity" (the STRIDE-LENGTH slider) to alter the behavior of the cows to allow for the success of the cooperative agents.  What other variables could have such a drastic effect on the evolutionary success of populations?

Also, consider that in this model the behaviors are fixed.  What would happen if the agents learned, or changed their behavior based on food availability?

## RELATED MODELS

Altruism

## CREDITS AND REFERENCES

This model, the Altruism model and the Divide the Cake model are part of the curriculum unit "Evolution of Altruistic and Cooperative Habits: Learning About Complexity in Evolution".  See http://ccl.northwestern.edu/rp/each/index.shtml for more information. The EACH unit is embedded within the BEAGLE (Biological Experiments in Adaptation, Genetics, Learning and Evolution) evolution curriculum. See http://ccl.northwestern.edu/rp/beagle/index.shtml.

Thanks to Damon Centola, Eamon McKenzie, Josh Mitteldorf, and Scott Styles.

## CITATIONS

For the model itself:

* Wilensky, U. (1997).  NetLogo Cooperation model.  http://ccl.northwestern.edu/netlogo/models/Cooperation.  Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

Please cite the NetLogo software as:

* Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.