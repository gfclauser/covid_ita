"""Funzioni per processare i dati."""

import shutil
import os
import matplotlib.pyplot as plt
import seaborn as sns


def plot_time_lines(ax, zz):
    """Plot vertical time lines."""
    for day in ["2020-03-09"]:
        ax.axvline(day, ls="--", color="blue", lw=1.5)
        plt.text(day, zz, "LOCKDOWN", fontsize=14, rotation=45)
    for day in ["2020-05-04"]:
        ax.axvline(day, ls="--", color="blue", lw=1.5)
        plt.text(day, zz, "PHASE 2", fontsize=14, rotation=45)
    for day in ["2020-06-03"]:
        ax.axvline(day, ls="--", color="blue", lw=1.5)
        plt.text(day, zz, "PHASE 3", fontsize=14, rotation=45)
    for day in ["2020-11-06"]:
        ax.axvline(day, ls="--", color="blue", lw=1.5)
        plt.text(day, zz, "LOCKDOWN", fontsize=14, rotation=45)


def directory_cleanup(region):
    """Remove old plots and create directory for new ones."""
    dir_path = f"/Users/GiorgioClauser 1/Documents/covid_plt/{region}"
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    return dir_path


def subset_to_region(df, region):
    """Filtra il dataset per la regione specifica."""
    fnl = df.copy()
    fnl = fnl.loc[fnl["denominazione_regione"] == f"{region}"].copy()
    return fnl


def manipulate_df(df):
    """Manipola il dataframe fornito dalla protezione civile."""
    fnl = df.copy()
    fnl["prcn_tamponi_positivi_overall"] = fnl["totale_casi"] / fnl["tamponi"]
    fnl["prcn_tamponi_positivi_daily"] = fnl["variazione_totale_positivi"] / (
        fnl["tamponi"] - fnl["tamponi"].shift(1)
    )
    fnl["reference_day"] = fnl.data.apply(lambda x: x[0:10])
    # fnl["nuovi_positivi"] = fnl["totale_positivi"] - fnl["totale_positivi"].shift(1)
    fnl["growth_rate"] = fnl["totale_positivi"] / fnl["totale_positivi"].shift(1)
    fnl["ic_variation"] = fnl["terapia_intensiva"] / fnl["terapia_intensiva"].shift(1)
    fnl.reset_index(inplace=True)
    return fnl


def plt_infection_evolution(df_input, region, n_label, dir_path):
    """Plot della evoluzione della infezione."""
    # Generate plot
    df = df_input.copy()
    plt.figure(figsize=(20, 12))
    ax = sns.lineplot(x="reference_day", y="totale_casi", data=df)
    plt.fill_between(
        x="reference_day", y1="totale_casi", y2=0, data=df, color="blue", alpha=0.1
    )
    plt.grid(color="grey", linestyle="--", linewidth=0.5, which="both")
    plt.ylabel("Total infected", fontsize=18)
    plt.xlabel("")
    plt.title(f"COVID19 - Infection evolution in {region}", fontsize=26)
    ax.tick_params(axis="both", which="major", labelsize=16)
    plt.xticks(rotation=45)
    plt.text(
        df.reference_day[len(df) - 1],
        df.totale_casi[len(df) - 1],
        df.totale_casi[len(df) - 1],
        fontsize=14,
    )
    plot_time_lines(ax, 0.3)
    ax.set_xticks(ax.get_xticks()[::n_label])
    plt.savefig(f"{dir_path}/infection_evolution_{region}.png")
    # plt.show()


def plt_growth_rate(df_input, region, n_label, dir_path):
    """Plot del growth rate."""

    df = df_input.copy()
    # Generate plot
    df_gr = df[["reference_day", "growth_rate"]].dropna().copy()
    df_gr["growth_rate"] = df_gr.growth_rate.rolling(window=4).mean()
    df_gr.dropna(inplace=True)
    df_gr = df[["reference_day", "growth_rate"]].dropna().copy()
    plt.figure(figsize=(20, 12))
    ax = sns.lineplot(x="reference_day", y="growth_rate", data=df_gr, lw=3)
    plt.grid(color="grey", linestyle="--", linewidth=0.5, which="both")
    plt.ylabel("Growth rate", fontsize=18)
    plt.xlabel("")
    plt.title(f"COVID19 - Growth rate evolution in {region}", fontsize=26)
    ax.tick_params(axis="both", which="major", labelsize=16)
    plt.xticks(rotation=45)
    # plt.ylim(bottom=-2, top=5)
    ax.axhline(1, ls="--", color="green", lw=1.5)
    plt.text(
        df_gr.reference_day[len(df_gr)],
        df_gr.growth_rate[len(df_gr)] + 0.01,
        round(df_gr.growth_rate[len(df_gr)], 2),
        fontsize=14,
    )
    plot_time_lines(ax, 0.84)
    ax.set_xticks(ax.get_xticks()[::n_label])
    plt.savefig(f"{dir_path}/growth_rate_{region}.png")
    # plt.show()


