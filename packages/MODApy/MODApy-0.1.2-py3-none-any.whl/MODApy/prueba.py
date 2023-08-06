from collections import OrderedDict

import cyvcf2
import pandas as pd

vcf = '/DiscoDatos/Development/modapy/data/Patients/PUFRA/PUFRA.final.vcf'
pVCF = cyvcf2.Reader(vcf)
variantsDict = OrderedDict()
for variant in pVCF:
    variantsDict[variant.CHROM + '+' + str(variant.POS) + '+' + variant.REF + '+' + ','.join(variant.ALT)] = {
        'ID': variant.ID, 'QUAL': variant.QUAL, 'FILTER': variant.FILTER}
    variantsDict[variant.CHROM + '+' + str(variant.POS) + '+' + variant.REF + '+' + ','.join(variant.ALT)].update(
        {k: v for (k, v) in variant.INFO})

df1 = pd.DataFrame.from_dict(variantsDict, orient='index')
df1.index = df1.index.str.split('+', expand=True)
df1.index.names = ['CHROM', 'POS', 'REF', 'ALT']
df1.reset_index(inplace=True)
anndf = df1['ANN']
df1.drop(columns='ANN', inplace=True)
pruebadf = df1.loc[df1['ALT'].str.contains(',') == True].copy()
collist = list()
collist.append('ALT')
collist.append('ID')
pruebadf.fillna('', inplace=True)
pru2 = pd.DataFrame()
for column in collist:
    pru2[column] = pruebadf[column].astype(str).str.split(',', n=1).stack()
    pru2 = pru2.reset_index()[['CHROM', 'POS', 'REF', column]]
    pru2.columns = [column, 'CHROM', 'POS', 'REF']
    print(len(pru2))
    pruebadf = pruebadf.merge(pru2, on=['CHROM', 'POS', 'REF'], how='left')
    pruebadf[column] = pruebadf[column + '_y'].combine_first(pruebadf[column + '_x'])
    pruebadf.drop(columns=[column + '_x', column + '_y'], inplace=True)

print(pruebadf)
