# In[]
# importing functions to reset parameters for scenarios
"""
[module with functions to set the model parameters for scenarios]

"""

__name__ = "COVID-19"
__version__ = "5.6.01.2020"
__doc__ = "functions to change parameter values for different scenarios of covid_model_india"

# functions to reset parameters for scenarios
import covid_india_model_config as cmc


def city_size(size):
    # size of city for simulation
    cmc.initial_population = size
    cmc.description['initial_population'] = ("population of city: " , cmc.initial_population)
    cmc.description['infection_multiplier_from_density'] = ("death multiplier due to density: ", cmc.initial_population/cmc.area)

def infection_seed(size):
    # number of initial infected persons
    cmc.infected_population = size
    cmc.description['infected_population'] = ("number of initial infected persons: ", cmc.infected_population)


def exposure_seed(size):
    # number of initial exposed persons
    cmc.exposed_population = size
    cmc.description['exposed_population'] = ("number of initial exposed persons: ", cmc.exposed_population)


def infectivity(infectivity):
    infectivity_of_exposed = cmc.infectivity_of_asymptomatic
    infectivity_of_infected = infectivity
    # use of masks will reduce infectivity: turn use_of_masks = 1 and decide the effectiveness_of_mask between 0 to 1
    cmc.infectivity_of_symptomatic = infectivity_of_infected
    # normal infection probability from infected population or risk of infection from symptomatic (probability)
    cmc.infectivity_of_asymptomatic = infectivity_of_exposed
    # normal infection probability from exposed population risk of infection from asymptomatic (probability)
    cmc.description['infectivity_of_asymptomatic'] = ("infection probability from exposed population risk of infection from asymptomatic (probability): ", cmc.infectivity_of_asymptomatic)
    cmc.description['infectivity_of_symptomatic'] = ("infection probability from infected population or risk of infection from symptomatic (probability): ", cmc.infectivity_of_symptomatic)


def masks(mask_effectivenss, mask_time):
    # normal reduction of infection probability by the use of masks (probability)
    cmc.reduction_of_infection_by_mask = 1.0-mask_effectivenss
    cmc.mask_program = True
    cmc.mask_time = mask_time
    cmc.description['reduction_of_infection_by_mask'] = ("reduction of infection probability by the use of masks (proportion): ", cmc.reduction_of_infection_by_mask)
    cmc.description['mask_program'] = ("mask use program: ", cmc.mask_program)
    cmc.description['mask_time'] = ("time when masks introduced: ", cmc.mask_time)


def immunity(immunity_effectiveness, immunity_time):
    # immunity boost with vitamin C and other immunity boosters will reduce infectivity
    # : turn immunity_program = 1 and decide the effectiveness_of_immunity between 0 to 1
    # normal reduction of infection probability by immunity programs
    cmc.reduction_of_susceptible_by_immunity = 1-immunity_effectiveness
    cmc.immunity_program = True
    cmc.immunity_time = immunity_time
    cmc.description['reduction_of_susceptible_by_immunity'] = ("infection probability from infected population or risk of infection from symptomatic (probability): ", cmc.reduction_of_susceptible_by_immunity)
    cmc.description['immunity_program'] = ("infection probability from infected population or risk of infection from symptomatic (probability): ", cmc.immunity_program)
    cmc.description['immunity_time'] = ("time when immunity program introduced (day): ", cmc.immunity_time)

def quarantine(proportion_quarantined, quarantine_time):
    proportion_exposed_quarantined = proportion_quarantined
    proportion_infected_quarantined = proportion_quarantined
    # quarantine of exposed persons or infected persons will reduce prevalance
    # : change proportion_exposed_quarantined and proportion_infected_quarantined between 0 to 1
    # prevalence is the number of disease cases present in a particular population at a given time
    cmc.proportion_reduction_of_exposed = 1-proportion_exposed_quarantined
    # normal reduction of infection probability by quaratine program for exposed or asymptomatic
    cmc.proportion_reduction_of_infected = 1-proportion_infected_quarantined
    # normal reduction of infection probability by quaratine program for infected or symptomatic
    cmc.quarantine_time = quarantine_time
    cmc.quarantine_program = True
    cmc.description['proportion_reduction_of_exposed'] = ("reduction of infection probability by quaratine program for exposed or asymptomatic (proportion): ", cmc.proportion_reduction_of_exposed)
    cmc.description['proportion_reduction_of_infected'] = ("reduction of infection probability by quaratine program for exposed or symptomatic (proportion): ", cmc.proportion_reduction_of_infected)
    cmc.description['quarantine_time'] = ("isolation of exposed and infected (day)", cmc.quarantine_time)

