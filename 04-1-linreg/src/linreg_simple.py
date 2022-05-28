import random
import matplotlib.pyplot as plt


def linear_regression(x, y):
    n = len(x)
    slope_upper_sum = 0.0
    slope_lower_sum = 0.0
    x_avg = sum(x) / float(n)
    y_avg = sum(y) / float(n)
    # Calculating slope
    for xi, yi in zip(x, y):
        slope_upper_sum += (xi - x_avg) * (yi - y_avg)
        slope_lower_sum += (xi - x_avg)**2

    slope = slope_upper_sum / slope_lower_sum
    # Calculating intercept
    intercept_sum = 0.0
    for xi, yi in zip(x, y):
        intercept_sum += yi - slope * xi

    intercept = intercept_sum / n  # tacka preseka na y-osi

    return slope, intercept


def predict(x, slope, intercept):
    return intercept + x * slope


def create_line(x, slope, intercept):
    y = [predict(xx, slope, intercept) for xx in x]
    return y


if __name__ == '__main__':
    x = range(50)  # celobrojni interval [0,50]
    random.seed(1337)  # da rezultati mogu da se reprodukuju
    y = [(i + random.randint(-5, 5)) for i in x]  # y = x (+- nasumicni sum)

    slope, intercept = linear_regression(x, y)

    line_y = create_line(x, slope, intercept)

    plt.plot(x, y, '.')
    plt.plot(x, line_y, 'b')
    plt.title('Slope: {0}, intercept: {1}'.format(slope, intercept))
    plt.show()
