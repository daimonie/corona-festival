import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import theano.tensor as tt
import pymc3 as pm
from datetime import datetime
from corona_festival.utils import setup_log, savefig, startfig, stop
from corona_festival.model import beta_normal_model

filenames = {
    "raw": 'data/raw_data.csv',
    "explore": 'figures/explore_{situation}.png',
    "burned_trace": 'figures/burned_trace_{situation}.png',
    "burned_trace_csv": 'figures/burned_trace_{situation}.csv'
}


if __name__ == "__main__":
    setup_log(name='corona')
    logging.info("Logging has been setup.")


    sns.set_theme(color_codes=True)

    df_festivals = pd.read_csv(
            filenames['raw'],
            sep=',',
            header=1
        )

    logging.info(df_festivals.head())
    
    for situation in df_festivals.situation.unique():
        startfig()
        sns.regplot(data=df_festivals[df_festivals.situation==situation], x='visitors', y='infected')
        savefig(filenames['explore'].format(
            situation=situation
        ))

        # This information was given to us.
        false_negative = 0.20
        # these two numbers were extracted 11 June 2021
        real_num_corona = 61000
        real_population_number = 17200000

        # Model says p * N * false_negative come in infected. They each infect R people and so we end up with
        # p N fn R people afterwards.
        # p sounds like the parameter of a binomial, let's make it a beta distribution?

        burned_trace = beta_normal_model(
            data=df_festivals,
            situation=situation,
            hyper_p_mu=real_num_corona/real_population_number,
            hyper_p_sigma=2*real_num_corona/real_population_number,
            hyper_r_mu=3,
            hyper_r_sigma=.2,
            false_negative=false_negative,
            sample=2000,
            cores=6,
            chains=4
        )

        startfig()
        plt.title("Burn trace.")
        pm.plot_trace(burned_trace)
        savefig(filenames['burned_trace'].format(
            situation=situation
        )) 

        pm.trace_to_dataframe(burned_trace).to_csv(filenames['burned_trace_csv'].format(
            situation=situation
        ))