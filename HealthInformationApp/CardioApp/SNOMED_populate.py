#Script for importing the SNOMED terminlogy into the CardiologyApp Database:

from CardioApp.models import SNOMED_Diagnosis
import re

from pymedtermino import *
from pymedtermino.snomedct import *

from pymedtermino.all import *
from pymedtermino.snomedct import *

concept_list = SNOMEDCT.search("heart*disorder*") 

for concept in concept_list:Diagnosis.objects.all()
    new_concept = SNOMED_Diagnosis() 
    concept_string = str(concept)
    new_concept.code = concept_string[re.search("\[", concept_string).start() + 1 : re.search("\]", concept_string).start()]
    new_concept.snomed_diagnosis = concept_string[re.search("\#", concept_string).start():]
    new_concept.save()