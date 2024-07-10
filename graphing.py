import matplotlib.pyplot as plt
import pandas as pd
def shift_plot_zoom(csv_file):
    df_full = pd.read_csv(csv_file)
    df = df_full[df_full['Error'] >=0]
    grouped = df.groupby('Shift').agg(
            mean_error=('Error', 'mean'),
            std_error=('Error', 'std')
        ).reset_index()
    plt.figure(figsize=(20, 12))
    plt.errorbar(grouped['Shift'], grouped['mean_error'], yerr=grouped['std_error'], fmt='o', linestyle='-', color='b', capsize=5)
    plt.title('Percent Error vs. Shift')
    plt.xlabel('Shift')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.show()
def shift_plot_full(csv_file):
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(20, 12))
    plt.plot(df['Shift'], df['Error'], marker='o', linestyle='-', color='g')
    plt.title('Percent Error vs. Shift')
    plt.xlabel('Shift')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.show()
def freq_dev_plot_zoom(csv_file):
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
def freq_dev_plot_full(csv_file):
    df = pd.read_csv(csv_file)
    plt.figure(figsize=(20, 12))
    plt.plot(df['Freq Dev'], df['Error'], marker='o', linestyle='-', color='g')
    plt.title('Percent Error vs. Freq Dev')
    plt.xlabel('Freq Dev')
    plt.ylabel('Percent Error')
    plt.grid(True)
    plt.show()
csv_file = 'plots/range50_dev10-880_vd06.csv'
freq_dev_plot_zoom(csv_file)
freq_dev_plot_full(csv_file)
