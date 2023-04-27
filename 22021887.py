# Importing libraries going to be used in this Assignment

import pandas as pd  # Pandas for data manipulation
import numpy as np  # NumPy for numerical computing
import matplotlib.pyplot as plt  # Matplotlib for data visualization
import matplotlib.gridspec as gridspec # Gridspec to create a infograph

# reading the dataset using the pandas 'pd.read_csv' method

try:
    df = pd.read_csv("dataset.csv")
except FileNotFoundError:
    print("Dataset file not found.")

# Checking the top 5 rows using head() method

df.head(5)

#Cleaning The DataSet by simply filling all the null values

df = df.fillna(0)

#Creating a new GDP_PER_CAPITA column which we use in the next steps

df['gdp_per_capita'] = np.where(df['population'] != 0, df['gdp'] / df['population'], 0)

# Creating a dataframe which contains only these columns which will help us

co2 = df[['year','country','co2']]

# Creating a list of Continents Because the dataset itself contain countries and continents as well
# List of continents to compare CO2 emissions, including "World" to compare overall emissions
# and "Antarctica" to represent uninhabited areas

continents = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']

# Seperating the country to be in the list of continents 
# this will help in Accurate measurement

# Only include data for continents because we want to compare CO2 emissions by continent
# and not by individual countries

continent_co2 = co2[co2['country'].isin(continents)]

# Check if all names in continents are valid

valid_continents = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']
invalid_continents = set(continents) - set(valid_continents)
if invalid_continents:
    print(f"Invalid continent names: {invalid_continents}")

#Grouping the countries with years because the only thing that is linked with these two is CO2. 
#That's why we group them by Co2 and calculate the mean which can help us in drawing outcomes easily.

mean_co2_by_country_and_year = (
    continent_co2.groupby(['country', 'year'])['co2']
    .mean()
    .reset_index()
    .sort_values(by='year')
    .reset_index(drop=True)
    .set_index('year')
)

# Displaying mean CO2 emissions by country and year with two decimal places
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# For drawing multiple i use different variables to store the each list-item extracted separately
co2_by_continent = {}
continents = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']

for c in continents:
    co2_by_continent[c] = mean_co2_by_country_and_year[mean_co2_by_country_and_year['country'] == c]

asia = co2_by_continent['Asia'].sum().get(1)
oceania = co2_by_continent['Oceania'].sum().get(1)
europe = co2_by_continent['Europe'].sum().get(1)
africa = co2_by_continent['Africa'].sum().get(1)
North_America = co2_by_continent['North America'].sum().get(1)
South_America = co2_by_continent['South America'].sum().get(1)

# Here i first set the figure size by passing a tuple in figsize which will set the width and height accordingy


fig = plt.figure(figsize = (10,6))

# Replace individual variables with dictionary values

for continent, data in co2_by_continent.items():
    data['co2'].plot()

plt.legend(co2_by_continent.keys())
plt.title("CO2 emission by continent")
plt.xlabel("Years")
plt.ylabel("CO2")
plt.grid()
plt.savefig('Muhammad_Adeel.png')
plt.show()

#Now doing the same thing to calculate the Co2 Emission Per Capita line graph
#which will further help us in understanding the dataset



co2percapita = df[['year','country','co2_per_capita']]
co2percapita_ok = co2percapita[co2percapita['country'].isin(continents)]
co2percapitagroup = co2percapita_ok.groupby(['country', 'year'])['co2_per_capita'].mean().reset_index().sort_values(by='year').reset_index(drop=True).set_index('year')

#Fixing the figure size

fig = plt.figure(figsize = (10,6))

#Plotting multiple line plots

continents = ['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica']
for continent in continents:
    cpc = co2percapitagroup[co2percapitagroup['country'] == continent]
    cpc['co2_per_capita'].plot()


#putting legends

plt.legend(['World', 'Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America', 'Antarctica'])
plt.suptitle("CO2 emission by continent")
plt.title("Muhammad Adeel-22021887", fontsize='small')
plt.xlabel("Years")
plt.ylabel("CO2 Per Capita")
plt.grid()
output_file = 'Muhammad_Adeel-22021887.png'
plt.savefig(output_file)
plt.show()

#now taking the only continents which have some values outcome. here we are not comparing the world because 
#we are going to create bar plots on the basis of different CO2 Emission sources.

continent = ['Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America']
# Filter out the rows in df that correspond to the continents we are interested in
df_continents = df[df['country'].isin(continent)]

#Extracting the CO2 Emission resources

if 'coal_co2' in df.columns and 'oil_co2' in df.columns and 'gas_co2' in df.columns:
    coal_co2 = df['coal_co2']
    oil_co2 = df['oil_co2']
    gas_co2 = df['gas_co2']
