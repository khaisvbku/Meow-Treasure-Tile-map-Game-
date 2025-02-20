import numpy as np
import pandas as pd

def generate_table(f, x_vals, y_vals):
    """Tạo bảng giá trị số của hàm f(x, y) tại các điểm gần (0,0)."""
    data = []
    for x in x_vals:
        row = [f(x, y) for y in y_vals]
        data.append(row)

    df = pd.DataFrame(data, index=x_vals, columns=y_vals)
    return df

# Định nghĩa hàm cần kiểm tra
def f(x, y):
    return (x**2 * y**3 + x**3 * y**2 - 5) / (2 - x*y)

# Các giá trị x, y gần 0
x_values = [-0.1, -0.01, 0, 0.01, 0.1]
y_values = [-0.1, -0.01, 0, 0.01, 0.1]

# Tạo bảng giá trị số
table = generate_table(f, x_values, y_values)
print(table)
