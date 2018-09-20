import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)



def question_1():
    df1 = pd.read_csv('olympics_dataset1.csv',skiprows=1)
    df2 = pd.read_csv('olympics_dataset2.csv',skiprows=1)
    df1.columns = df1.columns.str.replace('Unnamed.*', 'country')
    df2.columns = df2.columns.str.replace('Unnamed.*', 'country')
    df = pd.merge(df1, df2, how = 'outer',on = 'country', suffixes=['_1', '_2'])
    print(",".join([column for column in df]))
    for index, row in df.head(5).iterrows():
        print(",".join([str(row[column]) for column in df]))




def question_2():
    df1 = pd.read_csv('olympics_dataset1.csv', index_col=0, skiprows=1)
    df2 = pd.read_csv('olympics_dataset2.csv', index_col=0, skiprows=1)
    df = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=['_1', '_2'])
    df = df.drop('Totals')
    print(",".join([column for column in df]))
    for index, row in df.head(1).iterrows():
        print(",".join([str(row[column]) for column in df]))


def question_3():
    df1 = pd.read_csv('olympics_dataset1.csv',skiprows=1)
    df2 = pd.read_csv('olympics_dataset2.csv',skiprows=1)
    df1.columns = df1.columns.str.replace('Unnamed.*', 'country')
    df2.columns = df2.columns.str.replace('Unnamed.*', 'country')
    df = pd.merge(df1, df2, how = 'outer',on = 'country', suffixes=['_1', '_2'])
    df.drop(columns=['Rubish'],inplace=True)
    print(",".join([column for column in df]))
    for index, row in df.head(5).iterrows():
        print(",".join([str(row[column]) for column in df]))


def question_4():
    df1 = pd.read_csv('olympics_dataset1.csv',skiprows=1)
    df2 = pd.read_csv('olympics_dataset2.csv',skiprows=1)
    df1.columns = df1.columns.str.replace('Unnamed.*', 'country')
    df2.columns = df2.columns.str.replace('Unnamed.*', 'country')
    df = pd.merge(df1, df2, how = 'outer',on = 'country', suffixes=['_1', '_2'])
    d = df.dropna(how='any')
    d = d.drop([158])
    print(",".join([column for column in d]))
    for index, row in d.tail(10).iterrows():
        print(",".join([str(row[column]) for column in d]))

def question_5():
    df1 = pd.read_csv('olympics_dataset1.csv', index_col=0, skiprows=1, thousands=',')
    df2 = pd.read_csv('olympics_dataset2.csv', index_col=0, skiprows=1, thousands=',')
    df = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=['_1', '_2'])
    df = df.drop('Totals')
    a =df['Gold_1'].idxmax(axis=1)
    print('The country won the most gold medals in summer games:',a)



def question_6():
    df1 = pd.read_csv('olympics_dataset1.csv', index_col=0, skiprows=1, thousands=',')
    df2 = pd.read_csv('olympics_dataset2.csv', index_col=0, skiprows=1, thousands=',')
    df = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=['_1', '_2'])
    df = df.drop('Totals')
    for _ in df.iterrows():
        summer = df['Gold_1']
        winter = df['Gold_2']
        df['difference'] = abs(summer - winter)
    md = df['difference'].idxmax()
    print('The country that has the biggest difference between their summer and winter gold medal:',md)



def question_7():
    #pd.set_option('max_rows', 10) #the function that show the first five rows and last five rows
    df1 = pd.read_csv('olympics_dataset1.csv',skiprows=1,thousands=',')
    df2 = pd.read_csv('olympics_dataset2.csv',skiprows=1,thousands=',')
    df1.columns = df1.columns.str.replace('Unnamed.*', 'country')
    df2.columns = df2.columns.str.replace('Unnamed.*', 'country')
    df = pd.merge(df1, df2, how = 'outer',on = 'country', suffixes=['_1', '_2'])
    df = df.drop([158])
    a = df.sort_values(by = 'Total.1',ascending=False)
    print(",".join([column for column in a]))
    for index, row in a.head(5).iterrows():
        print(",".join([str(row[column]) for column in a]))
    for index, row in a.tail(5).iterrows():
        print(",".join([str(row[column]) for column in a]))



def question_8():
    df1 = pd.read_csv('olympics_dataset1.csv', index_col=0, skiprows=1, thousands=',')
    df2 = pd.read_csv('olympics_dataset2.csv', index_col=0, skiprows=1, thousands=',')
    df = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=['_1', '_2'])
    df = df.drop('Totals')
    names_ids = df.index.str.split('\s\(')  # split the index by '('
    df.index = names_ids.str[0].str.strip()  # the [0] element is the country name (new index)
    df = df.sort_values(by = 'Total.1',ascending=False)
    df.rename(columns = {'Total_1':'Summer games','Total_2':'Winter games'},inplace=True)
    df = df.head(10)
    df[['Winter games','Summer games']].plot.barh(title="Medals for winter and summer Games",stacked=True)



def question_9():
    df1 = pd.read_csv('olympics_dataset1.csv', index_col=0, skiprows=1, thousands=',')
    df2 = pd.read_csv('olympics_dataset2.csv', index_col=0, skiprows=1, thousands=',')
    df = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=['_1', ''])
    names_ids = df.index.str.split('\s\(') # split the index by '('
    df.index = names_ids.str[0].str.strip()# the [0] element is the country name (new index)
    b = df.ix[['United States', 'Australia', 'Great Britain', 'Japan', 'New Zealand'],['Gold','Silver','Bronze']]
    b[['Gold','Silver','Bronze']].plot.bar(title="Winter Games")
    plt.xticks(rotation = 360)
    plt.show()




if __name__ == "__main__":
    print('question1')
    question_1()
    print('question2')
    question_2()
    print('quesiton3')
    question_3()
    print('question4')
    question_4()
    print('question5')
    question_5()
    print('question6')
    question_6()
    print('question7')
    question_7()
    question_8()
    question_9()
