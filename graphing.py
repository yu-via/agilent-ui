import matplotlib.pyplot as plt
import pandas as pd
from itertools import cycle

def freq_dev_error_zoom(csv_file):
    df_full = pd.read_csv(csv_file)
    df = df_full[df_full['Error'] >=0]
    grouped = df.groupby('Freq Dev').agg(
            mean_error=('Error', 'mean'),
            std_error=('Error', 'std')
        ).reset_index()
    plt.figure(figsize=(20, 12))
    plt.errorbar(grouped['Freq Dev'], grouped['mean_error'], yerr=grouped['std_error'], fmt='o', linestyle='-', color='b', capsize=5)
    plt.title('Percent Error vs. Freq Dev')
    plt.xlabel('Freq Dev')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.show()
def freq_dev_error_full(csv_file):
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(20, 12))
    plt.plot(df['Freq Dev'], df['Error'], marker='o', linestyle='-', color='g')
    plt.title('Percent Error vs. Freq Dev')
    plt.xlabel('Freq Dev')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.show()
def two_full_plot(csv1,csv2):
    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)
    plt.figure(figsize=(20, 12))
    plt.plot(df1['Freq Dev'], df1['Error'], marker='o', linestyle='-', color='g')
    plt.plot(df2['Freq Dev'], df2['Error'], marker='o', linestyle='-', color='r')
    plt.title('Percent Error vs. Freq Dev')
    plt.xlabel('Freq Dev')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.show()
def combine(file1,file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    combined_df = pd.concat([df1, df2], ignore_index=True)
    
    combined_df = combined_df.sort_values(by='Freq Dev')
    return combined_df
def convert(file):
    df = pd.read_csv(file)
    df = df.sort_values(by='Freq Dev')
    return df
def combined_plot(df_list,range):
    plt.figure(figsize=(20, 12))
    colors = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    for df, color, max_val in zip(df_list, colors, range):
        df['Normalized'] = df['Freq Dev'] / max_val
        df = df[df['Error'] <=100]
        range_value = df['Range'].iloc[0]
        plt.plot(df['Normalized'], df['Error'], marker='o', linestyle='-', color=color, label=f'Range {range_value}')
    
    plt.xscale('log')
    plt.title('Percent Error vs. Freq Dev')
    plt.xlabel('Normalized Freq Dev')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.legend(title='Range Values')
    plt.show()
def zoom_plot(df_list,range):
    plt.figure(figsize=(20, 12))
    colors = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    for df, color, max_val in zip(df_list, colors, range):
        df['Normalized'] = df['Freq Dev'] / max_val
        df = df[(df['Error'] >= -1) & (df['Error'] <= 1)]        
        range_value = df['Range'].iloc[0]
        plt.plot(df['Normalized'], df['Error'], marker='o', linestyle='-', color=color, label=f'Range {range_value}')
    
    plt.xscale('log')
    plt.title('Percent Error vs. Freq Dev')
    plt.xlabel('Normalized Freq Dev')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.legend(title='Range Values')
    plt.show()   
file5_1 = 'plots/range5_dev0.05-2.csv'
file5_2 = 'plots/range5_dev5-95.csv'

file100_1 = 'plots/range100_dev0.1-45.csv'
file100_2 = 'plots/range100_dev50-1800.csv'

file10_1 = 'plots/range10_dev0.1-2.9.csv'
file10_2 = 'plots/range10_dev5-195.csv'

file50_1 = 'plots/range50_dev0.1-9.5.csv'
file50_2 = 'plots/range50_dev10-820.csv'

file20_1 = 'plots/range20_dev0.5-4.5.csv'
file20_2 = 'plots/range20_dev5-365.csv'

file500_1 = 'plots/range500_dev0.05-95.csv'
file500_2 = 'plots/range500_dev100-9000.csv'

file1000_1 = 'plots/range1000_dev0.1-45.csv'
file1000_2 = 'plots/range1000_dev50-15000.csv'

file200_1 = 'plots/range200_dev0.05-45.csv'
file200_2 = 'plots/range200_dev50-3300.csv'

new_file200 = 'plots/range200_dev0.05-3300_new.csv'
new_file100 = 'plots/range100_dev0.1-1800_new.csv'

new_file50_1 = 'plots/range50_dev0.1-9.5_new.csv'
new_file50_2 = 'plots/range50_dev10-840_new.csv'

new_file5 = 'plots/range5_dev0.05-95_new.csv'

new_file10 = 'plots/range10_dev0.1-195_new.csv'

new_file20 = 'plots/range20_dev0.5-365_new.csv'

new_file500 = 'plots/range500_dev0.05-9000_new.csv'

new_file1000 = 'plots/range1000_dev0.1-13000_new.csv'

df_list = [combine(file10_1,file10_2),combine(file20_1,file20_2),combine(file50_1,file50_2),combine(file100_1,file100_2),combine(file200_1,file200_2),combine(file500_1,file500_2),combine(file1000_1,file1000_2)]
df_list = [convert(new_file10),convert(new_file20),combine(new_file50_1,new_file50_2),convert(new_file100),convert(new_file200),convert(new_file500),convert(new_file1000)]
range_list = [158,316,790,1580,3160,7901,15802]

#combined_plot(df_list,range_list)
#zoom_plot(df_list,range_list)

df = [convert('plots/new_range1000_test.csv'),convert('plots/new_range1000_test2.csv'),combine(file1000_1,file1000_2),convert(new_file1000)]
range = [15802,15802,15802,15802]
combined_plot(df,range)
zoom_plot(df,range)