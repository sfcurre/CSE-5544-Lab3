import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from vega_datasets import data

counties = alt.topo_feature(data.us_10m.url, 'counties')
source = data.unemployment.url

gd = pd.read_csv('gender.csv')
conversion = pd.read_csv('countries_codes_and_coordinates.csv')
conversion = conversion.applymap(lambda x: x.strip().strip('"'))
conversion = conversion.drop_duplicates('Alpha-3 code')
conversion.index = conversion['Alpha-3 code']
variables = [
    'Country Name',
    'Country Code',
    'Year',
    'average_value_Adolescent fertility rate (births per 1,000 women ages 15-19)',
    'average_value_Fertility rate, total (births per woman)',
    'average_value_Life expectancy at birth, female (years)',
    'average_value_Life expectancy at birth, male (years)',
    'average_value_Mortality rate, adult, female (per 1,000 female adults)',
    'average_value_Mortality rate, adult, male (per 1,000 male adults)',
    'average_value_Survival to age 65, female (% of cohort)',
    'average_value_Survival to age 65, male (% of cohort)'
]
rename = [
    'Country Name',
    'Country Code',
    'Year',
    'Adolescent fertility rate',
    'Fertility rate total',
    'Life expectancy at birth female',
    'Life expectancy at birth male',
    'Mortality rate adult female',
    'Mortality rate adult male',
    'Survival to age 65 female',
    'Survival to age 65 male'
]
gd = gd[variables].dropna()
gd = gd[gd['Country Code'].isin(conversion.index)]
gd.columns = rename
gd['Life expectancy at birth ratio female to male'] = gd['Life expectancy at birth female'] / gd['Life expectancy at birth male']
gd['Mortality rate adult ratio female to male'] = gd['Mortality rate adult female'] / gd['Mortality rate adult male']
gd['Survival to age 65 ratio female to male'] = gd['Survival to age 65 female'] / gd['Survival to age 65 male']
gd['id'] = [int(conversion['Numeric code'].loc[c]) for c in gd['Country Code']]
rename += ['Life expectancy at birth ratio female to male',
           'Mortality rate adult ratio female to male',
           'Survival to age 65 ratio female to male']

countries = alt.topo_feature(data.world_110m.url, 'countries')

st.title('CSE 5544 Lab 3 - Ethics')
"""Sean Current"""

st.header("Heatmaps")

"""
Each heatmap below is identical save for the color scheme used. The first heatmap uses the 'rainbow' scheme,
while the second heatmap uses the 'darkgold' scheme, which is an Altair equivalent of the black body colormap.

Each color map plots a select variable (options listed). Data is taken from the Gender Equality Indicators dataset,
and only attributes with a low degree of missingness are considered. Additonally, ratio variables are used to better
reflect the differences between female and male sexes for many of the variables considered. All ratios are presented
as female/male. Years for the heatmaps are sorted numerically, while countries are sorted according to the mean of
their values for the variable under consideration.
"""

st.subheader("Choose Variable:")
var = st.selectbox("variable", rename[3:], key='var')
gd = gd.sort_values(by=['Year', var])

od = {}
for country in set(gd['Country Name']):
    cm = gd[gd['Country Name'] == country][var].mean()
    od[country] = 1 / cm
gd['order'] = gd['Country Name'].map(od)

st.write(f"Heatmap of {var}")

hm = alt.Chart(gd).mark_rect().encode(
    y=alt.Y('Country Name:N', sort=alt.EncodingSortField(field='order', order='ascending')),
    x='Year:O',
    color=alt.Color(var+':Q', scale=alt.Scale(scheme='rainbow'))
).properties(
    width=1000,
    height=2000
)

st.altair_chart(hm, use_container_width=False)

hm = alt.Chart(gd).mark_rect().encode(
    y=alt.Y('Country Name:N', sort=alt.EncodingSortField(field='order', order='ascending')),
    x='Year:O',
    color=alt.Color(var+':Q', scale=alt.Scale(scheme='darkgold'))
).properties(
    width=1000,
    height=2000
)

st.altair_chart(hm, use_container_width=False)

"""
The two color schemes portray the numerical data in vastly different ways. The rainbow color scheme
warps the data visualization and makes it extremely difficult to compare higher and lower values of
the data. Because the color scheme is cyclic, there is little differentiation between high and low
values. In contrast, the darkgold color scheme makes it significantly easier to compare countries
and better understand how the values change temporally. Because the intensity of the color changes
with respect to the values of the variable under consideration, the darkgold color map better portrays
the data to the reader.
"""

st.header("Geographic Heatmap")

st.subheader("Choose Variable:")
varia = st.selectbox("variable", rename[3:], key='varia')

st.subheader("Choose Year:")
year = st.slider("year", 1960, 2019, 1990)
gd_ = gd[gd['Year'] == year]

colors = sorted(['rainbow', 'darkgold', 'darkred', 'inferno', 'viridis'])
st.subheader("Choose Color Scheme:")
scheme = st.selectbox("scheme", colors)

