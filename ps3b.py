#Simulating the Spread of Disease and Virus Population Dynamics for MITx 6.00.2x 2014 session.

import numpy
import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# Iteration 2
#

class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        if (random.random() < float((self.getClearProb()))):
            return True
        else:
            return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        probability = self.maxBirthProb * (1 - popDensity) 
        if (random.random() < float((probability))):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()
            
            



class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        count = 0
        for i in self.viruses:
            count = count + 1
        return count


            

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        virusToRemove = 0
        for virus in self.viruses:
            if virus.doesClear() == True: #Must be called with instance of virus
                virusToRemove = virusToRemove + 1
        for times in range(virusToRemove):        
            foo = self.viruses.pop()
        newVirus = []
        for virus in self.viruses:
            popDensity = self.getTotalPop()/self.getMaxPop()
            try:
                newVirus.append(virus.reproduce(popDensity))
            except NoChildException:
                pass
        for littlefuckers in newVirus:
            self.viruses.append(littlefuckers)

        return self.getTotalPop()
#
# Iteration 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    #Creates a for loop that iterates over a number of trials
    avgTrialPop = []
    populations = []
    xAxis = []
    for trial in range(numTrials):
        #Creates a list of user specified number of viruses
        listOfViruses = []
        for i in range(numViruses):
            listOfViruses.append(SimpleVirus(maxBirthProb, clearProb))
        #Instantiates a patient
        bob = Patient(listOfViruses, maxPop)
        for j in range(300):
            bob.update()
            pop = bob.getTotalPop()
            populations.append(pop)

        avgTrialPop.append(populations)
        

        for element in range(300):
            sum = 0.0 
            for subelement in range(numTrials):
                sum += avgTrialPop[subelement][element]
            xAxis.append(sum/numTrials)

    ##Graphs average size of pop in y axis and Elapsed time steps in X axis
    pylab.figure() #insert number of figures in param (1)
    yAxis= [y for y in range(1,301)]
    pylab.plot(xAxis,yAxis) #insert (y,x)
    pylab.title("SimpleVirus Simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average virus population")
    pylab.legend() 
    pylab.show()


#
# Iteration 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        try:
            if self.resistances[drug] == True:
                return True
            else:
                return False
        except:
            pass

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        probability = self.maxBirthProb * (1 - popDensity) #Probability of reproduction
        #offSpringResistance = self.resistances
        count = 0
        offSpringResistances = {}

        #Checks if virus is resistant to all drugs, if virus is resistant to ALL drugs, reproduce it under the normal probability.   
        try:
            for drug in activeDrugs:
                if len(activeDrugs) == 0:
                    break
                if self.resistances[drug] == True:
                    count = count + 1
        except:
            count = 0
            #Decides if reproduces or not, must be inmune to all viruses    
        if (random.random() < float((probability)) and count == len(activeDrugs)):
            #Iterates over the resistance trait list from parent virus
            for resistance in self.resistances:
                if(random.random() > float(1 -self.mutProb)): #If mutation chance occurs
                    offSpringResistances[resistance] = not(self.resistances[resistance])

                else: #If offspring inherits the same resistance
                    offSpringResistances[resistance] = self.resistances[resistance]
                    
                    #returns the offspring with the inherited resistance
            return ResistantVirus(self.maxBirthProb, self.clearProb, offSpringResistances, self.mutProb) # Return instance because it passed reproducing odds
        else:
            raise NoChildException() # Didn't pass reproducive odds


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses,maxPop)
        self.listofDrugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if self.listofDrugs.__contains__(newDrug) == False:
            self.listofDrugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.listofDrugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        count = 0
        for virus in self.viruses:
            Resistance = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    Resistance = False
                    break
            if Resistance == True:
                count = count + 1
        return count

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        survivedViruses = [] #Creates a list for determining which viruses survive or not
        newVirus = []

        #Determines which viruses get to survive 
        for virus in self.viruses:
            if virus.doesClear() == False: 
                survivedViruses.append(virus)
        
        #Inserts viruses whom survived into list of viruses
        self.viruses = survivedViruses

        #Uses the new popDensity to reproduce virus particles and add new offsprings

        for virus in self.viruses:
            popDensity = self.getTotalPop()/self.getMaxPop()
            try:
                newVirus.append(virus.reproduce(popDensity, self.getPrescriptions())) #Takes into account the drug list from the treated patient 
            except NoChildException:
                pass
        for viruses in newVirus:
            self.viruses.append(viruses)

        return self.getTotalPop()


#
# Iteration 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    avgTrialPop = []
    totPop = None
    resPop = None
    xAxis = []

    for trials in range(numTrials):
        #Creates a list of user specified number of viruses
        listOfViruses = []
        #Adds viruses to the god damn list of viruses
        for i in range(numViruses):
            listOfViruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        #Instantiates a patient
        bob = TreatedPatient(listOfViruses, maxPop)
        #Create temporary lists, storing data for one set of trial
        tempTotPop = []
        tempResPop = []
        #Iterates over the 300 time steps
        for j in range(300):

            #Adds the drug at the middle of the graph
            if j == 150:
                bob.addPrescription('guttagonol')
            
            #Updates one data point of population for every time step
            tempTotPop.append(bob.update())
            
            #Update each point of resistant population for second graph:
            tempResPop.append(bob.getResistPop(['guttagonol']))
        if totPop == None:
            totPop = tempTotPop
            resPop = tempResPop
        else:
            for element in range(len(totPop)):
                totPop[element] = totPop[element] + tempTotPop[element]
                resPop[element] = resPop[element] + tempResPop[element]
    
    for i in range(len(totPop)):
        totPop[i] = totPop[i]/float(numTrials)
        resPop[i] = resPop[i]/float(numTrials)

    pylab.figure() #insert number of figures in param (1)
    xAxis= [y for y in range(0,300)]
    pylab.plot(xAxis,totPop) #insert (y,x)
    pylab.plot(xAxis,resPop)
    pylab.title("ResistantVirus Simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("# viruses")
    pylab.legend() 
    pylab.show()
