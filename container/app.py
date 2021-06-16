import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import theano.tensor as tt
import pymc3 as pm
from datetime import datetime
from corona_festival.utils import setup_log, savefig, startfig, stop

filenames = {
    "raw": 'data/raw_data.csv'
}


if __name__ == "__main__":
    setup_log(name='corona')
    logging.info("Logging has been setup.")


    sns.set_theme(color_codes=True)

    df_raw = pd.read_csv(
            filenames['raw'],
            sep=',',
            header=2
        )

    logging.info(df_raw.head())