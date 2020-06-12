import pandas as pd
import numpy as np
import xlrd

df = pd.read_excel('Koln-Airport-Scripted.xlsx')
df2 = pd.read_excel('Cologne - Bonn Airport.xlsx')

df_merge_col = pd.merge(df, df2, on='Parking Address')

print(df_merge_col)
writer = pd.ExcelWriter('Koln-Airport-refactored.xlsx', engine= 'xlsxwriter')
df_merge_col.to_excel(writer, sheet_name='Sheet1')
writer.save()








