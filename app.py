import sys
import os
import gradio as gr
import pandas as pd
import math
import numpy as np
from main import dc_volt, ac_volt
from random_generator import generate_random_numbers
from rf_pyvisa import *

def calc_dc(range, rf1, rf2_min, rf2_max, interval, times, existing_data):
    if existing_data is None:
        existing_data = []

    table_data = existing_data

    for rf in np.arange(rf2_min, rf2_max, interval):
        set_dc(rf * 10**6)
        results = dc_volt(times)
        shift = rf1 - rf
        measured = [(r * range * 10**-3) for r in results]
        expected = shift * 632.81 * 10**-3
        new_data = [[range, shift, m, expected, ((m - expected) / expected * 100)] for m in measured]
        table_data += new_data

    df = pd.DataFrame(table_data, columns=["Range", "Shift", "Measured", "Expected", "Error"])
    set_off()
    return table_data, table_data, df, df

def calc_ac_fm(range, dev, fm_min, fm_max, interval, times, existing_data):
    if existing_data is None:
        existing_data = []

    table_data = existing_data
    for fm in np.arange(fm_min, fm_max, interval):
        set_ac(dev * 10**3, fm * 10**3)
        results = ac_volt(times)
        measured = [(r * range * 10**-3) for r in results]
        expected = dev / math.sqrt(2) * 632.81 * 10**-6
        new_data = [[range, dev, fm, m, expected, ((m - expected) / expected * 100)] for m in measured]
        table_data += new_data

    df = pd.DataFrame(table_data, columns=["Range", "Freq Dev", "FM Freq", "Measured", "Expected", "Error"])
    set_off()
    return table_data, table_data, df, df
def calc_ac_dev(range, dev_min,dev_max, fm, interval, times, existing_data):
    if existing_data is None:
        existing_data = []

    table_data = existing_data
    for dev in np.arange(dev_min, dev_max, interval):
        set_ac(dev * 10**3, fm * 10**3)
        results = ac_volt(times)
        measured = [(r * range * 10**-3) for r in results]
        expected = dev / math.sqrt(2) * 632.81 * 10**-6
        new_data = [[range, dev, fm, m, expected, ((m - expected) / expected * 100)] for m in measured]
        table_data += new_data

    df = pd.DataFrame(table_data, columns=["Range", "Freq Dev", "FM Freq", "Measured", "Expected", "Error"])
    set_off()
    return table_data, table_data, df, df

def reset(existing_data):
    return [], [], pd.DataFrame(), pd.DataFrame()

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
                range_input = gr.Number(label="Range", value=200)
                rf1_input = gr.Number(label="RF 1 Frequency", value=110)
                rf2_min = gr.Number(label="RF 2 Min", value=110)
                rf2_max = gr.Number(label="RF 2 Max", value=110)
                interval = gr.Number(label="Interval", value=0.5)
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
            inputs=[range_input, rf1_input, rf2_min, rf2_max, interval, times_input, existing_data],
            outputs=[output_table, existing_data, output_plot, error_plot]
        )

        reset_button.click(
            fn=reset,
            inputs=[existing_data],
            outputs=[output_table, existing_data, output_plot, error_plot]
        )

        download_button.click(
            fn=download_dc,
            inputs=[existing_data],
            outputs=gr.File(label="Download CSV")
        )

    with gr.Tab("AC Velocity - FM Freq"):
        with gr.Row():
            with gr.Column(scale=1):
                range_input = gr.Number(label="Range", value=20)
                dev_input = gr.Number(label="Freq Dev", value=50)
                fm_min = gr.Number(label="FM Freq Min", value=10)
                fm_max = gr.Number(label="FM Freq Max", value=300)
                interval = gr.Number(label = "Interval", value=50)
                times_input = gr.Number(label="Number of Data Points", value=10)
                generate_button = gr.Button("Calculate")
                reset_button = gr.Button("Reset")
                download_button = gr.Button("Download as CSV")
            with gr.Column(scale=4):
                output_table = gr.Dataframe(headers=["Range", "Freq Dev", "FM Freq", "Measured", "Expected", "Error"])
                existing_data = gr.State(value=[])
        with gr.Tab("Measured vs FM Freq"):
            fm_plot = gr.LinePlot(x="FM Freq", y="Measured", label="Measured vs FM Freq")
        with gr.Tab("Error vs FM Freq"):
            error_plot = gr.ScatterPlot(x="FM Freq", y="Error", label="Error vs FM Freq")

        generate_button.click(
            fn=calc_ac_fm,
            inputs=[range_input, dev_input, fm_min, fm_max, interval, times_input, existing_data],
            outputs=[output_table, existing_data, fm_plot, error_plot]
        )

        reset_button.click(
            fn=reset,
            inputs=[existing_data],
            outputs=[output_table, existing_data, fm_plot, error_plot]
        )

        download_button.click(
            fn=download_ac,
            inputs=[existing_data],
            outputs=gr.File()
        )
    with gr.Tab("AC Velocity - Freq Dev"):
        with gr.Row():
            with gr.Column(scale=1):
                range_input = gr.Number(label="Range", value=20)
                dev_min = gr.Number(label="Freq Dev Min", value=50)
                dev_max = gr.Number(label="Freq Dev Max", value=600)
                fm_input = gr.Number(label="FM Freq", value=10)
                interval = gr.Number(label="Interval",value=50)
                times_input = gr.Number(label="Number of Data Points", value=10)
                generate_button = gr.Button("Calculate")
                reset_button = gr.Button("Reset")
                download_button = gr.Button("Download as CSV")
            with gr.Column(scale=4):
                output_table = gr.Dataframe(headers=["Range", "Freq Dev", "FM Freq", "Measured", "Expected", "Error"])
                existing_data = gr.State(value=[])
        with gr.Tab("Measured vs Freq Dev"):
            dev_plot = gr.LinePlot(x="Freq Dev", y="Measured", label="Measured vs Freq Dev")
        with gr.Tab("Error vs Freq Dev"):
            error_plot = gr.ScatterPlot(x="Freq Dev", y="Error", label="Error vs Freq Dev")

        generate_button.click(
            fn=calc_ac_dev,
            inputs=[range_input, dev_min,dev_max, fm_input, interval, times_input, existing_data],
            outputs=[output_table, existing_data, dev_plot, error_plot]
        )

        reset_button.click(
            fn=reset,
            inputs=[existing_data],
            outputs=[output_table, existing_data, dev_plot, error_plot]
        )

        download_button.click(
            fn=download_ac,
            inputs=[existing_data],
            outputs=gr.File()
        )

demo.launch(share=True)
