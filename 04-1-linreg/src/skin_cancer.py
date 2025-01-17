import matplotlib.pyplot as plt
from linreg_simple import linear_regression, create_line

if __name__ == '__main__':
    mort = []
    lat = []

    with open('../data/skincancer.csv', 'r') as file:
        for line in file:
            data = line.split(',')
            try:
                mort.append(float(data[2]))
                lat.append(float(data[1]))
            except:
                pass
    slope, intercept = linear_regression(lat, mort)
    line_mort = create_line(lat, slope, intercept)

    plt.plot(lat, mort, '.')
    plt.plot(lat, line_mort, 'b')
    plt.title('Slope {0}, intercept {1}'.format(slope, intercept))
    plt.show()