def lockdown1(contacts, lockdown_time=85):
    # lockdown reduces the effective contacts that a person will encounter: change the contact_rate between 1 and 100
    # currently between 50 and 100 according to source:
    # number of persons an average person interacts with during the day (persons/day)
    cmc.contact_rate_l1 = contacts
    cmc.lockdown_time1 = lockdown_time
    cmc.lockdown_program1 = True
    cmc.lockdown_program2 = False
    cmc.description['lockdown_program 1'] = ("lockdown program: ", cmc.lockdown_program)
    cmc.description['lockdown_time 1'] = ("lockdown effective from: ", cmc.lockdown_time1)
    cmc.description['contact_rate 1'] = ("number of persons a person interacts with every day (persons/day): ", cmc.contact_rate_l1)

def lockdown2(contacts, lockdown_time):
    # lockdown reduces the effective contacts that a person will encounter: change the contact_rate between 1 and 100
    # currently between 50 and 100 according to source:
    # number of persons an average person interacts with during the day (persons/day)
    cmc.contact_rate_l2 = contacts
    cmc.lockdown_time2 = lockdown_time
    cmc.lockdown_program2 = True
    cmc.lockdown_program1 = False
    cmc.description['lockdown_program 2'] = ("lockdown program: ", cmc.lockdown_program)
    cmc.description['lockdown_time 2'] = ("lockdown effective from: ", cmc.lockdown_time2)
    cmc.description['contact_rate 2'] = ("number of persons a person interacts with every day (persons/day): ", cmc.contact_rate_l2)

def closure1(effectiveness_of_closure, closure_time):
    # normal reduction of percentage of persons moving in or out of the city (percentage)
    cmc.reduction_by_closure1 = 1.0-effectiveness_of_closure
    cmc.closure_program1 = True
    cmc.closure_program2 = False
    cmc.description['reduction_by_closure'] = ("reduction of percentage of persons moving in or out of the country (percentage): ", cmc.reduction_by_closure1)
    cmc.closure_time1 = closure_time
    cmc.description['closure_time1'] = ("time that the closure is being implemented: ", cmc.closure_time1)

def closure2(effectiveness_of_closure, closure_time):
    # normal reduction of percentage of persons moving in or out of the city (percentage)
    cmc.reduction_by_closure2 = 1.0-effectiveness_of_closure
    cmc.closure_program1 = False
    cmc.closure_program2 = True
    cmc.description['reduction_by_closure'] = ("reduction of percentage of persons moving in or out of the country (percentage): ", cmc.reduction_by_closure2)
    cmc.closure_time2 = closure_time
    cmc.description['closure_time2'] = ("time that the closure is being implemented: ", cmc.closure_time2)

def incubation(time_to_symptoms):
    # currently between 3 and 6 days according to source:
    # time from being infected until onset of symptoms
    cmc.incubation_period = time_to_symptoms
    cmc.description['incubation_period'] = ("time from being infected until onset of symptoms (days): ", cmc.incubation_period)


def death_by_infection(proportion_infected_dying):
    # currently between 0.01 and 0.02 according to source:
    # normal proportion of infected dying (proportion)
    cmc.n_p_death = proportion_infected_dying
    cmc.description['n_p_death'] = ("proportion of infected dying (proportion): ", cmc.n_p_death)


def illness_duration(time_to_recovery):
    # currently between 4 and 10 according to source:
    cmc.disease_duration = time_to_recovery # days for recovery (days)
    cmc.description['disease_duration'] = ("days for recovery (days): ", cmc.disease_duration)


def recovery(time_to_healthy):
    # currently assumed to be 30 days after initial 120 days according to source:
    # days to become healthy after 90 days (days)
    cmc.time_to_health = time_to_healthy
    cmc.description['time_to_health'] = ("days to become healthy after 90 days (days): ", cmc.time_to_health)


def hospitals(proportion_served):
    # currently between 0.01 and 0.02 according to source:
    # proportion of population having hospital beds (proportion)
    cmc.hospital_capacity = proportion_served
    cmc.capacity_program = True
    cmc.description['hospital_capacity'] = ("proportion of population having hospital beds (proportion): ", cmc.hospital_capacity)
    cmc.description['capacity_program'] = ("Hospital capacity boost program: ", cmc.capacity_program)


def deaths_by_undercapacity(ty):
    cmc.dmct = ty # death multiplier from under capacity table (multiplier)
    cmc.description['dmct'] = ("death multiplier from under capacity table (multiplier): ", cmc.dmct)
