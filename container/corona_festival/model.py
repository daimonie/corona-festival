import logging
import pymc3 as pm
import pandas as pd
import numpy as np
import theano.tensor as tt

def beta_normal_model(
        data=None,
        situation='cookies',
        hyper_p_mu=0.01,
        hyper_p_sigma=0.03,
        hyper_r_mu=3,
        hyper_r_sigma=10,
        false_negative=.1,
        sample=1000,
        chains=4,
        cores=4,
        tune=1000,
        nuts=False
    ):
    assert data is not None

    logging.info(f"Bayesian stats analysis for {situation} festival data.")
    df_data = data[data.situation == situation]

    data_visitors = df_data.visitors.values
    data_infected = df_data.infected.values

    normal_positive = pm.Bound(
        pm.Normal,
        lower=0
    )
    with pm.Model() as model:
        r = normal_positive(
            'r',
            mu = hyper_r_mu,
            sigma = hyper_r_sigma
        )
        p = hyper_p_mu

        lam = p * r * false_negative 
        lam_print = tt.printing.Print("lam")(lam)

        observed = pm.Poisson(
            "observed",
            mu=lam* data_visitors,
            #sigma=50,
            observed=data_infected
        )

        start = pm.find_MAP()
        if nuts:
            step = pm.NUTS()
        else:
            step = pm.Metropolis()
        trace = pm.sample(
            sample,
            step=step,
            start=start,
            chains=chains,
            cores=cores,
            tune=tune,
            return_inferencedata=False
        )
        burned_trace = trace[int(sample*4/5):]

    return burned_trace