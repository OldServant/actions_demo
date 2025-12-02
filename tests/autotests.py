import unittest
from src.library import Book, PrintedBook, EBook, User, Librarian, Library


class TestBook(unittest.TestCase):
    def test_book_initial_state(self):
        book = Book("Война и мир", "Толстой", 1869)
        self.assertEqual(book.get_title(), "Война и мир")
        self.assertEqual(book.get_author(), "Толстой")
        self.assertEqual(book.get_year(), 1869)
        self.assertTrue(book.is_available())

    def test_book_mark_taken_and_returned(self):
        book = Book("Тест", "Автор", 2000)
        book.mark_as_taken()
        self.assertFalse(book.is_available())
        book.mark_as_returned()
        self.assertTrue(book.is_available())


class TestPrintedBook(unittest.TestCase):
    def test_repair_changes_condition(self):
        book = PrintedBook("Тест", "Автор", 2000, 100, "плохая")
        book.repair()
        self.assertEqual(book.condition, "хорошая")
        book.repair()
        self.assertEqual(book.condition, "новая")


class TestEBook(unittest.TestCase):
    def test_download_does_not_change_availability(self):
        book = EBook("Тест", "Автор", 2000, 10, "pdf")
        self.assertTrue(book.is_available())
        book.download()
        self.assertTrue(book.is_available())


class TestUserAndLibrary(unittest.TestCase):
    def setUp(self):
        self.lib = Library()
        self.book = PrintedBook("Война и мир", "Толстой", 1869,
                                1225, "хорошая")
        self.user = User("Анна")
        self.librarian = Librarian("Мария")
        self.librarian.add_book(self.lib, self.book)
        self.librarian.register_user(self.lib, self.user)

    def test_lend_and_return_book(self):
        self.lib.lend_book("Война и мир", "Анна")
        self.assertIn(self.book, self.user.get_borrowed_books())
        self.assertFalse(self.book.is_available())

        self.lib.return_book("Война и мир", "Анна")
        self.assertNotIn(self.book, self.user.get_borrowed_books())
        self.assertTrue(self.book.is_available())

    def test_show_available_books(self):
        # до выдачи книга доступна
        available = self.lib.show_available_books()
        self.assertIn(self.book, available)

        # после выдачи исчезает из доступных
        self.lib.lend_book("Война и мир", "Анна")
        available = self.lib.show_available_books()
        self.assertNotIn(self.book, available)

    def test_find_book(self):
        found = self.lib.find_book("Война и мир")
        self.assertIs(found, self.book)
        not_found = self.lib.find_book("Несуществующая")
        self.assertIsNone(not_found)


if __name__ == "__main__":
    unittest.main()
