# figuring out how to do stuff with the help of chat :|
import requests, pandas as pd, numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CENSUS_API_KEY")

request = requests.get(f"https://api.census.gov/data/2024/acs/acs5?get=GEO_ID,B01003_001E,B19013_001E,B17001_001E,B17001_002E&for=tract:*&in=state:06%20county:053&key={api_key}")

# print(request.json())
data = request.json()

df = pd.DataFrame(data[1:], columns=data[0])

# rename B19013_001E to median_household_income
df = df.rename(columns={"B19013_001E" : "median_household_income",
                         "B17001_001E" : "poverty_status_population",
                           "B17001_002E" : "poverty_population",
                           "B01003_001E" : "total_population"})

# print(df.dtypes)

# change median_household_income to type int
df["median_household_income"] = df["median_household_income"].astype('int')
df["poverty_status_population"] = df["poverty_status_population"].astype('int')
df["poverty_population"] = df["poverty_population"].astype('int')
# print(df.describe(include="all"))

# we can see that error values are defaulting to -66666666, clean this data
df["median_household_income"] = df["median_household_income"].replace(-666666666, np.nan)
# print(df.dtypes)

# print(df.shape) -> (104, 5)
# print(df.dtypes)
# print(df.isna().sum()) -> 5 NaN in m.h.i.
# print(df.describe(include="all"))

df["poverty_rate(%)"] = df["poverty_population"] / df["poverty_status_population"] * 100

# print(df.head())
# print(df["poverty_status_population"].describe())
# print(df["poverty_population"].describe())
# print(df['poverty_rate(%)'].describe()) # this count is 3 less than the others. because division of 0

print(df.loc[
    df["poverty_status_population"] == 0,
    ["GEO_ID", "total_population", "poverty_status_population", "poverty_population"]
])

# url = (
#     "https://api.census.gov/data/2024/acs/acs5"
#     "?get=NAME,GEO_ID"
#     "&for=tract:990000"
#     "&in=state:06%20county:053"
#     f"&key={api_key}"
# )

# response = requests.get(url)
# print(response.json())
