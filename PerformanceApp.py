import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np

def update_figure(data, threshold_value, threshold_enabled):
    axes = fig.axes[0]
    x = [i[0] for i in data]
    y = [int(i[1]) for i in data]

    # Clear the previous plot
    axes.clear()

    # Set background color
    axes.set_facecolor('#efefef')  # Light gray

    # Plot a bar chart
    bar_width = 0.8
    bar_color = 'skyblue'
    bar_edge_color = 'black'
    bar_alpha = 1.0
    axes.bar(x, y, color=bar_color, alpha=bar_alpha, label='Result',
             edgecolor=bar_edge_color, linewidth=1.2)

    # Plot a line chart with markers and custom color
    axes.plot(x, y, color='indianred', marker='o',
              linestyle='-', linewidth=2, markersize=6, label='Result Trend')

    # Add a threshold line if enabled
    if threshold_enabled:
        threshold_label = f'Threshold ({threshold_value})'
        axes.axhline(threshold_value, color='orange', linestyle='--', linewidth=2, label=threshold_label)

    axes.set_title("Student Performance", fontdict={
                   'fontsize': 16, 'fontweight': 'bold'})

    axes.legend(loc='center left', bbox_to_anchor=(0.9, 1.1))

    if len(data) >= 4:
        axes.set_xticklabels(x, rotation=45, ha='right')

    # Add major and minor grid lines
    axes.grid(True, which='major', color='gray', linewidth=0.8)

    # Set y-axis tick labels with a smaller step size
    axes.set_yticks(np.arange(0, max(y) + 10, 10))

    figure_canvas_agg.draw()


sg.theme('DarkTeal6')
table_content = []
layout = [
    [
        sg.Column(
            [
                [sg.Text('Unit Code:', font=('Helvetica', 12)), sg.Input(key='-UNITCODE-', size=(10, 1))],
                [sg.Text('Result:', font=('Helvetica', 12)), sg.Input(key='-RESULT-', size=(10, 1))],
                [sg.Button('Submit', button_color=('white', 'green'), font=('Helvetica', 12, 'bold')),
                 sg.Button('Delete', button_color=('white', 'red'), font=('Helvetica', 12, 'bold'))]
            ]
        ),
        sg.Column(
            [
                [sg.Table(
                    headings=['Unit Code', 'Result'],
                    values=table_content,
                    expand_x=True,
                    hide_vertical_scroll=True,
                    key='-TABLE-',
                    background_color='#f0f0f0',  # Light gray
                    text_color='black'  # Black text color
                )]
            ],
            expand_x=True
        )
    ],
    [sg.Canvas(key='-CANVAS-')],
    [sg.Checkbox('Enable Threshold', key='-ENABLE_THRESHOLD-', enable_events=True),
     sg.Text('Threshold:', font=('Helvetica', 12)),
     sg.Input(key='-THRESHOLD_VALUE-', size=(10, 1), default_text='49', enable_events=True)],
    [sg.Button('Export as PNG', button_color=('white', 'green'), size=(15, 1), font=('Helvetica', 12, 'bold'))]
]

window_layout = [
    [sg.Column(layout, size=(800, 600), scrollable=True, expand_x=True, expand_y=True)]
]

# Set the path to the favicon file
favicon_path = 'favicon/favicon.ico'

# Set the window icon
sg.SetOptions(icon=favicon_path)

window = sg.Window('Performance App', window_layout, finalize=True, resizable=True)

# matplotlib
fig = plt.figure(figsize=(13, 8))
fig.add_subplot(111).plot([], [])
figure_canvas_agg = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

threshold_enabled = False
threshold_value = 49

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'Submit':
        unit_code = values['-UNITCODE-']
        unit_code = unit_code.upper()
        result = values['-RESULT-']
        if result.isnumeric():
            result = min(100, float(result))  # Cap the result at 100
            table_content.append([unit_code, result])
            window['-TABLE-'].update(table_content)
            window['-UNITCODE-'].update('')
            window['-RESULT-'].update('')
            update_figure(table_content, threshold_value, threshold_enabled)

    if event == 'Export as PNG':
        filepath = sg.popup_get_file(
            'Save As', save_as=True, file_types=(("PNG Files", "*.png"),))
        if filepath:
            # Adjust the DPI setting for better quality
            fig.savefig(filepath, dpi=400)

    if event == 'Delete':
        selected_rows = window['-TABLE-'].SelectedRows
        if selected_rows:
            for row in selected_rows:
                del table_content[row]
            window['-TABLE-'].update(table_content)
            update_figure(table_content, threshold_value, threshold_enabled)

    if event == '-ENABLE_THRESHOLD-':
        threshold_enabled = values['-ENABLE_THRESHOLD-']
        update_figure(table_content, threshold_value, threshold_enabled)

    if event == '-THRESHOLD_VALUE-':
        threshold_value = float(values['-THRESHOLD_VALUE-']) if values['-THRESHOLD_VALUE-'].isnumeric() else None
        update_figure(table_content, threshold_value, threshold_enabled)

window.close()
