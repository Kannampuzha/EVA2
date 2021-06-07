# Evocative-algorithm-version-2
A more practical algorithm that uses memory to program its own behaviour.<br>

Refer [Evocative-Algorithm](https://github.com/Kannampuzha/Evocative-Algorithm)

This application is an enhanced and more practically applicable version of the Evocative-Algorithm.

# Evocative-Algorithm-Generator
A program working on memory to design an algorithm

*"EVOCATION - The act of bringing or recalling a feeling, memory, or image to the conscious mind."*

## What is it?
It is an alogorithm that learns to make an algorithm for some purpose. Here I identify a program as being 
synonymous to a biological organism having a set of well defined functions. It is very important to note that
every possible function of the organim is known, and defined in the program.
Any possible outcome that this organism will ever produce is thus clearly a manifestation of one or more functions
of this organism. No outcome is thus possible outside the domain of the organism.<br>

This example is a Lift Application Simulation . The lift takes in a single input (multi stimuli system is not yet developed )
It is then supposed to take you to a desired location , but it does not know how to do that .
It gives out random functions till it gets a good score . Once that happens , the correct behaviour is learnt , the next time you tell it to go somewhere , it can do that without giving random outputs. Learnt patterns can be unlearnt and tweaked with negative scoring.
The program knows the following things only :<br>
1. It knows to move itself.
2. It knows to take in a person.
3. It knows to take out a person.
4. It assumes that "What happens in the past could happens in the future".<br>

With the above functions , it essentially codes its own behaviour with the guidance of its memory and past actions , and the scores that users give . 
Once trained , the algorithm can be retrained , untrained , or adjusted to drastic changes with changes in scores .It doesn't complain if you suddenly start giving it -1 to something that deserved 1.

_This version of the algoritm solves the problem that was untouched earlier._ "The way it tries to find similarity between given stimuli". The algorithm does not work directly on a given stimulus. It charactersises each stimulus on the basis ofsome criteria. Then, for a given stimulus, it tries to find the most similar stimulus from the past, and applies the same set of functions in the same order. In a more realistic program, each stimuli will be defined not explictly, but by it's Type, Location of Stimulation and Size and so on. The functions execute in response to  identified, dynamic kind of stimuli that is 'similar' to a previous stimuli, based on these characteristics like 'Size' or 'Location'. This was missing in the previous version.

### How to use it :
The program takes in a stimuli, and gives some output.<br>
Based on whatever u like, give a score to the output it gave, say, 0 or 5 or 10 or -10.<br>

The scores are compared in memory everytime. Once a particular sequence of  functions is identifed to have a significantly larger score than all its counterparts, the program does not generate a random output, it will directly apply the same sequence of functions, and gives the output instantly.
Random Output making is done though 'PF', 'Process Function'
the local process that assumes the past functions to be applicable in future is called 'EPF' or 'Evocative Process Function'

_You can choose to skip the score by pressing **Enter**. In this case , the session is not recorded in memory._


I know that the algorithm hasn't been explained. I also know that the code is rather messy. A lot of things have been hurried up and this has resulted in some remarkably inefficient code in several parts of the program. It's efficency can be greatly imporved with some thoughtful changes in internal functions , mostly unrelated to the core processes. If you are genuinely intrested to know how it works and what it does , feel free to [mail](mailto:tejaskannampuzha@gmail.com) me and I will be more than happy to explain you everything in detail. I will try my best to make a documentation soon (not in the foreseeable future).

### What next ?
**The major limitation in this algorthim is that it accepts only a single input. A more realistic example should inclue multiple stimuli and multiprocessing. There is some (very low) possibilty that would start working on a multi stimuli version , but not in the near future.**



