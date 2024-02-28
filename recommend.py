from data import ALL_RESTAURANTS

from abstractions import *


##################################
# Phase 2: Supervised Learning! #
##################################
class LinearRegression:
    """A linear regression model to predict ratings
    a user might give to a restaurant."""

    def __init__(self) -> None:
        """Return a LinearRegression abstraction."""
        self.a = 0  # intercept of regression line
        self.b = 0  # slope of regression line
        self.xs = []  # x values used to train model
        self.ys = []  # y values used to train model
        self.r_squared = 0  # r-squared value of model (how well it fits the training data)

    def predict(self, restaurant: Restaurant) -> float:
        """Use the parameters of the regression model to predict a rating for
        `restaurant`.

        Arguments:
        restaurant -- A restaurant abstraction

        A linear regression model is a function from restaurants to ratings.
        It can be calculated using the formula:
        y = b * x + a
        where x is the mean rating of the restaurant, y is the predicted rating,
        a is the intercept of the model, and b is the slope of the model.

        >>> restaurant = Restaurant('New', [-10, 2], [], 2, [Review('New', 4)])
        >>> r = LinearRegression()
        >>> r.a = 1
        >>> r.b = 2
        >>> round(r.predict(restaurant), 1)
        9.0
        """
        return restaurant_mean_rating(restaurant) * self.b + self.a

    def train(self, user: User, restaurants: list[Restaurant]) -> None:
        """Train a rating predictor (a function mapping restaurants onto ratings),
        for `user` by performing least-squares linear regression using `restaurant_mean_rating`
        on the items in `restaurants`. Save the R^2 value and the parameters of this model
        as attributes of `self`.

        Arguments:
        user -- A user
        restaurants -- A sequence of restaurants
        >>> user = User('John D.', [Review('A', 1), Review('B', 5), Review('C', 2), Review('D', 2.5)])
        >>> restaurant = Restaurant('New', [-10, 2], [], 2, [Review('New', 4)])
        >>> cluster = [Restaurant('B', [4, 2], [], 1, [Review('B', 5)]),Restaurant('C', [-2, 6], [], 4, [Review('C', 2)]),Restaurant('D', [4, 2], [], 3.5, [Review('D', 2.5),Review('D', 3)])]
        >>> r = LinearRegression()
        >>> r.train(user, cluster)
        >>> print(round(r.predict(restaurant), 0))
        4.0
        >>> print(round(r.r_squared, 0))
        1.0
        """
        self.xs = [restaurant.restaurant_mean_rating() for restaurant in restaurants]
        self.ys = [user.user_rating(restaurant.get_name) for restaurant in restaurants]

        x_mean = sum(self.xs) / len(self.xs)
        y_mean = sum(self.ys) / len(self.ys)

        Sxx = sum((x - x_mean)**2 for x in self.xs)
        Syy = sum((y - y_mean)**2 for y in self.ys)
        Sxy = sum((x - x_mean) * (y - y_mean) for x,y in zip(self.xs, self.ys))

        self.b = Sxy/Sxx
        self.a = y_mean - (self.b*x_mean)
        r2 = (Sxy**2)/(Sxx*Syy)


    def rate_all(self, user: User, restaurants: list[Restaurant]) -> dict[Restaurant, float]:
        """Return the predicted ratings of `restaurants` by `user`.  Note
        that this method can only be called after `train` has been called.
        You will have to train the predictor using the restaurants in
        the user has reviewed in the past; you will then use that model
        to predict the user's ratings for restaurants they have not
        reviewed.

        Arguments:
        user -- A user
        restaurants -- A list of restaurants to be reviewed
        >>> user = User('Mr. Mean Rating Minus One', [Review('Cafe 3', 1.0),Review('Jasmine Thai', 2.0),Review('Fondue Fred', 2.0)])
        >>> to_rate = ALL_RESTAURANTS[:6]
        >>> c = LinearRegression()
        >>> print([round(r.restaurant_mean_rating(),0) for r in ALL_RESTAURANTS[:6]])
        [2.0, 3.0, 3.0, 2.0, 3.0, 4.0]
        >>> print([round(n,0) for n in list(c.rate_all(user, to_rate).values())])
        [1.0, 2.0, 2.0, 1.0, 2.0, 3.0]
        """
        predicted_ratings = {}

        for restaurant in restaurants:
            try:
                rating = user.user_rating(restaurant.get_name())
            except:
                rating = self.predict(restaurant)

            predicted_ratings[restaurant.get_name()] = rating

        return predicted_ratings




if __name__ == "__main__":
    import doctest
    doctest.testmod()
