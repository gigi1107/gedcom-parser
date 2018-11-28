
#NAME: Gigi Davidson
#DATE: Monday, April 30th 2018
#descendants.py


"""
GEDCOM parser design

Create empty dictionaries of individuals and families
Ask user for a file name and open the gedcom file
Read a line
Skip lines until a FAM or INDI tag is found
    Call functions to process those two types
Print descendant chart when all lines are processed

Processing an Individual
Get pointer string
Make dictionary entry for pointer with ref to Person object
Find name tag and identify parts (surname, given names, suffix)
Find FAMS and FAMC tags; store FAM references for later linkage
Skip other lines

Processing a family
Get pointer string
Make dictionary entry for pointer with ref to Family object
Find HUSB WIFE and CHIL tags
    Add included pointer to Family object
    [Not implemented ] Check for matching references in referenced Person object
        Note conflicting info if found.
Skip other lines

Print info from the collect of Person objects
Read in a person number
Print pedigree chart
"""
#Constants

FILENAME = "/Users/gdavidson/Documents/OldClasses/CPSC3400/Kennedy.ged"

#-----------------------------------------------------------------------

class Person():
    # Stores info about a single person
    # Created when an Individual (INDI) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self,ref):
        # Initializes a new Person object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._asSpouse = []  # use a list to handle multiple families
        self._asChild = None
        self._events = []
                
    def addName(self, nameString):
        # Extracts name parts from nameString and stores them
        names = line[6:].split('/')  #surname is surrounded by slashes
        self._given = names[0].strip()
        self._surname = names[1]
        self._suffix = names[2].strip()

    def addIsSpouse(self, famRef):
        # Adds the string (famRef) indicating family in which this person
        # is a spouse, to list of any other such families
        self._asSpouse += [famRef]
        
    def addIsChild(self, famRef):
        # Stores the string (famRef) indicating family in which this person
        # is a child
        self._asChild = famRef

    def printDescendants(self, prefix=''):
        # print info for this person and then call method in Family
        print(prefix + self.__str__())
        # recursion stops when self is not a spouse
        for fam in self._asSpouse:
            families[fam].printFamily(self._id,prefix)

    def addEvent(self, event):
        #Adds an event object to the person object
        self._events += [event]

    def isDescendant(self, otherPerson):
        #recursively checks family members of self
        #calls processDecendents in family class
        if self._id == otherPerson._id:
            return True
        else:
            for fam in self._asSpouse:
                return families[fam].processDescendants(otherPerson)                         
        return False

    def printAncestors(self, numGenerations=0, prefix = ''):
        #recursively prints ancestors in a tree format
        #calls printParents in family class
        if self._asChild:
            families[self._asChild].printParents(numGenerations, prefix + ' ')
        print(prefix + str(numGenerations) + self.__str__())
        
    def closestCommonAncestor(self,otherPerson, count1 = 0, count2 = 0):
        #intersects self with otherPerson's ancestor trees to find whether they have
        #any common ancestors, and if so, returns the identifier of the ancestor that
        #is the fewest generations removed from one of the two persons.
        #return identifier
        selfAncestors = {}
        otherPersonAncestors = {}
        persons[self._id].addAncestorsToDictionary(selfAncestors)
        persons[otherPerson._id].addAncestorsToDictionary(otherPersonAncestors)
        #compare dictionaries and find matches
        matches1 = {}
        matches2 = {}
        for key1 in selfAncestors:
            for key2 in otherPersonAncestors:
                if key1 == key2:
                    matches1[key1] = selfAncestors[key1]
                    matches2[key2] = otherPersonAncestors[key2]
        if not matches1:
            return "No common ancestors!"
        mini1 = 10
        closestAncestor1 = None
        mini2 = 10
        closestAncestor2 = None
        for key in matches1:
            #find the ancestor with the lowest number
            if matches1[key] < mini1:
                mini1 = matches1[key]
                closestAncestor1 = key
        #find the ancestor with the lowest number in the second person
        for key in matches2:
            if matches2[key] < mini2:
                mini2 = matches2[key]
                closestAncestor2 = key
        closestAncestor = None
##        print("closest ancestor1: " +closestAncestor1._id)
##        print("closest ancestor2: " +closestAncestor2._id)
        if matches1[closestAncestor1] < matches2[closestAncestor2]:
            closestAncestor = closestAncestor1
        else:
            closestAncestor = closestAncestor1
        print(getRelationship(selfAncestors[closestAncestor],otherPersonAncestors[closestAncestor]))
        return str(persons[closestAncestor])
            
    def addAncestorsToDictionary(self,dictionary,numGen = 0):
        #helper function to closest common ancestor, passes in a dictionary and
        #a generation number
        #recursive
        if self._asChild:
            families[self._asChild].getParents(numGen + 1,dictionary)
        dictionary[self._id] = numGen
        
    def __str__(self):
        if self._asChild: # make sure value is not None
            childString = ' asChild: ' + self._asChild
        else: childString = ''
        if self._asSpouse != []: # make sure _asSpouse list is not empty
            spouseString = ' asSpouse: ' + str(self._asSpouse)
        else: spouseString = ''
        eventsString = ''
        if self._events != []:
            for i in self._events:
                eventsString += str(i)
        else:
            eventsString = ''
        return self._given + ' ' + self._surname.upper()\
               + ' ' + self._suffix + eventsString

