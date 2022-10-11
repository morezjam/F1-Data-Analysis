import pandas as pd
import json
import numpy as np
import sqlite3
def establish_database(db_name = "F1Results.db"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS constructors")
    conn.commit()
    cur.execute("""CREATE TABLE constructors
    (constructorId  INT(3) PRIMARY KEY NOT NULL,constructorRef VARCHAR(30) unique not null,
    name VARCHAR(20) not null,
    nationality VARCHAR(20) not null,
    url VARCHAR(50) not null);""")
    conn.commit()
    
    cur.execute("DROP TABLE IF EXISTS drivers")
    conn.commit()
    cur.execute("""CREATE TABLE drivers
    (driverId  INT(5) PRIMARY KEY NOT NULL, driverRef VARCHAR(30) not null,
    number INT(10) not null,
    code VARCHAR(10) not null,
    forename VARCHAR(20) not null,
    surname VARCHAR(20) not null,
    dob DATE not null,
    nationality VARCHAR(20) not null,
    url VARCHAR(50) not null);""")
    conn.commit()
    
    cur.execute("DROP TABLE IF EXISTS circuits")
    conn.commit()
    cur.execute("""CREATE TABLE circuits
    (circuitId  INT(5) PRIMARY KEY NOT NULL, driverId INT(5) not null,
    stop INT(5) not null,
    lap INT(5) not null,
    time TIME not null,
    duration DECIMAL(2,3),
    milliseconds INT(8) not null);""")
    conn.commit()
    
    cur.execute("DROP TABLE IF EXISTS races")
    conn.commit()
    cur.execute("""CREATE TABLE races
    (raceId  INT(5) PRIMARY KEY NOT NULL, circuitRef VARCHAR(20) not null,
    name VARCHAR(20) not null,
    location VARCHAR(30) not null,
    country VARCHAR(20) not null,
    lat DECIMAL(3,5) not null,
    lng DECIMAL(3,5) not null,
    alt INT(4) not null,
    url VARCHAR(50) not null);""")
    conn.commit()
    
    cur.execute("DROP TABLE IF EXISTS pit_stops")
    conn.commit()
    cur.execute("""CREATE TABLE pit_stops
    (raceId  INT(5) PRIMARY KEY NOT NULL, driverId INT(5) not null,
    stop INT(5) not null,
    lap INT(5) not null,
    time TIME not null,
    duration DECIMAL(2,3),
    milliseconds INT(8) not null,
    FOREIGN KEY(driverId) REFERENCES drivers(driverId));""")
    conn.commit()
    
    cur.execute("DROP TABLE IF EXISTS lap_times")
    conn.commit()
    cur.execute("""CREATE TABLE lap_times
    (raceId  INT(5) PRIMARY KEY NOT NULL, driverId INT(5) not null,
    lap INT(5) not null,
    position INT(5) not null,
    time TIME not null,
    milliseconds INT(8) not null,
    FOREIGN KEY(raceId) REFERENCES races(raceId));""")
    conn.commit()
    
    cur.execute("DROP TABLE IF EXISTS constructor_standings")
    conn.commit()
    cur.execute("""CREATE TABLE constructor_standings
    (constructorStandingsId INT(5) PRIMARY KEY NOT NULL, raceId INT(5) not null,
    constructorId INT(5) not null,
    points INT(5) not null,
    position INT(5) not null,
    positionText VARCHAR(5) not null,
    wins INT(5) not null);""")
    conn.commit()
    
    cur.execute("DROP TABLE IF EXISTS constructor_results")
    conn.commit()
    cur.execute("""CREATE TABLE constructor_results
    (constructorResultsId INT(5) PRIMARY KEY NOT NULL, raceId INT(5) not null,
    constructorId INT(5) not null,
    points INT(5) not null, status VARCHAR(5) not null);""")
    conn.commit()
    
    conn.close()
    print("Database and its tables were built!\n")

def populate_table(db_name, table_name, path = "Dataset/"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    df = pd.read_csv(path + table_name + ".csv")
    df.to_sql(table_name, conn, if_exists = "replace", index = False)
    conn.close()
    print(table_name + " were succesfully populated.\n")

def save_table_as_JSON(db_name, table_name, file_name, path = "JSON Files/"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    
    rows = cur.execute("SELECT * from " + table_name).fetchall()
    conn.commit()
    conn.close()
    with open(path + file_name + ".json", 'w') as outfile:
        json.dump(rows, outfile)
    print(file_name + ".json " + "in the given path " + "was succesfully saved.")

def list_tables(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    rows = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.commit()
    conn.close()
    l = []
    for r in rows:
        l.append(r[0])
    return l