# In[]
# importing functions to initialise model variables
"""
[module to initialise the model variables]

"""

__name__ = "COVID-19 India config"
__version__ = "6.00.00.2020"
__doc__ = "variable configuration file for including with COVID-19 India model"
# put all initialization of model variables here
# model variables here are expected to be used as globals

import numpy as np

# In[]
# define all time constants
# starttime = 1  # start time
# endtime = 140  # length of run
# dt = .5  # integration step
# this is the time to display on plots
# time_points = np.arange(starttime, (endtime+1), dt)
# for array indexing for each time point
# no_of_time_points = int((endtime-starttime+1)/dt)
# j = starttime - 1  # past from array
# k = starttime  # present from array
# l = starttime + 1  # future from array
# jk = starttime - 1  # interval between past and present from array
# kl = starttime  # interval between present and future from array


def duration(start, end, step):
    """
    duration [set the start, end and step time for the simulation]

    [extended_summary]

    Arguments:
        start {[type]} -- [start time for the simulation]
        end {[type]} -- [end time for the simulation]
        step {[type]} -- [step time for the integration]
    """
    global time_points, no_of_time_points
    global starttime, endtime, dt
    starttime = start
    endtime = end
    dt = step
    time_points = np.arange(starttime, (endtime+1), dt)
    no_of_time_points = int((endtime-starttime+1)/dt)

# In[]


