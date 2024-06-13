import pandas as pd
list_name= 'Ohtani_Gjerloev2020.csv' #as an example
data= pd.read_csv(list_name, parse_dates='Date_UTC') # parse dates just nice converts the column into a proper date format rather than just a string

