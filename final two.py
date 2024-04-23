import pandas as pd
import matplotlib.pyplot as plt

#creating the dataframe
df = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')
#check the data set
desc = df.describe()
shp = df.shape
dupli = df.duplicated().sum()
memo =df.memory_usage()
#clearing the data
missing= df.isna().sum()
#we don't drop the duplicates or nan cause the missing data are not relative to the request
#df=df.drop_duplicates()
#df = df.dropna(axis = 0)


#setting the max rows to 500 so that will be easier to read
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns',4)

#change the form of the date so that it is easier to use
df['date']=pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

#keeping only the relative columns
df2=df[['store_number','store_name','sale_dollars','year']]

#keeping only the relative years
years = df2.loc[(df2.year>=2016)&(df2.year<=2019),['store_number','store_name','sale_dollars']]

#grouping the data by store so that we have the accurate total, plus summing the sales. then we reset the index
group= years.groupby(['store_number','store_name'])['sale_dollars'].sum().reset_index()

# we are using the sum to find the total dollars that the sales made
totalDol = group['sale_dollars'].sum()

#we create a new column that represents the percent of the sales per store
group['%Sales']=(group['sale_dollars']/totalDol)*100

#droping the store number column, cause we dont need it any more
group= group.drop('store_number',
                 axis=1)

#using the sort values method to change the order
group=group.sort_values('%Sales',ascending=True)

#using the tail method to get the last 15 stores
group = group.tail(16)

#creating the plot

#creating variables of the columns
store_name=group['store_name']
Sales= round(group['%Sales'],2)
sale_dollars=group['sale_dollars']

#creating the figure size to fit the hole chart
plt.figure(figsize=(18,8))

#creating the barHorizontal chart
barh =plt.barh(store_name,Sales)

#iter throught the bar chart for each bar to annote each one
for bar in barh:
    x_value = bar.get_width()
    y_value = bar.get_y() + bar.get_height() / 2
    space =25
    #creating a variable to be used as the label for each bar
    annote='{}'.format(x_value)
    #creating the annotation inside the for loop, so we can iter for each number to be assigned at a bar
    plt.annotate(
        annote, (x_value, y_value)
        , textcoords='offset points'
        , xytext=(space, 0), va='center'
        , ha='center'
        , bbox=dict(boxstyle='ellipse', fc='lightblue', ec='white'))

#creating title, label for the bottom and using the tight layout so that it fits nice inside the figure
plt.title('%Sales by store')
plt.xlabel('%Sales')
plt.tight_layout()
plt.show()
