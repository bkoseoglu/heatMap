import pandas as pd
import geopandas as gpd
import geoplot as gplt
import sys
import geoplot.crs as gcrs
import matplotlib.pyplot as plt


def take_inverse(row):
	return 1-row['Unbanked']

def get_world_data_frame():
	path = gpd.datasets.get_path('naturalearth_lowres')
	df = gpd.read_file(path)
	return df

if __name__ == "__main__":
	#xls = pd.ExcelFile('Global Findex Database.xlsx')
	#df = pd.read_excel(xls, 'Data')
	df = pd.read_excel('data/Global Findex Database.xlsx',sheet_name = 'Data', usecols = "A:F")
	df = df.loc[df['Year'] == 2017]
	print(df.columns.values[-1],"column_names")
	df = df.rename(columns={df.columns.values[-1]: "Unbanked"})
	df = df.rename(columns={'Country': "name"})
	df['Unbanked'] = df.apply(take_inverse, axis=1)
	df = df.filter(items=['name','Unbanked'])
	df = df.reset_index(drop=True)
	df.to_csv("HeatMap.csv", sep='\t', encoding='utf-8')
	dfWorld = get_world_data_frame()
	print(df.columns.values,"columnNames")
	dfWorld = pd.merge(dfWorld,df, on=['name','name'])

	print(df.head())
	#proj = gcrs.AlbersEqualArea()
	proj = gcrs.PlateCarree()
	#ax = gplt.polyplot(dfWorld, projection=proj)
	#print(ax)
	legend_kwargs = {'loc' : 'upper left'}
	#hue is the data series to visualize
	#dfWorld is geometry specified
	#proj is the projection type 
	gplt.choropleth(dfWorld, 
                hue=dfWorld['Unbanked'],  # Display data, passed as a Series
                projection=proj,
                cmap='Purples', 
                k=None,  # Do not bin our counties.
                legend=True,
                edgecolor='white', linewidth=0.5,
                figsize=(13.65, 10.24))
	plt.title("World Unbanked/Underbanked People Heat Map")
	plt.savefig("world unbanked population.png", bbox_inches='tight', pad_inches=0.1)


	
