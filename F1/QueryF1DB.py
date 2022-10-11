import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

def table_to_df(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM " + table_name)
    cols = [column[0] for column in data.description]
    df = pd.DataFrame.from_records(data.fetchall(), columns = cols)
    conn.close()
    return df

def circuits_per_country(db_name = "F1Results.db", table_name = "circuits"):
    data = table_to_df(db_name, table_name)
    d = data.groupby(data.country, as_index = False).count()
    d = d[["country", "circuitId"]]
    d = d.rename(columns = {"circuitId" : "number of circuits"})
    return d

def races_per_year(db_name = "F1Results.db", table_name = "races"):
    data = table_to_df(db_name, table_name)
    d = data.groupby("year", as_index = False).count()
    d = d[["year", "raceId"]]
    d = d.rename(columns={"raceId": "number of races"})
    return d

def constructors_per_nationality(db_name = "F1Results.db", table_name = "constructors"):
    data = table_to_df(db_name, table_name)
    d = data.groupby("nationality", as_index = False).count()
    d = d[["nationality", "constructorId"]]
    d = d.rename(columns={"constructorId": "number of constructors"})
    return d

def drivers_per_nationality(db_name = "F1Results.db", table_name = "drivers"):
    data = table_to_df(db_name, table_name)
    d = data.groupby("nationality", as_index = False).count()
    d = d[["nationality", "driverId"]]
    d = d.rename(columns={"driverId": "number of drivers"})
    return d

def lapTimes_trend(db_name = "F1Results.db"):
    data = table_to_df(db_name, "lap_times")
    data2 = table_to_df(db_name, "races")
    result = pd.merge(data,data2,on="raceId")
    cid = result.circuitId.unique()
    dr = result.groupby("circuitId", as_index=False)["milliseconds"].agg(min)
    dr = pd.merge(dr,data2,on="circuitId")
    dr = dr[["date", "milliseconds"]]
    dr["date"] = pd.to_datetime(dr["date"])
    dr.index = dr.date
    dr = dr.drop("date", axis=1)
    start_date = datetime(1995,1,1)
    end_date = datetime(2022,1,1)
    return dr[(start_date <= dr.index) & (dr.index <= end_date)]

def pitStops_trend(db_name = "F1Results.db"):
    data = table_to_df(db_name, "pit_stops")
    data2 = table_to_df(db_name, "constructor_results")
    data4 = table_to_df(db_name, "races")
    result2 = pd.merge(data,data2, on="raceId")
    result2 = pd.merge(result2, data4, on="raceId")
    result2 = result2[result2.circuitId == 7]
    dr2 = result2.groupby("constructorId", as_index=False)[["date", "milliseconds"]]
    dr2 = dr2.apply(lambda x: x)
    dr2["date"] = pd.to_datetime(dr2["date"])
    dr2.index = dr2.date
    dr2 = dr2.drop("date", axis=1)
    start_date = datetime(1995,1,1)
    end_date = datetime(2022,1,1)
    return dr2[(start_date <= dr2.index) & (dr2.index <= end_date)]

def points_per_constructor(db_name = "F1Results.db"):
    data = table_to_df(db_name, "constructor_results")
    data2 = table_to_df(db_name, "constructors")
    d = data.groupby("constructorId", as_index=False).count()
    d = d.apply(lambda x: x)
    d = pd.merge(data2, d, on="constructorId")
    d = d[["points", "constructorId", "name"]]
    d_a = d.loc[(d["constructorId"] > 0) & (d["constructorId"] <= 72)]
    d_b = d.loc[(d["constructorId"] > 72) & (d["constructorId"] <= 134)]
    d_c = d.loc[(d["constructorId"] > 134) & (d["constructorId"] <= 214)]
    return d_a, d_b, d_c

def races_per_constructor(db_name = "F1Results.db"):
    data = table_to_df(db_name, "constructor_standings")
    data2 = table_to_df(db_name, "constructors")
    d = data.groupby("constructorId", as_index=False).count()
    d = d.apply(lambda x: x)
    d = pd.merge(data2, d, on="constructorId")
    d = d[["raceId", "constructorId", "name"]]
    d = d.rename(columns={"raceId": "number of races"})
    d_a = d.loc[(d["constructorId"] > 0) & (d["constructorId"] <= 72)]
    d_b = d.loc[(d["constructorId"] > 72) & (d["constructorId"] <= 134)]
    d_c = d.loc[(d["constructorId"] > 134) & (d["constructorId"] <= 214)]
    return d_a, d_b, d_c