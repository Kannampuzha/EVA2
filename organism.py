# An organism having the following functions
# This organism is a hypothetical lift having a single stimulus . The lift takes people to and fro across floors 0,1,2,3,4,5,6

# This is an example of an EPF based organism with a single , but dynamic stimulus
from random import randint, choice

from typing import Any, Generator
from time import time

# reading memory
memory = []
with open("memory.mem", 'r') as memory1:
    string_memory = memory1.readline()
    exec(f"memory={string_memory}")
print("Memory :")
print(memory)

# reading bad_memory
bad_memory = []
with open("bad_memory.mem", 'r') as memory1:
    string_memory = memory1.readline()
    exec(f"bad_memory={string_memory}")
print("Bad Memory :")
print(bad_memory)

memorised_actions=[]
with open("memorised_actions.mem", 'r') as memory1:
    string_memory = memory1.readline()
    exec(f"memorised_actions={string_memory}")
print("Memorised Actions :")
print(memorised_actions)


# Similarity algorithm
def check_similarity(stimulus1, stimulus2):  # Find the percentage of similaroty of stimulus2 with respect to stimulus1
    # The stumulus looks like tis : [a number 0 or 1 , a number 0 to 6]
    stop = False;
    number_of_elements_similar = 0;
    index = 0

    while stop != True and index !=len(stimulus1):
        if stimulus1[index] == stimulus2[index]:
            number_of_elements_similar += 1
            index += 1
        else:
            stop = True
    total_possible_similarity = 2  # len(stimulus1)
    similarity_percentage = (number_of_elements_similar / total_possible_similarity) * 100
    return (similarity_percentage)


def key_to_sort_by_end(x):
    return (x[-1])


