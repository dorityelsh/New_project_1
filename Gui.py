import pysimplegui as sg
import anomaly as af

layout = [
    [sg.Text("Anomaly Detection in Financial Data", size=(30, 1), font=("Helvetica", 25))],
    [sg.Text("Choose Anomaly Detection Method:")],
    [sg.Radio("Robust Z-Score", "RADIO1", key="-ZSCORE-"), sg.Radio("Isolation Forest", "RADIO1", key="-ISOLATION-")],
    [sg.Button("Run"), sg.Button("Exit")]
]   

window = sg.Window("Anomaly Detection GUI", layout)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    if event == "Run":
        if values["-ZSCORE-"]:
            af.choose_method(method='robust_z_score')
            af.check_anomalies(af.df)
        elif values["-ISOLATION-"]:
            af.choose_method(method='isolation_forest')
            af.check_anomalies(af.df)
        else:
            sg.popup("Please select a method.")
window.close()