else:
    print("Error: 'coal_co2', 'oil_co2', or 'gas_co2' columns not found in DataFrame.")


# Group the data by country and sum the coal, oil, and gas emissions for each country
# This will give us the total amount of CO2 emitted by each country in the list of continents we are interested in

try:
    coal_co2_sum = df_continents.groupby('country')['coal_co2'].sum()
    oil_co2_sum = df_continents.groupby('country')['oil_co2'].sum()
    gas_co2_sum = df_continents.groupby('country')['gas_co2'].sum()
except KeyError:
    print("Error: 'country', 'coal_co2', 'oil_co2', or 'gas_co2' columns not found in DataFrame.")
    

#Creating simple bar chart to check values

coal_co2_sum.plot(kind='bar', x='country', y='coal_co2')

#Adding Title

plt.title("Amount of Coal_Co2 Released by Countries")

#Adding Labels

plt.xlabel("Countries")
plt.ylabel("Coal_Co2")

#Enabling Grid

plt.grid(True)

#Saving the output
plt.savefig("Coal_co2(22021887).png")
plt.show()

#Creating simple bar chart to check values


oil_co2_sum.plot(kind='bar', x='country', y='oil_co2')

#Adding Title

plt.title("Amount of Oil_Co2 Released by Countries")

#Adding Labels

plt.xlabel("Countries")
plt.ylabel("Oil_Co2")

#Enabling Grid

plt.grid()
plt.legend(['Oil CO2'])

#Saving the Figure

plt.savefig("Oil_co2(22021887).png")
plt.show()

#Creating simple bar chart to check values


gas_co2_sum.plot(kind='bar', x='country', y='gas_co2')

#Adding Title

plt.title("Amount of Gas_Co2 Released by Countries")

#Adding Labels

plt.xlabel("Countries")
plt.ylabel("Gas_Co2")

#Enabling Grid

plt.grid()

#Saving the Figure

plt.savefig("Gas_co2(22021887).png")
plt.show()



#Creating a infograph which together tell us a story about the Co2 Emission
#setting the figure size and applying a tight layout

fig = plt.figure(tight_layout=True,figsize=(20,12))

#creating a gridspec of 2 rows and 3 columns 

gs = gridspec.GridSpec(2, 3)

#Creating a Super Title to Describe Efficiently

plt.suptitle("Overall Co2 Emission Infograph --- Student-Id -- 22021887")

#creating first plot which is on first row and have two columns in total

ax = fig.add_subplot(gs[0, :2])

#Applying a for loop to generate multiple plots

for continent, data in co2_by_continent.items():
    ax.plot(data['co2'])

#setting the Labels,Title and Appropriate legends

ax.set_ylabel('Total Amount Co2')
ax.set_xlabel('Years')
ax.set_title("Co2 Emission by Contients")
plt.legend(co2_by_continent.keys(),fontsize=12)

#turning the grid on for better understanding of values

plt.grid(True)

#Creating Second subplot in our gridspec which is in first row and on the third column

ax = fig.add_subplot(gs[0,2])

#setting the bar width of each bar

bar_width = 0.3

#setting the value of each starting point to create a side by side bar plot on different values
x = ['Asia', 'Oceania', 'Europe', 'Africa', 'North America', 'South America']
r1 = np.arange(len(coal_co2_sum))
r = [x - bar_width for x in r1]
r2 = [x + bar_width for x in r1]


#Creating our Side-by-Side bar plots

ax.bar(r,coal_co2_sum,width=bar_width)
ax.bar(r1,oil_co2_sum,width=bar_width)
ax.bar(r2,gas_co2_sum,width=bar_width)

# Set the x-ticks to the country names
plt.xticks([r + bar_width/2 for r in range(len(coal_co2_sum))], x)

#Setting the Title of our second plot
ax.set_title("Seperate Emission by Contients")
plt.legend(x, fontsize=12)

#Setting the X-ticks and Activating the grid

ax.set_xticklabels(x,rotation=90, fontsize=10)
plt.grid(True)

#Creating the Third Subplot

ax = fig.add_subplot(gs[1,0])

ax.pie(coal_co2_sum,autopct='%0.1f%%',labels=x)
ax.set_title("Percentage of Coal_Co2 emission")

#Creating the Fourth Subplot

ax = fig.add_subplot(gs[1,1])

ax.pie(oil_co2_sum,autopct='%0.1f%%',labels=x)
ax.set_title("Percentage of Oil_Co2 emission")

#Creating the Fifth Subplot

ax = fig.add_subplot(gs[1,2])
ax.pie(gas_co2_sum,autopct='%0.1f%%',labels=x)
ax.set_title("Percentage of Gas_Co2 emission")

#Saving the Infograph

plt.savefig("Infograph(22021887).png")
plt.show()