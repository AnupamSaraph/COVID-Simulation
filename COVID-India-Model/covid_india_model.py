# In[]
# import external modules
"""
 [COVID 19 SEIR model]

[the variables used here are initialized in covid_india_model_config
pass the model function to the simulator to simulate the model
this is the core model with definitions of epidemiology
adapted to model the transmission of disease
]
"""
__version__ = "6.0.00.2020"
__doc__ = "SEIR model to explore the response and options of India to COVID-19"
__name__ = "COVID-19 India Model"

# this has all the functions to initialise the model variables
import covid_india_model_config as cmc
import SD as sd  # has all system dynamics builtin functions
import random

# In[]
# the model equations


def model(t, dt, j, k, jk, kl):
    """
    model the model equations for computation at each timepoint

    [c = number of contacts in the time unit,
    χ = infectiveness of one contact with an infective
    γ(t) the rate at which infectives recover from the disease
    λ(t) = cχ N(t)/I(t) =force_of_infection (1)
    N(t) = S(t)+I(t)+R(t) = total population (2)]
    R0 = cχ/γ = basic reproductive number (10)
    [Source: THE MATHEMATICAL MODELING OF EPIDEMICS
    Mimmo Iannelli]

    Table 1 Summary of notation.
    S Susceptibles
    E Exposed people in the latent period
    I Infectives R Recovered people with immunity
    m,s,e,i,r Fractions of the population in the classes above
    β Contact rate
    1/δ Average period of passive immunity
    1/ε Average latent period
    1/γ Average infectious period
    R0 Basic reproduction number
    σ Contact number
    R Replacement number

    dS/dt =−βIS/N,
    S(0) = So ≥0,
    dI/dt = βIS/N −γI,
    I(0) = Io ≥0,
    dR/dt = γI,
    R(0) = Ro ≥0,

    where S(t), I(t), and R(t) are the numbers in these classes,
    so that S(t)+I(t)+R(t)= N

    [Source: SIAM REVIEW Vol. 42, No. 4, pp. 599–653
    The Mathematics of Infectious Diseases
    Herbert W. Hethcote]

    """

    # Now write the model equations
    if t > cmc.starttime:
        cmc.susceptible[k] = (cmc.susceptible[j]
                              + cmc.dt
                              * ((cmc.births[jk] - cmc.susceptible_deaths[jk])
                                 - cmc.exposure_rate[jk]
                                 + cmc.health_regain_rate[jk]
                                 + cmc.inflow_rate[jk]
                                 - cmc.outflow_rate[jk]))  # susceptible population

        cmc.exposed[k] = (cmc.exposed[j]
                          + cmc.dt
                          * (cmc.exposure_rate[jk]
                             - cmc.infection_rate[jk]
                             - cmc.exposed_deaths[jk]
                             + cmc.exposed_inflow_rate[jk]
                             - cmc.exposed_outflow_rate[jk]))  # exposed population

        cmc.infected[k] = (cmc.infected[j]
                           + cmc.dt
                           * (cmc.infection_rate[jk]
                              + cmc.relapse_rate[jk]
                              - cmc.covid_death_rate[jk]
                              - cmc.recovery_rate[jk]
                              + cmc.infected_inflow_rate[jk]
                              - cmc.infected_outflow_rate[jk]))  # infected population

        cmc.recovered[k] = (cmc.recovered[j]
                            + cmc.dt
                            * (cmc.recovery_rate[jk]
                               - cmc.recovered_deaths[jk]
                               - cmc.relapse_rate[jk]
                               - cmc.health_regain_rate[jk]
                               + cmc.recovered_inflow_rate[jk]
                               - cmc.recovered_outflow_rate[jk]))  # recovered population

        cmc.covid_deaths[k] = (cmc.covid_deaths[j]
                               + cmc.dt
                               * (cmc.covid_death_rate[jk]))  # cumulative deaths due to covid

        cmc.total_infected[k] = (cmc.total_infected[j]
                                 + cmc.dt
                                 * (cmc.infection_rate[jk]
                                    + cmc.relapse_rate[jk]))   # cumulative infected population
        # cumulative non covid deaths (persons)
        cmc.noncovid_deaths[k] = (cmc.noncovid_deaths[j]
                                  + cmc.dt
                                  * (cmc.susceptible_deaths[jk]
                                     + cmc.exposed_deaths[jk]
                                     + cmc.recovered_deaths[jk]))

    else:
        cmc.susceptible[k] = cmc.initial_population
        cmc.exposed[k] = cmc.exposed_population
        cmc.infected[k] = cmc.infected_population

    cmc.population[k] = cmc.susceptible[k] + \
        cmc.exposed[k] + cmc.infected[k] + cmc.recovered[k]
    cmc.p_exposed[k] = cmc.exposed[k]/cmc.susceptible[k]
    cmc.p_infected[k] = cmc.infected[k]/cmc.susceptible[k]
    cmc.p_recovered[k] = cmc.recovered[k]/cmc.p_infected[k]

    cmc.exposed_prevalance[k] = (cmc.exposed[k]/cmc.population[k])
    cmc.infected_prevalance[k] = (cmc.infected[k]/cmc.population[k])
    cmc.proportion_susceptible[k] = (cmc.susceptible[k]/cmc.population[k])

    cmc.under_capacity[k] = cmc.infected[k] / \
        (cmc.initial_population*cmc.hospital_capacity)

    cmc.density = cmc.initial_population/cmc.area
    cmc.infection_multiplier_from_density[k] = sd.tabhl(
        cmc.imt, cmc.density, 0.5e4, 7.5e4, 1e4)

    # intervention programs
    # lockdown program
    r1 = random.randint(sd.ifthenelse(
        cmc.contact_rate_l1 < cmc.default_contact_rate, cmc.contact_rate_l1, cmc.default_contact_rate),
        sd.ifthenelse(
        cmc.contact_rate_l1 < cmc.default_contact_rate, cmc.default_contact_rate, cmc.contact_rate_l1)
    )

    r2 = random.randint(sd.ifthenelse(
        cmc.contact_rate_l1 < cmc.contact_rate_l2, cmc.contact_rate_l1, cmc.contact_rate_l2),
        sd.ifthenelse(
        cmc.contact_rate_l1 < cmc.contact_rate_l2, cmc.contact_rate_l2, cmc.contact_rate_l1)
    )
    cmc.contact_rate[k] = sd.clip(cmc.default_contact_rate,
                                  sd.clip(
                                      r1,
                                      r2,
                                      t,
                                      cmc.lockdown_time2/dt),
                                  t, cmc.lockdown_time1/dt)

    # closure
    reduction_by_closure = sd.clip(1,
                                   sd.clip(
                                       cmc.reduction_by_closure1,
                                       cmc.reduction_by_closure2,
                                       t,
                                       cmc.closure_time2/dt),
                                   t, cmc.closure_time1/dt)

   
    # mask program
    reduction_of_infection_by_mask = sd.clip(
        1, cmc.reduction_of_infection_by_mask, t, cmc.mask_time/dt)

    # quarantine program
    reduction_of_exposed_by_isolation = sd.clip(
        1, cmc.proportion_reduction_of_exposed, t, cmc.quarantine_time/dt)
    reduction_of_infected_by_isolation = sd.clip(
        1, cmc.proportion_reduction_of_infected, t, cmc.quarantine_time/dt)

    # immunity boost program
    reduction_of_susceptible_by_immunity = sd.clip(1, cmc.reduction_of_susceptible_by_immunity,
                                                  t, cmc.immunity_time/dt)

    cmc.infectiveness_e[k] = cmc.infectivity_of_asymptomatic * \
        reduction_of_infection_by_mask * \
        reduction_of_exposed_by_isolation * \
        cmc.contact_rate[k] * cmc.infection_multiplier_from_density[k]

    cmc.infectiveness_i[k] = cmc.infectivity_of_symptomatic * \
        reduction_of_infection_by_mask * \
        reduction_of_infected_by_isolation * \
        cmc.contact_rate[k] * cmc.infection_multiplier_from_density[k]

    cmc.force_of_infection[k] = (cmc.infectiveness_e[k]*cmc.exposed_prevalance[k]) + (
        cmc.infectiveness_i[k]*cmc.infected_prevalance[k])
    cmc.transmission_rate[k] = cmc.force_of_infection[k]*cmc.susceptible[k] * \
        reduction_of_susceptible_by_immunity

    # births and deaths of the population
    # births (persons/day)
    cmc.births[kl] = cmc.population[k] * \
        cmc.normal_births
    # non covid deaths (persons/day)
    cmc.susceptible_deaths[kl] = max(0, cmc.susceptible[k] * cmc.normal_deaths)
    cmc.exposed_deaths[kl] = max(0, cmc.exposed[k] * cmc.normal_deaths)
    cmc.recovered_deaths[kl] = max(0, cmc.recovered[k] * cmc.normal_deaths)
    # inflows and outflows of the susceptible population

    cmc.inflow_rate[kl] = cmc.susceptible[k] * \
        cmc.normal_inflow * reduction_by_closure
    cmc.outflow_rate[kl] = cmc.susceptible[k] * \
        cmc.normal_outflow * reduction_by_closure
    # exposure rate (persons/day)
    cmc.exposure_rate[kl] = min(cmc.susceptible[k], cmc.transmission_rate[k])
    # exposed persons coming into the city
    cmc.exposed_inflow_rate[kl] = cmc.exposed[k] * \
        cmc.normal_inflow * reduction_by_closure
    # exposed persons leaving the city
    cmc.exposed_outflow_rate[kl] = cmc.exposed[k] * \
        cmc.normal_outflow * reduction_by_closure
    # rate of daily cases (persons/day)

    cmc.infection_rate[kl] = cmc.exposed[k]/cmc.incubation_period
    # infected persons coming into the city
    cmc.infected_inflow_rate[kl] = cmc.infected[k] * \
        cmc.normal_inflow * reduction_by_closure
    # infected persons leaving the city
    cmc.infected_outflow_rate[kl] = cmc.infected[k] * \
        cmc.normal_outflow * reduction_by_closure
    # relapse rate (persons/day)
    cmc.relapse_rate[jk] = cmc.recovered[k] * \
        random.random()*0.0
    # death multiplier from undercapacity of hospitals  (dimensionless)
    cmc.death_multiplier_from_capacity[k] = sd.tabhl(cmc.dmct, cmc.under_capacity[k], 1, 5, 1)
    # covid death rate (persons/day)
    cmc.covid_death_rate[kl] = max(
        0, (cmc.infected[k]*cmc.n_p_death*cmc.death_multiplier_from_capacity[k]))
    # recovery rate (persons/day)

    cmc.recovery_rate[kl] = max(0, (cmc.infected[k] / cmc.disease_duration *
                                    cmc.m_therapy))
    # rate at which recovered rejoin the susceptabli or susceptible population (person/day)
    cmc.health_regain_rate[kl] = 0
    # max(0, (cmc.recovered[k]/cmc.time_to_health))
    cmc.recovered_inflow_rate[kl] = cmc.recovered[k] * \
        cmc.normal_inflow * reduction_by_closure
    # infected persons leaving the city
    cmc.recovered_outflow_rate[kl] = cmc.recovered[k] * \
        cmc.normal_outflow * reduction_by_closure

    cmc.R0[k] = (cmc.infectiveness_e[k] +
                 cmc.infectiveness_i[k])/cmc.recovery_rate[k]
    cmc.infection_growth_rate[k] = (
        cmc.infected[k]-cmc.infected[j])/max(1, cmc.infected[j])*100
    cmc.infection_doubling_time[k] = 70/cmc.infection_growth_rate[k]


# %%
