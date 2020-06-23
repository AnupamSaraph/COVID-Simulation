# COVID India Model

COVID India model allows the simulation of different options before the Government of India to contain the COVID-19 pandemic. It provides a means to evaluate the impact of different options on new cases per day, total cases, total deaths and active cases.  


## Usage
The repository is being prepared for public use. You will be able to access the files here soon.

Soon you will be able to run the model online 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AnupamSaraph/COVID-Simulation/master)

You will be able to run the model offline 
>You will need to install the model code and requirements. These files have not yet been added to the repository, this file will change when they are.
>
> Use pip to install COVID-India-model:
>
>
>    `$ pip install COVID-India-model`
>
> Or use conda:
>
>   `$ conda install COVID-India-model`
>
>
You will then be able to also download and run the notebooks that call the model simulator and produce the outputs.

* [covid_india_reference_run.ipynb]()
* [covid_india_automatic_scenarios.ipynb]()

[covid_india_reference_run.ipynb]() compares the historical data with the simulation that includes the actions of the Government of India upto day 146. [covid_india_automatic_scenarios.ipynb]() enables you to simulate any interventions from any day for as many days as you like and generate.

If you set ```sim.Show = True``` in the notebook, the model outputs will be displayed in the interactive notebook. If you set ```sim.Save = True in``` the notebook, the results of the simulation will be saved in a folder with the version of the model (currently 5.6.01.2020).