#-----------------------------------------------------------------------

class Event():
    #stores date and place info

    def __init__(self,typeOf):
        #Initializes a new Event object, storing the string (ref) by
        #which it can be referenced.
        self._type = typeOf.strip()
        self._date = None
        self._place = None
        
    def addEventDate(self, date):
        #adds the data of the event to the event object (self)
        self._date = date.strip()

    def addEventPlace(self, place):
        #adds the place of the event as a string to the event obj(self)
        self._place = place.strip()

    def __str__(self):
        
        if self._date:
            dateStr = str(self._date)
        else:
            dateStr = ''
        if self._place:
            place = str(self._place)
        else:
            place = ""
        if self._type == 'BIRT':
            selfString = 'b '
        elif self._type =='DEAT':
            selfString = 'd '
        elif self._type == 'MARR':
            selfString = 'm '
            
        return selfString+ dateStr + " "+ place+ " "

    
 
#-----------------------------------------------------------------------
                    
class Family():
    # Stores info about a family
    # Created when an Family (FAM) GEDCOM record is processed.
    #-------------------------------------------------------------------

    def __init__(self, ref):
        # Initializes a new Family object, storing the string (ref) by
        # which it can be referenced.
        self._id = ref
        self._husband = None
        self._wife = None
        self._children = []
      

    def addHusband(self, personRef):
        # Stores the string (personRef) indicating the husband in this family
        self._husband = personRef

    def addWife(self, personRef):
        # Stores the string (personRef) indicating the wife in this family
        self._wife = personRef

    def addChild(self, personRef):
        # Adds the string (personRef) indicating a new child to the list
        self._children += [personRef]

    def addMarriage(self, event):
        #adds a marriage (type event) to the family.
        #for the most part, this will be attached to the husband's name.
        if self._husband:
            curr= persons[self._husband]
        elif self._wife:
            curr = persons[self._wife]
        curr.addEvent(event)
           
    def printFamily(self, firstSpouse, prefix):
        # Used by printDecendants in Person to print spouse
        # and recursively invoke printDescendants on children
        if prefix != '':
            prefix = prefix[:-2]+'  '
        if self._husband == firstSpouse:
            if self._wife:  # make sure value is not None
                print(prefix+ '+' +str(persons[self._wife]))
        else:
            if self._husband:  # make sure value is not None
                print(prefix+ '+' +str(persons[self._husband]))
        for child in self._children:
             persons[child].printDescendants(prefix+'|--')

#self- PErson obj
#otherPerson- Person obj
    def processDescendants(self, otherPerson):
        #used by isDescendant in Person to process self and recursively
        #invoke isDescendant on children
        flag = False
        if self._children:
            for child in self._children:
                if persons[child].isDescendant(otherPerson):
                    flag = True
        return flag
        
    def printParents(self, generation, prefix):
        #used by printAncestors in Person class
        #prints parents of fam1 husband and wife
        if self._husband:
            persons[self._husband].printAncestors(generation + 1, prefix)
        if self._wife:
            persons[self._wife].printAncestors(generation + 1, prefix)

    def getParents(self, gen, dictionary):
        #used by addAncestorsToDictionary in its recursive structure
        #uses addAncestorsToDictionary
        if self._husband:
            persons[self._husband].addAncestorsToDictionary(dictionary, gen)
        if self._wife:
            persons[self._wife].addAncestorsToDictionary(dictionary, gen)
            
    def __str__(self):
        if self._husband: # make sure value is not None
            husbString = ' Husband: ' + self._husband
        else: husbString = ''
        if self._wife: # make sure value is not None
            wifeString = ' Wife: ' + self._wife
        else: wifeString = ''
        if self._children != []: childrenString = ' Children: ' + str(self._children)
        else: childrenString = ''
        
        return husbString + wifeString + childrenString


#-----------------------------------------------------------------------

def getRelationship(num1, num2):
    #helper function to obtain the relationship between two people
    #Given the distance between that person and the most recent common
    #ancestor. num1 and num2 are ints.
    if (num1 == 1 and num2 == 0) or (num1 == 0 and num2 == 1):
        return "Relationship: child/parent"
    elif num1 == 1 and num2 ==1:
        return "Relationship: siblings"
    elif (num1 == 0 and num2 == 2) or (num1 == 2 and num2 == 0):
        return "Relationship: grandparent/ grandchild"
    elif num1 == 1 and num2 == 2:
        return "Relationship: Person 1 is the aunt/uncle of P2"
    elif num1 == 2 and num2 == 1:
        return "Relationship: Person 1 is the niece/nephew of P2"
    elif num1 == 2 and num2 == 2:
        return "Relationship: cousins"
    elif num1 == 3 and num2 ==3:
        return "Relationship: second cousins"
    elif num1 == 1 and num2 == 3:
        return "Relationship: grandaunt/granduncle"
    elif num1 == 3 and num2 == 1:
        return "Relationship: grandneice/ grandnephew"
    elif (num1 == 2 and num2 == 3) or (num1 == 3 and num2 == 2):
        return "Relationship: 1st cousins once removed"
    elif (num1 == 2 and num2 == 4) or (num1 == 4 and num2 == 2):
        return "Relationship: 1st cousins twice removed"
    else:
        return "Relationship: unknown"
        
