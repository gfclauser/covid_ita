"""Procude tutti i grafici su COVID-19 in Italia."""

# Set working directory to home
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.utils import (
    directory_cleanup,
    subset_to_region,
    plt_infection_evolution,
    manipulate_df,
    plt_growth_rate,
    plt_infection_peak,
    plt_intensive_care,
    plt_new_cases,
    plt_ic_variation,
)
from src.metadata import region_dict

os.chdir("/Users/GiorgioClauser 1/Projects/covid_ita")

# Import region data
df_all = pd.read_csv(
    "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"
)

# Import national data
df_ita = pd.read_csv(
    "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
)

# Loop over regioni
for regione in list(region_dict.keys()):

    print(f"Working on {regione}")

    # Filtra per regione
    df = subset_to_region(df_all, regione)

    # Manipola dataframe
    df = manipulate_df(df)

    # Remove old plots and create directory for new ones
    dir_path = directory_cleanup(regione)

    # Generate plots
    plt_infection_evolution(df, regione, 14, dir_path)
    plt_growth_rate(df, regione, 14, dir_path)
    plt_infection_peak(df, regione, 14, dir_path, region_dict[regione])
    plt_intensive_care(df, regione, 14, dir_path)
    plt_new_cases(df, regione, 14, dir_path, region_dict[regione])
    # plt_ic_variation(
    #     df,
    #     regione,
    #     14,
    #     dir_path,
    # )
    plt.close("all")

# Do Italy

print("Working on Italy")

# Manipola dataframe
df = manipulate_df(df_ita)

dir_path = directory_cleanup("Italia")

# Generate plots
plt_infection_evolution(df, "Italia", 14, dir_path)
plt_growth_rate(df, "Italia", 14, dir_path)
plt_infection_peak(df, "Italia", 14, dir_path, 60244639)
plt_intensive_care(df, "Italia", 14, dir_path)
plt_new_cases(df, "Italia", 14, dir_path, 60244639)
# plt_ic_variation(df, "Italia", 14, dir_path)
plt.close("all")