def initialise_model(program):
    """
    initialise_model

    all model variables declared as global and initialised here

    """
    print("Initialising ", __name__, " Version ", __version__, program)

    # global program_name
    # program_name = program

    global description
    description = {}  # create an empty dictionary of scenario parameters

    # constants: initial values of stocks
    global initial_population, exposed_population, infected_population

    # structural interventions
    global disease_duration, time_to_health, incubation_period
    global infectivity_of_asymptomatic, infectivity_of_symptomatic, n_p_death
    global area, density, imt
    global normal_births, normal_deaths, normal_inflow, normal_outflow

    # political interventions
    global closure_program1, closure_program2, effectiveness_of_closure, reduction_by_closure1
    global reduction_by_closure2, closure_time1, closure_time2
    global capacity_program, hospital_capacity, death_multiplier_from_capacity
    global lockdown_program, lockdown_time1, lockdown_time2, default_contact_rate
    global contact_rate_l1, contact_rate_l2, contact_rate, patient_zero_day
    global quarantine_program, proportion_exposed_quarantined, proportion_reduction_of_exposed
    global quarantine_time
    global proportion_infected_quarantined, proportion_reduction_of_infected

    # technological interventions
    global m_therapy
    global mask_program, effectiveness_of_mask, reduction_of_infection_by_mask
    global mask_time
    global immunity_program, effectivness_of_immunity, reduction_of_susceptible_by_immunity
    global immunity_time

    # dynamic variables: core model
    global susceptible, births
    global susceptible_deaths, exposed_deaths, recovered_deaths
    global exposure_rate, health_regain_rate
    global inflow_rate, outflow_rate
    global exposed, exposure_rate, infection_rate
    global exposed_inflow_rate, exposed_outflow_rate
    global infected, relapse_rate, covid_death_rate, recovery_rate
    global infected_inflow_rate, infected_outflow_rate
    global total_infected
    global recovered, health_regain_rate
    global recovered_inflow_rate, recovered_outflow_rate
    global covid_deaths, dmct, noncovid_deaths
    global population

    # dynamic varibales: auxillary variables for analysis
    global p_exposed, p_infected, p_recovered
    global exposed_prevalance, infected_prevalance, proportion_susceptible
    global under_capacity

    global infection_multiplier_from_density
    global infectiveness_e, infectiveness_i, R0, force_of_infection
    global transmission_rate

    global infection_growth_rate, infection_doubling_time

    # dynamic variables: core model
    susceptible = np.zeros(no_of_time_points)
    births = np.zeros(no_of_time_points)
    susceptible_deaths = np.zeros(no_of_time_points)
    exposed_deaths = np.zeros(no_of_time_points)
    recovered_deaths = np.zeros(no_of_time_points)
    noncovid_deaths = np.zeros(no_of_time_points)
    exposure_rate = np.zeros(no_of_time_points)
    health_regain_rate = np.zeros(no_of_time_points)
    inflow_rate = np.zeros(no_of_time_points)
    outflow_rate = np.zeros(no_of_time_points)
    exposed = np.zeros(no_of_time_points)
    exposure_rate = np.zeros(no_of_time_points)
    contact_rate = np.zeros(no_of_time_points)
    infection_multiplier_from_density = np.zeros(no_of_time_points)
    density = np.zeros(no_of_time_points)
    infection_rate = np.zeros(no_of_time_points)
    exposed_inflow_rate = np.zeros(no_of_time_points)
    exposed_outflow_rate = np.zeros(no_of_time_points)
    infected = np.zeros(no_of_time_points)
    relapse_rate = np.zeros(no_of_time_points)
    covid_death_rate = np.zeros(no_of_time_points)
    death_multiplier_from_capacity = np.zeros(no_of_time_points)
    recovery_rate = np.zeros(no_of_time_points)
    infected_inflow_rate = np.zeros(no_of_time_points)
    infected_outflow_rate = np.zeros(no_of_time_points)
    total_infected = np.zeros(no_of_time_points)
    recovered = np.zeros(no_of_time_points)
    recovered_inflow_rate = np.zeros(no_of_time_points)
    recovered_outflow_rate = np.zeros(no_of_time_points)
    population = np.zeros(no_of_time_points)
    health_regain_rate = np.zeros(no_of_time_points)
    covid_deaths = np.zeros(no_of_time_points)

    # dynamic varibales: auxillary variables for analysis
    p_exposed = np.zeros(no_of_time_points)
    p_infected = np.zeros(no_of_time_points)
    p_recovered = np.zeros(no_of_time_points)
    exposed_prevalance = np.zeros(no_of_time_points)
    infected_prevalance = np.zeros(no_of_time_points)
    proportion_susceptible = np.zeros(no_of_time_points)
    under_capacity = np.zeros(no_of_time_points)

    infectiveness_e = np.zeros(no_of_time_points)
    infectiveness_i = np.zeros(no_of_time_points)
    R0 = np.zeros(no_of_time_points)
    force_of_infection = np.zeros(no_of_time_points)
    transmission_rate = np.zeros(no_of_time_points)

    infection_growth_rate = np.zeros(no_of_time_points)
    infection_doubling_time = np.zeros(no_of_time_points)

    # initial values of stocks
    initial_population = 1.380004e9  # city of a million persons
    exposed_population = 4  # no exposed persons (on 30.01.2020 source:OWID)
    infected_population = 1  # no infected persons (on 30.01.2020 source:OWID)
    patient_zero_day = 30  # day when first patient identified

    # constants: parameters
    # normal urban birth rate per day census of India 2013 00-Ind T1
    normal_births = 17.3/(1000*365)
    # normal urban dealth rate per day census of India 2013 00-Ind T1
    normal_deaths = 5.6/(1000*365)

    # Source: Kolifarhood, Aghaali et al. 2020 – Epidemiological and Clinical Aspects
    disease_duration = 22.1
    # default: 3  # days for recovery default 5 (days)
    # days to become susceptible  after 7 days default 7 (days)
    time_to_health = 3650
    # time from being infected until onset of symptoms default 6 (days) dafault 3.6
    # Source: Lauer, Stephen A.; Grantz, Kyra H.; Bi, Qifang; Jones, Forrest K.; Zheng, Qulu; Meredith, Hannah R. et al. (2020): The Incubation Period of Coronavirus Disease 2019 (COVID-19) From Publicly Reported Confirmed Cases: Estimation and Application. In Annals of internal medicine 172 (9), pp. 577–582. DOI: 10.7326/M20-0504.
    incubation_period = 5.1
    # default: 4  # (source: OWID)
    # probability of infection from exposure to symptomatic person default 0.036 (probability)
    # 0.0159  # 0.01092 # 0.0046  # (avg source: OWID)
    infectivity_of_symptomatic = 0.002
    # probability of infection from exposure to asymptomatic person default 0.2 (probability)
    infectivity_of_asymptomatic = infectivity_of_symptomatic * 0.05  # 0.0008

    area = 3287263  # area of the India (sq km)
    # infection multiplier from density (multiplier)
    imt = 1, 1.05, 1.1, 1.2, 1.8, 2, 2.1

    closure_program1 = False  # Default no closure of inflow and outflow
    closure_program2 = False  # Default no closure of inflow and outflow
    # default percentage effectiveness of closure (percentage)
    closure_time1 = 80
    closure_time2 = endtime
    effectiveness_of_closure = 0.99
    # percentage reduction of infection probability by the use of masks (percentage)
    reduction_by_closure1 = (
        1-effectiveness_of_closure) if closure_program1 else 1.0
    reduction_by_closure2 = (
        1-effectiveness_of_closure) if closure_program2 else 1.0

    # normal pecentage population that flows in from outside every day (persons/day)
    normal_inflow = 0.001
    # normal pecentage population that flows outside every day (persons/day)
    normal_outflow = 0.001

    # default to no program to seek and quarantine persons, True if seeking and quarantine people ongoing
    quarantine_program = False
    quarantine_time = endtime
    # precentage of exposed persons tracked and quarantined (precentage)
    proportion_exposed_quarantined = 0
    # percentage of infected persons tracked and quarantined (precentage)
    proportion_infected_quarantined = 0
    # percentage reduction of exposed persons by quarantine (percentage)
    proportion_reduction_of_exposed = (
        1-proportion_exposed_quarantined) if quarantine_program else 1.0
    # percentage reduction of infected persons by quarantine (percentage)
    proportion_reduction_of_infected = (
        1-proportion_infected_quarantined) if quarantine_program else 1.0

    # Default  to no program to enhance hospital capacity
    capacity_program = False
    # proportion of population having hospital beds (proportion)
    hospital_capacity = 0.01
    # death multiplier from under capacity table (multiplier)
    dmct = 1, 5, 8, 10
    # case fatality rate or ratio between confirmed deaths and confirmed cases
    # source: https://ourworldindata.org/grapher/coronavirus-cfr
    n_p_death = 0.0019  # 0.137  # default: 3.25/1000

    lockdown_program = False
    # number of persons an average person interacts with during the day (persons/day)
    default_contact_rate = 100  # (source: OWID)
    contact_rate_l1 = default_contact_rate
    contact_rate_l2 = default_contact_rate
    lockdown_time1 = endtime
    lockdown_time2 = endtime

    mask_program = False  # Default to no masks in use
    # default percentage effectiveness of masks (percentage)
    mask_time = endtime
    effectiveness_of_mask = 0.8
    # percentage reduction of infection probability by the use of masks (percentage)
    reduction_of_infection_by_mask = (
        1.0-effectiveness_of_mask) if mask_program else 1.0

    # Default  to no program to boost immunity, True if immunity program is ongoing
    immunity_program = False
    immunity_time = endtime
    # default reduction of infection probability by increase of immunity (percentage)
    effectivness_of_immunity = 0.5
    # percentage reduction of infection probability by incresing immunity (percentage)
    reduction_of_susceptible_by_immunity = (
        1-effectivness_of_immunity) if immunity_program else 1.0

    m_therapy = 1  # multiplier from therapy for faster recovery (multiplier)


