import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def analyze_motion(filename: str, distance_m: float = 20.0):
    if filename.endswith('.csv'):
        df = pd.read_csv(filename)
    else:
        df = pd.read_excel(filename)

    #нормализация столбцов
    df.columns = [col.strip().lower() for col in df.columns]
    time = df["time (s)"]
    accel = df["absolute acceleration (m/s^2)"]

    accel_smooth = pd.Series(accel).rolling(window=5, center=True).mean().fillna(method='bfill').fillna(method='ffill')

    #Поиск пиков ускорения
    # высота пика > 11 м/с
    peaks, _ = find_peaks(accel_smooth, height=11, distance=10)
    steps = len(peaks)

    #Расчёт длительности и средней скорости
    duration = time.iloc[-1] - time.iloc[0]
    avg_speed = distance_m / duration

    #Результаты 
    print(f"Количество шагов: {steps}")
    print(f"Длительность записи: {duration:.2f} с")
    print(f"Средняя скорость: {avg_speed:.2f} м/с")

    return steps, avg_speed, duration


if __name__ == "__main__":
    steps, speed, duration = analyze_motion("DATA.xls", distance_m=20.0)
