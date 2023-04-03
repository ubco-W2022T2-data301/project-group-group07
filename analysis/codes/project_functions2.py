import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_process(path, dfname):

    df1 = (
    pd.read_csv(path)
    .drop(columns=['work_year', 'employment_type', 'job_title', 'employee_residence', 'company_size', 'experience_level','salary_currency', 'salary'])
    .loc[lambda df: df["company_region"] == dfname]
      )

    df2 = (
          df1
          .assign(remote_ratio = lambda x : x['remote_ratio'].replace(0, "Not remote").replace(50, "Partially remote").replace(100, "Fully remote"))
          .groupby("remote_ratio")
          .mean()
          .reset_index()
      )

    return df2 