def getPointer(line):
    # A helper function used in multiple places in the next two functions
    # Depends on the syntax of pointers in certain GEDCOM elements
    # Returns the string of the pointer without surrounding '@'s or trailing
    return line[8:].split('@')[0]


#@Param newPerson is a person object
def processPerson(newPerson):

    global line
    line = f.readline()
    while line[0] != '0': # process all lines until next 0-level
        tag = line[2:6]  # substring where tags are found in 0-level elements
        if tag == 'NAME':
            newPerson.addName(line[7:])
        elif tag == 'FAMS':
            newPerson.addIsSpouse(getPointer(line))
        elif tag == 'FAMC':
            newPerson.addIsChild(getPointer(line))
        elif tag =='BIRT'or tag =='DEAT' or tag == 'MARR':
            newEvent = Event(tag)
            line = f.readline()
            tag = line[2:6]
            if tag == 'DATE':
                newEvent.addEventDate(line[7:])
                line = f.readline()
                tag = line[2:6]
            if tag == 'PLAC':
                newEvent.addEventPlace(line[7:])
            newPerson.addEvent(newEvent)
        # read to go to next line
        line = f.readline()

def processFamily(newFamily):
    global line
    line = f.readline()
    while line[0] != '0':  # process all lines until next 0-level
        tag = line[2:6]
        if tag == 'HUSB':
            newFamily.addHusband(getPointer(line))
        elif tag == 'WIFE':
            newFamily.addWife(getPointer(line))
        elif tag == 'CHIL':
            newFamily.addChild(getPointer(line))
        ## add code here to look for other fields 
        elif tag == 'MARR':
            newEvent = Event(tag)
            line = f.readline()
            tag = line[2:6]
            if tag == 'DATE':
                newEvent.addEventDate(line[7:])
                line = f.readline()
                tag = line[2:6]
            if tag == 'PLAC':
                newEvent.addEventPlace(line[7:])
            newFamily.addMarriage(newEvent)
        # read to go to next line
        line = f.readline()


## Main program starts here

persons = {}  # dictionary of ID: Person_object
families = {} # to save references to all of the Family objects

f = open (FILENAME)
line = f.readline()
while line != '':
    fields = line.strip().split(' ')
    # print(fields)
    if line[0] == '0' and len(fields) > 2:
        # print(fields)
        if (fields[2] == "INDI"): 
            ref = fields[1].strip('@')
            persons[ref] = Person(ref)  ## store ref to new Person
            processPerson(persons[ref])
        elif (fields[2] == "FAM"):
            ref = fields[1].strip('@')
            families[ref] = Family(ref) ## store ref to new Family
            processFamily(families[ref])      
        else:    # 0-level line, but not of interest -- skip it
            line = f.readline()
    else:    # skip lines until next candidate 0-level line
        line = f.readline()

# Optionally print out all information stored about individuals
for ref in sorted(persons.keys()):
    print(ref+':', persons[ref])

# Optionally print out all information stored about families
for ref in sorted(families.keys()):
    print(ref+':', families[ref])


userInput = 'y'
while(userInput == 'y'):
    person = input("Enter person ID for descendants chart:")
    while person not in persons:
        person = input("Please enter VALID person ID for descendants chart:")
    persons[person].printDescendants()

    
    otherPerson = input("Enter another Person Id to check to see if that "+
                        "person is a descendant of the previous person"+
                        " entered:")
    while otherPerson not in persons:
        otherPerson = input("Please enter VALID person ID to "+
                            "check against first person: ")
    print(persons[person].isDescendant(persons[otherPerson]))

    print("Now findning the ancestral tree to otherPerson:")

    persons[otherPerson].printAncestors()


    personA = input("Now finding the most recent common ancestor to the "+
                    "two people indicated: Please list the first person: ")
    while personA not in persons:
        personA = input("Please enter VALID person: ")

    personB = input("Now list the second person: ")
    while personB not in persons:
        personB = input("Please enter VALID person: ")

    print("Closest common ancestor is: ")

    print(persons[personA].closestCommonAncestor(persons[personB]))

    
    userInput = input("Would you like to enter more people? y or n: ")
    while userInput != 'y' and userInput != 'n':
        userInput = input("Would you like to enter more people? y or n: ")
    
    


