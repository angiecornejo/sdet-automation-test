import allure
import pytest

@allure.story("Book Search")
@allure.title("Verify product rating")
@pytest.mark.parametrize(
    'bookname,amount,rating',
    [
        ('Harry potter', '500', 4.9),
        ('Game of thrones', '75', 3)
    ],
)
def test_search_book(google_setup,bookname,amount,rating):
    """
    Test the search functionality of books on Google Shopping
    """
    google_book_search = google_setup 
    google_book_search.searchBook(bookname)
    google_book_search.clickShoppingTab()
    google_book_search.selectHighToLowPrice()
    google_book_search.completeMaxAmount(amount)
    google_book_search.verifySecondProductRating(rating)
        