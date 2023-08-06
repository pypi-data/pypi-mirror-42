import pandas as pd
import numpy as np
from met_estimator.cutpoints import sasaki, nhanes, freedson
from met_estimator.METs import cr2_mets, c_mets, freedson_mets, sasaki_mets
from met_estimator.sojourn import sojourn_1x

df = pd.read_csv("stuff.csv")
fn_df = pd.DataFrame()
fn_df["sasaki_cut"] = sasaki(list(df["axis1"]))
fn_df["nhanes_cut"] = nhanes(list(df["axis1"]))
fn_df["freedson_cut"] = freedson(list(df["axis1"]))
fn_df["crouter2_mets"] = cr2_mets(list(df["axis1"]))
fn_df["c_mets"] = c_mets(list(df["axis1"]))
fn_df["freedson_mets"] = freedson_mets(list(df["axis1"]))
fn_df["sasaki_mets"] = sasaki_mets(list(df["vectormagnitude"]))
sojourn_1x(list(df["axis1"]))
fn_df.to_csv("output.csv")

