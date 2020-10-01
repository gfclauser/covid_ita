"""Procude tutti i grafici su COVID-19 in Italia."""

# Set working directory to home
import os
import pandas as pd
from src.utils import (
    directory_cleanup,
    subset_to_region,
    plt_infection_evolution,
    manipulate_df,
    plt_growth_rate,
    plt_infection_peak,
)

os.chdir("/Users/giorgioclauser/Projects/covid_ita/")

# Import national data
df = pd.read_csv(
    "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
)

# Decidi la regione
regione = "Lombardia"

# Filtra per regione
df = subset_to_region(df, regione)

# Manipola dataframe
df = manipulate_df(df)

# Remove old plots and create directory for new ones
dir_path = directory_cleanup(regione)

# Generate plots
plt_infection_evolution(df, regione, 14, dir_path)
plt_growth_rate(df, regione, 14, dir_path)
plt_infection_peak(df, regione, 14, dir_path)
