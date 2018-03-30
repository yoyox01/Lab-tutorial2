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

result.reset_index(inplace=True, drop=True)                                 # reindex

result.to_csv("105Jongli_and_Taoyuan.csv", encoding="big5")                 # output the final merge of Jongli and Taoyuan

#print(result.dtypes)
for col in result.iloc[:, 3:]:                                              # convert object types to float
    result[col] = pd.to_numeric(result[col])
#print(result.dtypes)



''' (1) '''
ans1 = result['SO2'].max()                                                  # find max
print("\n(1) The maximum value of SO2 is : \n", ans1)



''' (2) '''
ans2 = result.loc[result.location=='中壢','CO'].mean()                      # calculate the average
print("\n(2) The average value of CO in Jongli is : \n", ans2)



''' (3) '''
ans3_1 = result['date'][result['PM2.5'].idxmax()]                           # date of maximum PM2.5
ans3_2 = result['location'][result['PM2.5'].idxmax()]                       # location of maximum PM2.5

print("\n(3) The maximum value of PM2.5 is in : \n", ans3_1, ",", ans3_2)



''' (4) '''
result['date'] = pd.to_datetime(result.date)                                # convert float type to datetime
taoyuan_april = result[(result.date.dt.month == 4) & 
                (result.location.str.encode('big5','strict') == u'桃園'.encode('big5','strict'))]
ans4 = taoyuan_april.O3.mean()
print("\n(4) The average density of O3 in Taoyuan is : \n", ans4)



''' (5) '''
#result.rename(columns={'PM2.5':'PM25'}, inplace=True)
correlations = result.corr()                                                    # dataFrame of all correlations
ans5 = correlations[correlations['PM2.5'] > 0.3]['PM2.5']
print("\n(5) The correlation with PM2.5 over 0.3 in Jongli and Taoyuan is :")
print(ans5)



''' (6) '''
NO_avg = result['NO'].mean()
tmp = result[result['NO']<result['NO'].mean()]                                  # a dataFrame that NO vaules is smaller than averrage
tmp = tmp.sort_values('PM10',ascending=False)                                   # PM10 sorted descendingly
ans6 = tmp.loc[: ,['date','time','location','NO','PM10']]
print("\n(6) List the date, time and location of the top 10 PM10 density ")
print("that the NO density is lower than average :\n")
print(ans6.head(10))
print("\n (NO averrage : ", NO_avg ,")")