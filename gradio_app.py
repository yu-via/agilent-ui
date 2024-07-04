import gradio as gr
import pandas as pd
from random_generator import generate_random_numbers

def calc_velocity(range, rf1, rf2, times, existing_data):
    results = generate_random_numbers(times)
    shift = rf1 - rf2
    measured = [(r * range * 10**-3) for r in results]
    expected = shift * 632.81 * 10**-6
    new_data = [[range, shift, m, expected, ((m - expected) / expected * 100)] for m in measured]
    
    # Append new data to existing data
    if existing_data is None:
        existing_data = []
    table_data = existing_data + new_data

    # Prepare data for the plot
    df = pd.DataFrame(table_data, columns=["Range", "Shift", "Measured", "Expected", "Error"])

    return table_data, table_data, df

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale = 1):
            range_input = gr.Number(label="Range", value=20)
            rf1_input = gr.Number(label="RF 1 Frequency", value=110)
            rf2_input = gr.Number(label="RF 2 Frequency", value=110)
            times_input = gr.Number(label="Number of Data Points", value=10)
            generate_button = gr.Button("Calculate")
        with gr.Column(scale = 4):
            output_table = gr.Dataframe(headers=["Range", "Shift", "Measured", "Expected", "Error"])
            existing_data = gr.State(value=[])
    output_plot = gr.LinePlot(x="Shift", y="Measured", label="Measured vs Shift")

    generate_button.click(
        fn=calc_velocity,
        inputs=[range_input, rf1_input, rf2_input, times_input, existing_data],
        outputs=[output_table, existing_data, output_plot]
    )


demo.launch(share=True)
