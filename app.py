import sys
import os
import gradio as gr
import pandas as pd
import math
from main import dc_volt, ac_volt
from random_generator import generate_random_numbers

def calc_dc(range, rf1, rf2, times, existing_data):
    results = dc_volt(times)
    shift = rf1 - rf2
    measured = [(r * range * 10**-3) for r in results]
    expected = shift * 632.81 * 10**-3
    new_data = [[range, shift, m, expected, ((m - expected) / expected * 100)] for m in measured]
    
    if existing_data is None:
        existing_data = []
    table_data = existing_data + new_data

    df = pd.DataFrame(table_data, columns=["Range", "Shift", "Measured", "Expected", "Error"])

    return table_data, table_data, df, df

def calc_ac(range, dev, fm, times, existing_data):
    results = ac_volt(times)
    measured = [(r * range * 10**-3) for r in results]
    expected = dev/math.sqrt(2) * 632.81 * 10**-6
    new_data = [[range, dev, fm, m, expected, ((m - expected) / expected * 100)] for m in measured]
    
    if existing_data is None:
        existing_data = []
    table_data = existing_data + new_data

    df = pd.DataFrame(table_data, columns=["Range", "Freq Dev", "FM Freq", "Measured", "Expected", "Error"])

    return table_data, table_data, df,df,df

def reset_dc(existing_data):
    return [], [], pd.DataFrame(), pd.DataFrame()
def reset_ac(existing_data):
    return [], [], pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def download_dc(data):
    df = pd.DataFrame(data, columns=["Range", "Shift", "Measured", "Expected", "Error"])
    csv_file = "data.csv"
    df.to_csv(csv_file, index=False)
    return csv_file
def download_ac(data):
    df = pd.DataFrame(data, columns=["Range", "Freq Dev", "FM Freq", "Measured", "Expected", "Error"])
    csv_file = "data.csv"
    df.to_csv(csv_file, index=False)
    return csv_file
with gr.Blocks() as demo:
    with gr.Tab("DC Velocity"):
        with gr.Row():
            with gr.Column(scale=1):
                range_input = gr.Number(label="Range", value=20)
                rf1_input = gr.Number(label="RF 1 Frequency", value=110)
                rf2_input = gr.Number(label="RF 2 Frequency", value=110)
                times_input = gr.Number(label="Number of Data Points", value=10)
                generate_button = gr.Button("Calculate")
                reset_button = gr.Button("Reset")
                download_button = gr.Button("Download as CSV")
            with gr.Column(scale=4):
                output_table = gr.Dataframe(headers=["Range", "Shift", "Measured", "Expected", "Error"])
                existing_data = gr.State(value=[])
        with gr.Tab("Measured vs Shift"):
            output_plot = gr.LinePlot(x="Shift", y="Measured", label="Measured vs Shift")
        with gr.Tab("Error vs Shift"):
            error_plot = gr.ScatterPlot(x="Shift", y="Error", label="Error vs Shift")

        generate_button.click(
            fn=calc_dc,
            inputs=[range_input, rf1_input, rf2_input, times_input, existing_data],
            outputs=[output_table, existing_data, output_plot,error_plot]
        )

        reset_button.click(
            fn=reset_dc,
            inputs=[existing_data],
            outputs=[output_table, existing_data, output_plot,error_plot]
        )

        download_button.click(
            fn=download_dc,
            inputs=[existing_data],
            outputs=gr.File(label="Download CSV")
        )

    with gr.Tab("AC Velocity"):
        with gr.Row():
            with gr.Column(scale=1):
                range_input = gr.Number(label="Range", value=20)
                dev_input = gr.Number(label="Freq Dev", value=50)
                fm_input = gr.Number(label="FM Freq", value=10)
                times_input = gr.Number(label="Number of Data Points", value=10)
                generate_button = gr.Button("Calculate")
                reset_button = gr.Button("Reset")
                download_button = gr.Button("Download as CSV")
            with gr.Column(scale=4):
                output_table = gr.Dataframe(headers=["Range", "Freq Dev", "FM Freq", "Measured", "Expected", "Error"])
                existing_data = gr.State(value=[])
        with gr.Tab("Measured vs FM Freq"):
            fm_plot = gr.LinePlot(x="FM Freq", y="Measured", label="Measured vs FM Freq")
        with gr.Tab("Measured vs Freq Dev"):
            dev_plot = gr.LinePlot(x="Freq Dev", y="Measured", label="Measured vs Freq Dev")
        with gr.Tab("Error vs Freq Dev"):
            error_plot = gr.ScatterPlot(x="Freq Dev", y="Error", label="Error vs Freq Dev")

        generate_button.click(
            fn=calc_ac,
            inputs=[range_input, dev_input, fm_input, times_input, existing_data],
            outputs=[output_table, existing_data, fm_plot,dev_plot,error_plot]
        )

        reset_button.click(
            fn=reset_ac,
            inputs=[existing_data],
            outputs=[output_table, existing_data, fm_plot, dev_plot, error_plot]
        )

        download_button.click(
            fn=download_ac,
            inputs=[existing_data],
            outputs=gr.File()
        )

demo.launch(share=True)
