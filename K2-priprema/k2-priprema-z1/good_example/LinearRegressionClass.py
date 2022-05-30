class LinearRegression:
    def __init__(self):
        self.intercept_ = 0.0
        self.slope_ = 0.0

    def fit(self, X, y):
        n = len(X)
        slope_upper_sum = 0.0
        slope_lower_sum = 0.0
        x_avg = sum(X) / float(n)
        y_avg = sum(y) / float(n)
        # Calculating slope
        for xi, yi in zip(X, y):
            slope_upper_sum += (xi - x_avg) * (yi - y_avg)
            slope_lower_sum += (xi - x_avg)**2

        self.slope_ = slope_upper_sum / slope_lower_sum
        # Calculating intercept
        intercept_sum = 0.0
        for xi, yi in zip(X, y):
            intercept_sum += yi - self.slope_ * xi

        self.intercept_ = intercept_sum / n  # tacka preseka na y-osi

        return self

    def predict(self, x):
        return self.intercept_ + x * self.slope_

    def create_line(self, x):
        y = [self.predict(xx) for xx in x]
        return y