def plt_infection_peak(df_input, region, n_label, dir_path, tot_ab):
    """Grafico del numero totale di infetti attivi."""

    df = df_input.copy()
    ratio = df.totale_positivi[len(df) - 1] / (tot_ab / 100000)
    plt.figure(figsize=(20, 12))
    ax = sns.lineplot(
        x="reference_day", y="totale_positivi", data=df, lw=3, color="orange"
    )
    plt.grid(color="grey", linestyle="--", linewidth=0.5, which="both")
    plt.fill_between(
        x="reference_day",
        y1="totale_positivi",
        y2=0,
        data=df,
        color="orange",
        alpha=0.1,
    )
    plt.ylabel("Number of infected", fontsize=18)
    plt.xlabel("")
    plt.title(
        f"COVID19 - In {region} today {round(ratio,1)} active cases per 100K inhabitants.",
        fontsize=26,
    )
    ax.tick_params(axis="both", which="major", labelsize=16)
    plt.xticks(rotation=45)
    plt.text(
        df.reference_day[len(df) - 1],
        df.totale_positivi[len(df) - 1] + 144,
        df.totale_positivi[len(df) - 1],
        fontsize=14,
    )
    plot_time_lines(ax, 0.3)
    ax.set_xticks(ax.get_xticks()[::n_label])
    plt.savefig(f"{dir_path}/peak_evolution_{region}.png")
    # plt.show()


def plt_intensive_care(df_input, region, n_label, dir_path):
    """Numero di letti in terapia intensiva occupati."""

    # Generate plot
    df = df_input.copy()
    plt.figure(figsize=(20, 12))
    ax = sns.lineplot(x="reference_day", y="terapia_intensiva", data=df)
    plt.fill_between(
        x="reference_day",
        y1="terapia_intensiva",
        y2=0,
        data=df,
        color="blue",
        alpha=0.1,
    )
    plt.grid(color="grey", linestyle="--", linewidth=0.5, which="both")
    plt.ylabel("People in intensive care", fontsize=18)
    plt.xlabel("")
    plt.title(f"COVID19 - Intensive care in {region}", fontsize=26)
    ax.tick_params(axis="both", which="major", labelsize=16)
    plt.xticks(rotation=45)
    plt.text(
        df.reference_day[len(df) - 1],
        df.terapia_intensiva[len(df) - 1] + 21,
        df.terapia_intensiva[len(df) - 1],
        fontsize=14,
    )
    plot_time_lines(ax, 0.3)
    ax.set_xticks(ax.get_xticks()[::n_label])
    plt.savefig(f"{dir_path}/intensive_care_{region}.png")
    # plt.show()


def plt_new_cases(df_input, region, n_label, dir_path, tot_ab):
    """Grafico del numero di nuovi casi."""

    df = df_input.copy()
    ratio = df.nuovi_positivi[len(df) - 1] / (tot_ab / 100000)
    plt.figure(figsize=(20, 12))
    ax = sns.lineplot(
        x="reference_day", y="nuovi_positivi", data=df, lw=3, color="orange"
    )
    plt.grid(color="grey", linestyle="--", linewidth=0.5, which="both")
    plt.fill_between(
        x="reference_day",
        y1="nuovi_positivi",
        y2=0,
        data=df,
        color="orange",
        alpha=0.1,
    )
    plt.ylabel("Number of new cases", fontsize=18)
    plt.xlabel("")
    plt.title(
        f"COVID19 - In {region} today {round(ratio,2)} new cases per 100K inhabitants.",
        fontsize=26,
    )
    ax.tick_params(axis="both", which="major", labelsize=16)
    plt.xticks(rotation=45)
    plt.text(
        df.reference_day[len(df) - 1],
        df.nuovi_positivi[len(df) - 1] + 13,
        df.nuovi_positivi[len(df) - 1],
        fontsize=14,
    )
    plot_time_lines(ax, 0.3)
    ax.set_xticks(ax.get_xticks()[::n_label])
    plt.savefig(f"{dir_path}/new_cases_{region}.png")


def plt_ic_variation(df_input, region, n_label, dir_path):
    """Plot della variazione giornaliera terapia intensiva."""

    df = df_input.copy()
    # Generate plot
    df_gr = df[["reference_day", "ic_variation"]].dropna().copy()
    plt.figure(figsize=(20, 12))
    ax = sns.lineplot(x="reference_day", y="ic_variation", data=df_gr, lw=3)
    plt.grid(color="grey", linestyle="--", linewidth=0.5, which="both")
    plt.ylabel("IC variation", fontsize=18)
    plt.xlabel("")
    plt.title(f"COVID19 - Intensive care variation in {region}", fontsize=26)
    ax.tick_params(axis="both", which="major", labelsize=16)
    plt.xticks(rotation=45)
    # plt.ylim(bottom=-2, top=5)
    ax.axhline(1, ls="--", color="green", lw=1.5)
    plt.text(
        df_gr.reference_day[len(df_gr)],
        df_gr.ic_variation[len(df_gr)] + 0.01,
        round(df_gr.ic_variation[len(df_gr)], 2),
        fontsize=14,
    )
    plot_time_lines(ax, 0.84)
    ax.set_xticks(ax.get_xticks()[::n_label])
    plt.savefig(f"{dir_path}/ic_variation_{region}.png")
    # plt.show()
