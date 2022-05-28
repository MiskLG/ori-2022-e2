import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

if __name__ == '__main__':
    data_x = []
    data_y = []

    with open('../data/iq.tsv', 'r') as file:
        for line in file:
            try:
                row = [float(num) for num in line.split()]
                data_x.append(row[1:])
                data_y.append(row[0])
            except:
                pass
    lr = LinearRegression().fit(data_x, data_y)
    print(lr.coef_)
    print(lr.intercept_)