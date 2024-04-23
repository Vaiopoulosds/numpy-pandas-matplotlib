import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#setting the max rows to 500 so that will be easier to read
pd.set_option('display.max_rows', 500)
#importing the dataframe
df = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')
#check the data set
desc = df.describe()
shp = df.shape
dupli = df.duplicated().sum()
memo =df.memory_usage()
#clearing the data
missing= df.isna().sum()
#we don't drop the duplicates or nan cause the missing data are not relative to the request
# df=df.drop_duplicates()
# df = df.dropna(axis = 0)

#most popular item in each zipcode
#first we select the columns that we need
items = df[['zip_code','item_number','bottles_sold','store_number']]
#then we group by the columns so we can sum all the same bottles that are listed in the database
#this is to merge the duplicated zip codes and store numbers
store = items.groupby(['zip_code','store_number','item_number'])['bottles_sold'].sum().reset_index()
#droping an unnecessary column
store = store.drop('store_number', axis=1)
#using the idxmax to keep only the max number in the bottles sold column
idx = store.groupby(['zip_code'])['bottles_sold'].idxmax()
#turning the results from idxmax into data that we can print
#plus using the astype to change the floats at zip_code column
zips = store.loc[idx].astype({'zip_code':'int64'})

#create the scatter figure
fig, ax = plt.subplots()
scatter = plt.scatter(x=zips['zip_code'],
          y=zips['bottles_sold'],
          c=np.random.rand(len(zips['zip_code']),3))
#create the annotation
text_label= {}
for index, row in zips.iterrows():
    annotation =ax.annotate(text='',
                xy= (row['zip_code'], row['bottles_sold']),
                xytext = (15,15),
                textcoords= 'offset points',
                bbox = {'boxstyle': 'round', 'fc':'w'},
                arrowprops= {'arrowstyle':'->'}
                )
    text_label[f'{row["zip_code"]}']= f'{row["item_number"]}'
    annotation.set_visible(False)

#implement hover event
def motion_hover(event):
    annotation_visibility = annotation.get_visible()
    if event.inaxes == ax:
        is_contained, annotation_index = scatter.contains(event)
        if is_contained:
            data_point_location = scatter.get_offsets()[annotation_index['ind'][0]]
            annotation.xy = data_point_location
            text_labela = '{}'.format(text_label[f'{int(data_point_location[0])}'])
            annotation.set_text(text_labela)
            annotation.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annotation_visibility:
                annotation.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect('motion_notify_event', motion_hover)


#naming the titles in each side and at the top of the diagram
ax.set_xlabel('Zipcode')
ax.set_ylabel('Bottles sold')
ax.set_title('Bottles sold')
plt.show()
