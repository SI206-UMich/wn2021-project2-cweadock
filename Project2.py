from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    titles_from_search = []
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, filename)) as f:
        soup = BeautifulSoup(f, 'html.parser')
        books = soup.find_all('tr', itemtype = "http://schema.org/Book")
        for book in books:
            title_find = book.find('span', itemprop = 'name')
            title = title_find.text
            author_find = book.find('span',itemprop = 'author')
            author = author_find.text.strip()
            #tup = tuple(title, author)
            titles_from_search.append(author)
    return titles_from_search

        # #can't figure this out
        # books = soup.find_all('td', )
        # titles = soup.find_all('a', class_ = 'bookTitle')
        # #authors = soup.find_all('a', class_ = 'authorName')
        # for title in titles:
        #     title = title.text.strip()
        #     author = 
        
        
        # #for author in authors:
        #     #authors_lst.append(author.text.strip())

        # return list(zip(titles_lst, authors_lst))


#TESTED, WORKS
def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    ???https://www.goodreads.com/book/show/kdkd".

    """
    response = requests.get('https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc')
    if response.ok:
        urls = []
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('a', class_ = 'bookTitle')
        for i in books:
            url = i.get('href', None)
            urls.append('https://www.goodreads.com' + url)
    return urls[0:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    response = requests.get(book_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find(id = 'bookTitle').text.strip()
        author = soup.find('a', class_= 'authorName').text.strip()
        pages = int((soup.find('span', itemprop = 'numberOfPages').text.strip()).split(' ')[0])
        summary = (title, author, pages)
    return summary


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    summary = []
    with open(filepath, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        books = soup.find_all('div', class_ = 'category clearFix')
        for i in books:
            category = i.h4.text.strip()
            titlecontainer = i.find('div', class_ = 'category__winnerImageContainer')
            img = titlecontainer.find('img', alt = True)
            title = img['alt']
            url = i.find('a').get('href')
            book_tuple = (category, title, url)
            summary.append(book_tuple)
    return summary


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    dir = os.path.dirname(__file__)
    outfile = open(os.path.join(dir, filename), "w")
    writer = csv.writer(outfile, delimiter = ',')
    writer.writerow(['Book title', 'Author Name'])
    for i in data:
        writer.writerow([i[0], i[1]])
    outfile.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results('search_results.htm')
        print(titles)
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)
        # check that the variable you saved after calling the function is a list
        self.assertTrue(type(titles) is list)
        # check that each item in the list is a tuple
        #self.assertEqual(type(title[0]) is tuple)
        #self.assertEqual(type(title[-1]) is tuple)
        for i in titles:
            self.assertTrue(type(i) is tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))

    # def test_get_search_links(self):
    #     # check that TestCases.search_urls is a list
    #     self.assertTrue(type(TestCases.search_urls) is list)

    #     # check that the length of TestCases.search_urls is correct (10 URLs)
    #     self.assertEqual(len(TestCases.search_urls), 10)

    #     # check that each URL in the TestCases.search_urls is a string
    #     for i in TestCases.search_urls:
    #         self.assertTrue(type(i) is str)
    #     # check that each URL contains the correct url for Goodreads.com followed by /book/show/
    #     for i in TestCases.search_urls:
    #         self.assertTrue('https://www.goodreads.com/book/show/' in i)
            

    # def test_get_book_summary(self):
    #     # create a local variable ??? summaries ??? a list containing the results from get_book_summary()
    #     # for each URL in TestCases.search_urls (should be a list of tuples)
    #     summaries = []
    #     for i in TestCases.search_urls:
    #         summaries.append(get_book_summary(i))
    #     # check that the number of book summaries is correct (10)
    #     self.assertEqual(len(summaries), 10)
    #     # check that each item in the list is a tuple
    #     for i in summaries:
    #         self.assertTrue(type(i) is tuple)
    #         # check that each tuple has 3 elements
    #         self.assertTrue(len(i), 3)
    #         # check that the first two elements in the tuple are string
    #         self.assertTrue(type(i[0]) is str)
    #         self.assertTrue(type(i[1]) is str)
    #         # check that the third element in the tuple, i.e. pages is an int
    #         self.assertTrue(type(i[2]) is int)
    #     # check that the first book in the search has 337 pages
    #     self.assertEqual(summaries[0][2], 337)
            


    # def test_summarize_best_books(self):
    #     # call summarize_best_books and save it to a variable
    #     summary = summarize_best_books('best_books_2020.htm')
    #     #list of tuples

    #     # check that we have the right number of best books (20)
    #     self.assertEqual(len(summary), 20)
    #     # assert each item in the list of best books is a tuple
    #     for i in summary:
    #         self.assertTrue(type(i) is tuple)
    #         # check that each tuple has a length of 3
    #         self.assertEqual(len(i), 3)
    #     # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
    #     self.assertEqual(summary[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
    #     # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
    #     self.assertEqual(summary[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))



    # def test_write_csv(self):
    #     # call get_titles_from_search_results on search_results.htm and save the result to a variable
    #     search_results = get_titles_from_search_results('search_results.htm')
    #     # call write csv on the variable you saved and 'test.csv'
    #     write_csv(search_results, 'test.csv')
    #     # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
    #     f = open('test.csv')
    #     csv_lines = f.readlines()

    #     # check that there are 21 lines in the csv
    #     self.assertEqual(len(csv_lines), 21)
    #     # check that the header row is correct
    #     self.assertEqual(csv_lines[0], 'Book title,Author Name')
    #     # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
    #     self.assertEqual(csv_lines[1], 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling')
    #     # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
    #     self.assertEqual(csv_lines[-1], 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling')


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