mp = alt.Chart(countries).mark_geoshape().transform_lookup(
    lookup='id',
    from_=alt.LookupData(gd_, key='id', fields=[varia]),
).encode(
    color=alt.Color(varia+':Q', scale=alt.Scale(scheme=scheme))
).project(
    'equirectangular'
).properties(
    width=800,
    height=400
)

st.altair_chart(mp, use_container_width=False)

"""
Unlike the prior visualizations, the geographic heatmap is unable to portray temporal
changes in the values of variables. However, spatial locality is much better conveyed. For
example, the higher adolescent fertility rate throughout much of Africa is significantly
better protrayed than in the prior heatmaps. Additionally, this visualization makes it easier
for the reader to understand regional correlations and significance, as well as connecting
the information better with the reader's prior knowledge of the world.
"""

st.header("Code")

"""
Code to produce the plots above is shown below.
"""

st.code("""
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

from vega_datasets import data

counties = alt.topo_feature(data.us_10m.url, 'counties')
source = data.unemployment.url

gd = pd.read_csv('gender.csv')
conversion = pd.read_csv('countries_codes_and_coordinates.csv')
conversion = conversion.applymap(lambda x: x.strip().strip('"'))
conversion = conversion.drop_duplicates('Alpha-3 code')
conversion.index = conversion['Alpha-3 code']
variables = [
    'Country Name',
    'Country Code',
    'Year',
    'average_value_Adolescent fertility rate (births per 1,000 women ages 15-19)',
    'average_value_Fertility rate, total (births per woman)',
    'average_value_Life expectancy at birth, female (years)',
    'average_value_Life expectancy at birth, male (years)',
    'average_value_Mortality rate, adult, female (per 1,000 female adults)',
    'average_value_Mortality rate, adult, male (per 1,000 male adults)',
    'average_value_Survival to age 65, female (% of cohort)',
    'average_value_Survival to age 65, male (% of cohort)'
]
rename = [
    'Country Name',
    'Country Code',
    'Year',
    'Adolescent fertility rate',
    'Fertility rate total',
    'Life expectancy at birth female',
    'Life expectancy at birth male',
    'Mortality rate adult female',
    'Mortality rate adult male',
    'Survival to age 65 female',
    'Survival to age 65 male'
]
gd = gd[variables].dropna()
gd = gd[gd['Country Code'].isin(conversion.index)]
gd.columns = rename
gd['Life expectancy at birth ratio female to male'] = gd['Life expectancy at birth female'] / gd['Life expectancy at birth male']
gd['Mortality rate adult ratio female to male'] = gd['Mortality rate adult female'] / gd['Mortality rate adult male']
gd['Survival to age 65 ratio female to male'] = gd['Survival to age 65 female'] / gd['Survival to age 65 male']
gd['id'] = [int(conversion['Numeric code'].loc[c]) for c in gd['Country Code']]
rename += ['Life expectancy at birth ratio female to male',
           'Mortality rate adult ratio female to male',
           'Survival to age 65 ratio female to male']

countries = alt.topo_feature(data.world_110m.url, 'countries')

st.title('CSE 5544 Lab 3 - Ethics')

st.header("Heatmaps")

st.subheader("Choose Variable:")
var = st.selectbox("variable", rename[3:], key='var')
gd = gd.sort_values(by=['Year', var])

od = {}
for country in set(gd['Country Name']):
    cm = gd[gd['Country Name'] == country][var].mean()
    od[country] = 1 / cm
gd['order'] = gd['Country Name'].map(od)

st.write(f"Heatmap of {var}")

hm = alt.Chart(gd).mark_rect().encode(
    y=alt.Y('Country Name:N', sort=alt.EncodingSortField(field='order', order='ascending')),
    x='Year:O',
    color=alt.Color(var+':Q', scale=alt.Scale(scheme='rainbow'))
).properties(
    width=1000,
    height=2000
)

st.altair_chart(hm, use_container_width=False)

hm = alt.Chart(gd).mark_rect().encode(
    y=alt.Y('Country Name:N', sort=alt.EncodingSortField(field='order', order='ascending')),
    x='Year:O',
    color=alt.Color(var+':Q', scale=alt.Scale(scheme='darkgold'))
).properties(
    width=1000,
    height=2000
)

st.altair_chart(hm, use_container_width=False)

st.header("Geographic Heatmap")

st.subheader("Choose Variable:")
varia = st.selectbox("variable", rename[3:], key='varia')

st.subheader("Choose Year:")
year = st.slider("year", 1960, 2019, 1990)
gd_ = gd[gd['Year'] == year]

colors = sorted(['rainbow', 'darkgold', 'darkred', 'inferno', 'viridis'])
st.subheader("Choose Color Scheme:")
scheme = st.selectbox("scheme", colors)

mp = alt.Chart(countries).mark_geoshape().transform_lookup(
    lookup='id',
    from_=alt.LookupData(gd_, key='id', fields=[varia]),
).encode(
    color=alt.Color(varia+':Q', scale=alt.Scale(scheme=scheme))
).project(
    'equirectangular'
).properties(
    width=800,
    height=400
)

st.altair_chart(mp, use_container_width=False)
""")