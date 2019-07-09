import glob
from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import read_pdf
import pandas as pd
import numpy as np

PROVINCES = {'Alberta': 'AB', 'British Columbia': 'BC', 'Manitoba': 'MB',
             'New Brunswick': 'NB', 'New Foundland and Labrador': 'NL',
             'Northwest Territories': 'NT', 'Nova Scotia': 'NS',
             'Nunavut': 'NU', 'Ontario': 'ON', 'Quebec': 'QC',
             'Saskatchewan': 'SK', 'Yukon Ter': 'YT'
             }

inputpdf = PdfFileReader(open("otd.pdf", "rb"))
for i in range(37, 48):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("pg%s_n.pdf" % i, "wb") as outputStream:
        output.write(outputStream)

files = glob.glob('*n.pdf')

final = pd.DataFrame()

for j in range(len(files)):
    df1 = read_pdf(files[j])

    # tabula breaks on page 9
    if df1.columns[0] == 'Location Elevation':
        df1 = df1.rename(columns={'Location Elevation': 'Location'})
        df1 = df1.iloc[6:, ]
        df1['Location'] = df1['Location'].str[:-6]

        df2 = pd.DataFrame(columns=['Location', 'Cooling'])
        df2.loc[0] = ['Saskatchewan'] + [np.nan]
        df1 = pd.concat([df2, df1])

    df1 = df1[['Location', 'Cooling']]
    final = pd.concat([final, df1])
    final['Cooling'] = final['Cooling'].str[:2]
    final = final[pd.notnull(final['Location'])]
    final = final.reset_index(drop=True)

for k, v in PROVINCES.items():
    r = final.index[final['Location'] == k][0]
    final.loc[(r+1):, 'PR'] = v

final = final[pd.notnull(final['Cooling'])]
final.columns = ['station', 'design_temp', 'province']
final.to_csv('design_temps.csv')

