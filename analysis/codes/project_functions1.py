import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_process_region(path, regionName):
  """
  Load the data from the given path and process the data based on the given region. After processing, it returns the dataframe of the count by each company size.
  Args:
    path (string): the path of the file to load the file.
    regionName (string): the name of the region to be proecessed.

  Returns:
    pandas.core.frame.DataFrame: the processed dataframe that includes the count by company size based on the region.
  """
  dfRegion = (
    pd.read_csv(path)
    .drop(columns=["work_year", "employment_type", "job_title", "salary", "salary_currency", "remote_ratio"])
    .loc[lambda df: df["company_region"] == regionName]
    .loc[:, ["company_size", "company_region"]]
    .groupby("company_size")
    .count()
    .reset_index()
    .rename(columns={"company_region":"count"})
    .assign(company_region = regionName)
    .assign(percentage=lambda x: (x["count"] / sum(x["count"]) * 100))
  )
  return dfRegion