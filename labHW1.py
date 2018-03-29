import pandas as pd

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

res_Jongli.to_csv("test.csv", encoding="big5")
res_Jongli.info()

''' merge 3 Taoyuan tables in 1 '''
res_Taoyuan = pd.merge(df_T1, df_T2, on=['date','location','time'])         # merge Taoyuan table #1 and #2
res_Taoyuan = res_Taoyuan.drop(columns=res_Taoyuan.columns[0])              # drop the Unnamed column
res_Taoyuan = res_Taoyuan.drop(columns=res_Taoyuan.columns[12])             # drop the Unnamed column

res_Taoyuan = pd.merge(res_Taoyuan, df_T3, on=['date','location','time'])   # the final merge of Taoyuan table
res_Taoyuan = res_Taoyuan.drop(columns=res_Taoyuan.columns[21])             # drop the Unnamed column

res_Taoyuan.to_csv("test2.csv", encoding="big5")
res_Taoyuan.info()


''' merge Jongli and Taoyuan '''
result = pd.concat([res_Taoyuan,res_Jongli])
#result = res_Taoyuan.append(res_Jongli)
result.to_csv("test3.csv", encoding="big5")
result.info()

