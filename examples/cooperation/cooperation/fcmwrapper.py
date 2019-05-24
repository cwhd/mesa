import requests
import json

class FCMAgent():

#TODO would be cool to have a code generation button in the FCM modeler - 
# - so when you have params that you want, 
# -- click a button
# -- get some code you can copy/paste into here for params

    """
    Method to get results of an FCM based agent. 
    model_id : the id of the model from the FCM system
    starting_state_dict : dictionary of node state information to use as a starting point  
    """
    def getFCM(self, model_id, starting_state_dict):
        #print("getting FCM...")

        post_body = json.dumps(starting_state_dict)

        headers = {'content-type': 'application/json'}
        fcm_request = requests.post('http://localhost:8080/fcm/' + model_id + '/run?maxEpochs=1', data=post_body, headers=headers)
        results = fcm_request.json()
        results_dict = json.loads(fcm_request.text)
        fcm_dict = {}
        for node in results_dict['iterations'][0]['nodes']:
            fcm_dict[node['name']] = node['value']

        return fcm_dict

"""
TODO put stuff for FCM connections in here.
- ensure that we pass parameters that match mesa paradihm

WORKFLOW
- define an agent in the web based tool
- give it a name, maybe the interface gives you a URL?
- put the URL for the agent in the agent definition
- pass data back into a data collector
- mesa offloads FCM stuff to FCM platform

COOPERATION
- Define an FCM for a greedy cow and one for a cooperative cow
- See how the 2 different resources survive as they compete for food

"""