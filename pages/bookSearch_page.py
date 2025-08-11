import re
from playwright.sync_api import Page, expect

class BookSearch:
    def __init__(self, page:Page):
        self.page = page
        self.searchbox = page.get_by_role('combobox')
        self.shoppingTab = page.get_by_role('navigation').get_by_text('Shopping')
        self.allFiltersButton = page.get_by_role("button", name="All filters.")
        self.highPriceButton = page.get_by_title('Price: high to low')
        self.maxAmountInput = page.get_by_title('Max')
        self.goPriceButton = page.locator('div:has(input[aria-label*="price"]) button:has-text("Go")')
        self.productsWithRatings = page.locator('//g-inner-card[.//span[contains(@aria-label, "Rated")]]')
        self.secondRatingText = self.productsWithRatings.nth(1).locator('//span[contains(@aria-label, "Rated")]').first

    def searchBook(self, bookName: str):
        self.searchbox.fill('Book ' + bookName)
        self.page.keyboard.press('Enter')

    def clickShoppingTab(self):
        self.shoppingTab.click()
        self.page.wait_for_load_state('networkidle')

    def selectHighToLowPrice(self):
        self.allFiltersButton.click()
        self.highPriceButton.click()

    def completeMaxAmount(self, amount: str):
        self.maxAmountInput.fill(amount)
        self.goPriceButton.click()

    def verifySecondProductRating(self, minRating: float):
        assert self.productsWithRatings.count() >= 2

        aria_label = self.secondRatingText.get_attribute('aria-label')
        print(f"aria-label: {aria_label}") 
        match = re.search(r'Rated ([\d.]+) out of 5', aria_label)
        if match:
            ratingValue = float(match.group(1))
            print(f"Extracted rating: {ratingValue}")
        else:
            raise ValueError(f"Could not extract rating from aria-label: {aria_label}")

        assert ratingValue >= minRating, f"Expected rating >= {minRating}, but got {ratingValue}"