class Organism():
    def __init__(self):
        self.stimuli = None  # stimuli looks like this : [Location_of_stimulus,Value_of_stimulus] ex : [0,6] , [1,4] , [0,3] , [1,3] etc . 0 is the Panel inside the lift . 1 is the panel outside the lift .
        self.transformer = None
        self.default_stimuli = None

        self.response = None
        self.default_response = None

        self.memory = memory  # refer line 10
        self.bad_memory = bad_memory  # refer line 18
        self.memorised=memorised_actions
        self.session_memory = []  # The memory of the session
        self.functions = ['go_to', 'take_person_in', 'take_person_out']  # organism's functions
        self.actual_functions = [self.go_to, self.take_person_in,self.take_person_out]  # the above ones are just for reference , this is the list of actual functions .
        self.chosen_function = None
        self.good_bad_determiner = 0.5
        self.difrence_threshold = 1  # Increase/Decrease this to change the limit till what score is considered as 'good' or 'bad'

        ##########Organism Specific Variables (Unrelated to the EPF)
        self.location = 0
        self.inside_person = False

    # Functions of the organism
    def go_to(self):
        # The function changes location of the lift by moving it
        print("Current Floor : ",self.location)
        try:

            if self.location != self.stimuli[-1]:
                self.location = self.stimuli[-1]
                print("moved lift to floor ", self.location)
            else:
                print("Aldready in requested location , no changes")
            self.response = self.location
        except:
            self.response=self.location


    def take_person_in(self):
        try:
            if self.inside_person == False:
                self.inside_person = True
                print("Took Person In")
                self.response = self.location
            else:
                print("There is aldready someone inside ! Can't take in more")
                self.response = self.location
        except:
            self.response=self.location


    def take_person_out(self):
        try:
            if self.inside_person == True:
                self.inside_person = False
                print("Took Person Out")
                self.response = self.location
            else:
                print("Nobody to take out")
                self.response = self.location
        except:
            self.response = self.location

    #####################################
    # EPF code (Dynamic, single stimulus )
    def PF(self):  # Process function . This takes any few functions and executes them in some order.
        memory_chunk = [self.stimuli]
        # selecting a random function
        id_of_random_function = randint(0, (len(self.functions) - 1))
        # putting function name in memory
        memory_chunk.append(self.functions[id_of_random_function])
        # executing the function
        self.actual_functions[id_of_random_function]()

        # putting response into memory chunk
        memory_chunk.append(self.response)

        # put memory chunk into session memory
        self.session_memory.append(memory_chunk)

        # Now select a random number 0 or 1 . If 0 , terminate PF , If 1 , invoke EPF
        recurse_or_terminate = randint(0, 1)
        if recurse_or_terminate == 0:

            # --------code to terminate EPF---------

            self.time_at_ending_epf = time()
            print("Time taken =", (self.time_at_ending_epf - self.time_at_session_beginning))


            # Put these things at each termination
            self.session_memory.append(self.response)
            print("Session :")
            print(self.session_memory)
            try:
                score = float(input("Enter Score :"))
                self.session_memory.append(score)
                self.memory.append(self.session_memory)
                # writing memory
                with open("memory.mem", 'w') as memory:
                    memory.write(f"{self.memory}")

                if score > self.good_bad_determiner and self.initial_stimuli not in self.memorised:
                    self.memorised.append(self.initial_stimuli)
                    with open("memorised_actions.mem", 'w') as memory:
                        memory.write(f"{self.memorised}")

                self.stimuli = self.default_stimuli
                self.response = self.default_response
                self.session_memory = []
                return ()
            except:
                self.stimuli = self.default_stimuli
                self.response = self.default_response
                self.session_memory = []
                return ()

        else:


            # Select a random number 0 or 1 . If 0  stimuli and response are unchanged . If 1 , stimuli will become response and response becomes None.
            # That means , if 0 , then further possible function will work on the same stimuli as before . If 1 , then
            # future function will work on a new stimuli , which was the response from this current function .
            # we are assuming this here.
            new_stimuli_or_old = randint(0, 1)
            if new_stimuli_or_old == 1:
                self.stimuli = self.response
                self.response = None
            else:
                pass

            # evoking EPF again , recursing .
            self.PF()
            return ()

    def non_PF(self):

        past_instances = [x for x in self.memory if x[0] == self.stimuli]

        # making its set , where everyon is unique
        past_instances_as_set = []
        past_instances_with_score = []

        for x in past_instances:

            if x[:len(x) - 1] not in past_instances_as_set:
                past_instances_as_set.append(x[:len(x) - 1])
                past_instances_with_score.append([x[:len(x) - 1], x[-1]])
                # This would be [session , cumulative_score]

            else:

                past_instances_with_score[past_instances_as_set.index(x[:len(x) - 1])][-1] += x[-1]

        # seleccing one with highest score
        self.difrence_threshold = 1  # cahnege this to increase diffrnece . It is an added bias to the alogoritm , roughly translating to "the good one should be atleast 3 scores ahead of all the other ones"

        self.selected_instance = None;
        self.selected_score = 0
        multiple_instances_having_same_score = []
        for x in past_instances_with_score:
            if x[1] > self.selected_score:
                self.selected_instance = x[0]
                self.selected_score = x[1]

        # checking if the gap between chosen function and others is equal or greater than the diffence thershold.
        for x in past_instances_with_score:

            if x[0] != self.selected_instance and self.selected_score != 0:
                if self.selected_score - x[1] == 0:
                    multiple_instances_having_same_score.append(x)
                    continue
                    # This means 2 or more sessions are equal . We can choose one randomly fromm them
                if self.selected_score - x[1] < self.difrence_threshold:
                    self.selected_instance = None
                    self.selected_score = 0

                    # This means that the diffrence isnt large enough . So we evoke PF
            else:

                pass




        if len(multiple_instances_having_same_score) > 0:
            multiple_instances_having_same_score.append(self.selected_instance)
            self.selected_instance = choice(
                multiple_instances_having_same_score)  # choose one randomly among equal scoring functions



        if self.selected_instance == None:
            # This means that it will not be evaluated from memory . So ,if this is a transformed object , we shall remove the transformation
            # and pass it to the next nearest similar stimulus.

            if self.transformer != None:
                # Removing transformation , in case this is being performed on a transformed stimulus....
                self.stimuli = self.transformer
                self.transformer = None
                self.PF()
            return (0)


        else:
            print("Evaluating from Memory")
            if self.initial_stimuli not in self.memorised:
                self.memorised.append(self.initial_stimuli)
                with open("memorised_actions.mem", 'w') as memory:
                    memory.write(f"{self.memorised}")



        # now we have to take each memory chunk from it and re-run them.

        # Before we do anything , we should remove the transofrmation.
        if self.transformer != None:
            t = self.stimuli
            self.stimuli = self.transformer
            self.transformer = None

        else:
            t=0

        selected_past_instace = self.selected_instance[1:(len(self.selected_instance) - 1)]

        self.selected_score = 0
        self.selected_instance = None  # Ignore this line . Just to prevent complcations in future

        initial_stimuli = self.stimuli
        operations_to_be_performed = []
        for x in selected_past_instace:
            # if it is not self.stimuli , then that means here the further function worked on an older response
            # So we map this in operations_to_be_performed , to direct in afterwards to to work on self.response and not self.stimuli .

            if x[1] in self.functions:  # x[1] would be a function .
                operations_to_be_performed.append(x[1])
            elif x != self.stimuli:
                operations_to_be_performed.append(1)
            elif x == self.stimuli:
                operations_to_be_performed.append(0)

        # performing the operations as per the sequnece . Wherever its 1 , the stimuli is changed to the eariler response . Wherever it is 0 , stimuli is turned bak to the initial stimuli .
        for x in operations_to_be_performed:
            memory_chunk = [self.stimuli]
            if x != 1 and x != 0:
                memory_chunk.append(x)
                self.actual_functions[self.functions.index(x)]()
                memory_chunk.append(self.response)

                self.session_memory.append(memory_chunk)  # put memory chunk into session memory
            elif x == 1:
                self.stimuli = self.response
            elif x == 0:
                self.stimuli = initial_stimuli

        # --------code to terminate EPF---------

        self.time_at_ending_epf = time()
        print("Time taken =", (self.time_at_ending_epf - self.time_at_session_beginning))


        # Put these things at each termination
        self.session_memory.append(self.response)
        print("Session :")
        print(self.session_memory)
        try:
            score = float(input("Enter Score :"))
            self.session_memory.append(score)
            self.memory.append(self.session_memory)
            # writing memory
            with open("memory.mem", 'w') as memory:
                memory.write(f"{self.memory}")

            if t==1 and score<self.good_bad_determiner:
                self.bad_memory.append([self.stimuli,t])
                with open("bad_.mem", 'w') as memory:
                    memory.write(f"{self.bad_memory}")





            self.stimuli = self.default_stimuli
            self.response = self.default_response
            self.session_memory = []
            return (1)
        except:
            self.stimuli = self.default_stimuli
            self.response = self.default_response
            self.session_memory = []
            return (1)

    def static_EPF_modified(self, transforming_stimulus):
        # This is technically the same code as non_EPF() , diffrences are summarised here :
        # 1. First , self.stimuli changes to the transforming past instance .
        # 2. Aftr it instructs to evaluate from meory or through PF , the transformation is removed , and operations are performed on the earleir stimulus .
        # Exchange for transforming
        self.stimuli, self.transformer = transforming_stimulus, self.initial_stimuli
        self.non_PF()

    def EPF(self):  # Evocation Processing Function
        # put initial stimuli into session memory
        self.time_at_session_beginning = time()
        self.session_memory.append(self.stimuli)
        self.initial_stimuli = self.stimuli

        if len(self.memory) != 0:

            # First , we will find simialriy % for each . This method is less efficient from a biological perspective , but quite usable as an example .
            # A better technique qould be to use a graph.
            # Here , we will find similarity of the self.stimuli to every single past encountered stimulus in the past in the memory . Then we selectthe best of them.
            similarity_list = []
            for past_encounter in memory:
                similarity_list.append([past_encounter[0], check_similarity(self.stimuli, past_encounter[0])])


            similarity_list.sort(key=key_to_sort_by_end)
            similarity_list.reverse()

            # Now select the best one , with highest similarity .
            index = 0
            print('hello', similarity_list)
            while index != len(similarity_list) :
                if similarity_list[index][-1] == 100:
                    successful_or_not = self.non_PF()  # it is either 0 or 1

                    if successful_or_not == 0:
                        index += 1
                        continue
                    if successful_or_not == 1:
                        break  # This means we have ended it here.

                if similarity_list[index][-1] == 0:

                    self.PF()
                    break

                else:  # any value between 0% and 100% similarity
                    
                    if (self.bad_memory.count([self.stimuli, similarity_list[index][0]]) < self.difrence_threshold) and (similarity_list[index][0] in memorised_actions) :  # If the number of  times it it there is too much , then we will not do this.
                        self.static_EPF_modified(similarity_list[index][0])
                        break
                    else:
                        index += 1
                        pass

                    # It is technically the same thing, diffrence is that there is transformation of the stimulus into the past stimulus






        else:

            self.PF()

    def initialise(self, argument_for_organism):
        # Actual initialisation of EPF . EPF is the carrier of all functions of the organism
        self.stimuli = argument_for_organism
        self.EPF()
        return (self.response)


def train():
    lift = Organism()
    for x in range(100):
        target_floor=randint(0,6)
        print("Target_floor :", target_floor)
        lift.initialise([1,target_floor])

        target_floor = randint(0, 6)
        print("Target_floor :", target_floor)
        lift.initialise([0,target_floor])



#Run this for training
train()

'''Parameters for initialising :
Initialise with a list [x,y] 
where x is 0 or 1 and y is 0,1,2,3,4,5 or 6
In case of x , 0 represents "The Panel Inside the Lift"
1 is "The Panel on the exertior , on each floor" '''
'''If you dont want to work in training mode , simply press enter whem it asks you score'''
