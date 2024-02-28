"""Data Abstractions"""
from typing import List, Type


#############################
# Phase 1: Data Abstractions #
#############################
class Review:
    """A review for a restaurant, including the name of the restaurant, the
    number of stars given, and the name of the reviewer."""
    _restaurant_name: str
    _rating: float

    def __init__(self, restaurant_name: str, rating: float) -> None:
        """Return a Review abstraction."""
        self._restaurant_name = restaurant_name
        self._rating = rating

    def get_name(self) -> str:
        """Return the restaurant name of the `review`, which is a string."""
        return self._restaurant_name

    def get_rating(self) -> float:
        """Return the number of stars given by the `review`, which is a
        floating point number between 1.0 and 5.0."""
        return self._rating

    def __repr__(self):
        """Return a string representation of the review.
        This will be used anytime you print a Review object.
        The string representation should be in the following format:
        Review('<NAME>', <RATING>)
        >>> Review("A", 1.0)
        Review('A', 1.0)
        """
        return f"Review('{self._restaurant_name}', {self._rating:.1f})"


# Restaurants
class Restaurant:
    """A restaurant, with a name, a location, a list of categories, a price
    rating, and a list of reviews. You can decide on the names and attribute
    types."""

    def __init__(self, name: str, location: list[float], categories: list[str], price: int,
                 reviews: list[Review]) -> None:
        """Return a restaurant abstraction.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).get_name()
        'A'
        """
        self._name = name
        self._location = location
        self._categories = categories
        self._price = price
        self._reviews = reviews

    def get_name(self) -> str:
        """Return the name of the `restaurant`, which is a string.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).get_name()
        'A'
        """
        return self._name

    def get_location(self) -> list[float]:
        """Return the location of the `restaurant`, which is a list containing
        latitude and longitude.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).get_location()
        [1.0, 2.0]
        """
        return self._location

    def get_categories(self) -> list[str]:
        """Return the categories of the `restaurant`, which is a list of strings.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).get_categories()
        ['B', 'C']
        """
        return self._categories

    def get_price(self) -> int:
        """Return the price of the `restaurant`, which is a number.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).get_price()
        1
        """
        return self._price

    def get_reviews(self) -> list[Review]:
        """Return a list of reviews for `restaurant`.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).get_reviews()
        [Review('A', 1.0), Review('B', 2.0)]
        """
        return self._reviews

    def get_ratings(self) -> list[int]:
        """Return a list of ratings, which are numbers from 1 to 5, of the
        `restaurant` based on the reviews of the `restaurant`.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).get_ratings()
        [1, 2]
        """
        return [review.get_rating() for review in self._reviews]

    def restaurant_num_ratings(self) -> int:
        """Return the number of ratings for `restaurant`.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).restaurant_num_ratings()
        2
        """
        return len(self._reviews)

    def restaurant_mean_rating(self) -> float:
        """Return the average rating for `restaurant`.
        >>> Restaurant('A', [1.0, 2.0], ['B', 'C'], 1, [Review('A', 1), Review('B', 2)]).restaurant_mean_rating()
        1.5
        """
        return sum(r.get_rating() for r in self._reviews)/len(self._reviews)


class User:
    """A user, with a name and a list of reviews."""
    _name: str
    _reviews: list[Review]

    def __init__(self, name: str, reviews: list[Review]) -> None:
        self._name = name
        self._reviews = reviews

    def get_name(self) -> str:
        """Return the name of the `user`, which is a string."""
        return self._name

    def get_reviews(self) -> list[Review]:
        """Return a list of reviews for restaurants by the `user`."""
        return self._reviews

    def get_reviewed_restaurants(self, restaurants: list[Restaurant]) -> list[Restaurant]:
        """Return the subset of `restaurants` reviewed by `user`.
            Arguments:
            restaurants -- a list of restaurant abstractions
            """
        user_reviews = list(self.get_reviews())
        names = [r.get_name() for r in user_reviews]
        return [r for r in restaurants if r.get_name() in names]

    def user_rating(self, restaurant_name) -> float:
        """Return the rating given for `restaurant_name` by a `user`."""
        user_reviews = self.get_reviews()
        names = [r.get_name() for r in user_reviews]
        return user_reviews[names.index(restaurant_name)].get_rating()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
