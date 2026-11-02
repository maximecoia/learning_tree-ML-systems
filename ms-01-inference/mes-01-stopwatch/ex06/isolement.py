from time import perf_counter, process_time
import gc

from echauffement import mesurer_plusieurs
from chrono import mesurer

def mesurer_isole(f, repetitions=5, echauffement=1, horloge=perf_counter):
    etait_active = gc.isenabled()
    gc.disable()
    try:
        return mesurer_plusieurs(f, repetitions, echauffement, horloge)
    finally:
        if etait_active:
            gc.enable()

def temps_processus(f, horloge=process_time):
    return mesurer(f, horloge)