# In[]
# function to store the data of each simulation into a dataframe

def store():
    """
    store [function to store important model variable in a dataframe]

    [extended_summary]

    Returns:
        [DataFrame] -- [DataFrame containing variable in column names]
    """
    # add the lists of model variables to a dataframe and return it
    import pandas as pd
    return pd.DataFrame(list(zip(
        time_points, contact_rate,
        susceptible, exposed, infected, recovered, population,
        exposed_prevalance, infected_prevalance, proportion_susceptible,
        total_infected, covid_deaths, noncovid_deaths,
        p_exposed, p_infected, p_recovered,
        births, exposure_rate, infection_rate, relapse_rate, recovery_rate,
        health_regain_rate, covid_death_rate,
        exposed_inflow_rate, exposed_outflow_rate,
        infected_inflow_rate, infected_outflow_rate,
        infectiveness_i, infectiveness_e, force_of_infection, transmission_rate,
        R0, infection_growth_rate, infection_doubling_time,
        under_capacity, death_multiplier_from_capacity)),
        columns=[
        'time', 'contact_rate',
        'susceptible', 'exposed', 'infected', ' recovered', 'population',
        'exposed_prevalance', ' infected_prevalance', ' proportion_susceptible',
        'total_infected', 'covid_deaths', 'noncovid_deaths',
        'p_exposed', 'p_infected', 'p_recovered',
        'births', 'exposure_rate', 'infection_rate', 'relapse_rate', 'recovery_rate',
        'health_regain_rate', 'covid_death_rate',
        'exposed_inflow_rate', 'exposed_outflow_rate',
        'infected_inflow_rate', 'infected_outflow_rate',
        'infectiveness_i', 'infectiveness_e', 'force_of_infection', 'transmission_rate',
        'R0', 'infection_growth_rate', 'infection_doubling_time',
        'under_capacity', 'death_multiplier_from_capacity'])
