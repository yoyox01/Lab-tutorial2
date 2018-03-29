import pandas as pd
import numpy as np

''' read csv '''
df_J1 = pd.read_csv("105Jongli_table1.csv", encoding="big5")
df_J2 = pd.read_csv("105Jongli_table2.csv", encoding="big5")
df_J3 = pd.read_csv("105Jongli_target_variable.csv", encoding="big5")

df_T1 = pd.read_csv("105Taoyuan_table1.csv", encoding="big5")
df_T2 = pd.read_csv("105Taoyuan_table2.csv", encoding="big5")
df_T3 = pd.read_csv("105Taoyuan_target_variable.csv", encoding="big5")


''' merge 3 Jongli tables in 1 '''
res_Jongli = pd.merge(df_J1, df_J2, on=['date','location','time'])          # merge Jongli table #1 and #2
res_Jongli = res_Jongli.drop(columns=res_Jongli.columns[0])                 # drop the Unnamed column
res_Jongli = res_Jongli.drop(columns=res_Jongli.columns[12])                # drop the Unnamed column

res_Jongli = pd.merge(res_Jongli, df_J3, on=['date','location','time'])     # the final merge of Jongli table
res_Jongli = res_Jongli.drop(columns=res_Jongli.columns[20])                # drop the Unnamed column
#res_Jongli.to_csv("test.csv", encoding="big5")


''' merge 3 Taoyuan tables in 1 '''
res_Taoyuan = pd.merge(df_T1, df_T2, on=['date','location','time'])         # merge Taoyuan table #1 and #2
res_Taoyuan = res_Taoyuan.drop(columns=res_Taoyuan.columns[0])              # drop the Unnamed column
res_Taoyuan = res_Taoyuan.drop(columns=res_Taoyuan.columns[12])             # drop the Unnamed column

res_Taoyuan = pd.merge(res_Taoyuan, df_T3, on=['date','location','time'])   # the final merge of Taoyuan table
res_Taoyuan = res_Taoyuan.drop(columns=res_Taoyuan.columns[21])             # drop the Unnamed column
#res_Taoyuan.to_csv("test2.csv", encoding="big5")


''' merge Jongli and Taoyuan '''
result = pd.concat([res_Jongli,res_Taoyuan])                                # merge Jongli and Taoyuan

cols = result.columns.tolist()                                              # rearrange
cols = cols[-3:] + cols[:-3]
result = result[cols]

result.replace('\*|#|-|[A-Z]|[a-z]', 0, regex=True, inplace=True)           # clean data
#result.replace('NR', 0, inplace=True)
result.fillna(0, inplace=True)

result.to_csv("105Jongli_and_Taoyuan.csv", encoding="big5")


''' (1) '''
result['SO2'] = result.SO2.astype(float)
#print(result.dtypes)
ans1 = result['SO2'].max()
print("\n(1) The maximum value of SO2 is : ", ans1)


''' (2) '''
result['CO'] = result.CO.astype(float)
ans2 = result.loc[result.location=='中壢','CO'].mean()
print("\n(2) The average value of CO in Jongli is :", ans2)


''' (3) '''
result.rename(columns={'PM2.5':'PM25'}, inplace=True)
result['PM25'] = result.PM25.astype(float)
result.rename(columns={'PM25':'PM2.5'}, inplace=True)
ans3_1 = result['date'][result['PM2.5'].idxmax()]
ans3_2 = result['location'][result['PM2.5'].idxmax()]

#print(result['PM2.5'].idxmax())
print(ans3_1)
print(ans3_2)