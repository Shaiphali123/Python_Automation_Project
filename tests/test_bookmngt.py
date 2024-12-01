import pytest
from unittest.mock import MagicMock
from fastapi.exceptions import HTTPException
from app.database import Book
from app.bookmgmt import create_book, update_book, delete_book, get_book_by_id, get_all_books

@pytest.fixture
def mock_db():
    """Fixture to mock the database session."""
    return MagicMock()

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_create_book(mock_db):
    """Test creating a book."""
    book_data = Book(
        id=1, name="Test Book", author="Test Author", published_year=2024, book_summary="Test summary"
    )

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = book_data

    response = await create_book(book=book_data, db=mock_db)  # Await the asynchronous function

    assert response == book_data
    mock_db.add.assert_called_once_with(book_data)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(book_data)

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_update_book(mock_db):
    """Test updating a book."""
    book_id = 1
    existing_book = Book(
        id=book_id, name="Old Book", author="Old Author", published_year=2020, book_summary="Old summary"
    )
    updated_data = Book(
        id=book_id, name="Updated Book", author="Updated Author", published_year=2024, book_summary="Updated summary"
    )

    mock_db.query().filter().first.return_value = existing_book

    response = await update_book(book_id=book_id, update_data=updated_data, db=mock_db)  # Await the asynchronous function

    assert response.name == updated_data.name
    assert response.author == updated_data.author
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(existing_book)

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_update_book_not_found(mock_db):
    """Test updating a non-existing book."""
    book_id = 1
    updated_data = Book(
        id=book_id, name="Updated Book", author="Updated Author", published_year=2024, book_summary="Updated summary"
    )

    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        await update_book(book_id=book_id, update_data=updated_data, db=mock_db)  # Await the asynchronous function

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_delete_book(mock_db):
    """Test deleting a book."""
    book_id = 1
    existing_book = Book(
        id=book_id, name="Test Book", author="Test Author", published_year=2024, book_summary="Test summary"
    )

    mock_db.query().filter().first.return_value = existing_book

    response = await delete_book(book_id=book_id, db=mock_db)  # Await the asynchronous function

    assert response["message"] == "Book deleted successfully"
    mock_db.delete.assert_called_once_with(existing_book)
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_delete_book_not_found(mock_db):
    """Test deleting a non-existing book."""
    book_id = 1
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        await delete_book(book_id=book_id, db=mock_db)  # Await the asynchronous function

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_get_book_by_id(mock_db):
    """Test getting a book by ID."""
    book_id = 1
    existing_book = Book(
        id=book_id, name="Test Book", author="Test Author", published_year=2024, book_summary="Test summary"
    )

    mock_db.query().filter().first.return_value = existing_book

    response = await get_book_by_id(book_id=book_id, db=mock_db)  # Await the asynchronous function

    assert response == existing_book
    mock_db.query().filter().first.assert_called_once()

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_get_book_by_id_not_found(mock_db):
    """Test getting a non-existing book by ID."""
    book_id = 1
    mock_db.query().filter().first.return_value = None

    with pytest.raises(HTTPException) as excinfo:
        await get_book_by_id(book_id=book_id, db=mock_db)  # Await the asynchronous function

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"

@pytest.mark.asyncio  # Marks the test as asynchronous
async def test_get_all_books(mock_db):
    """Test getting all books."""
    books = [
        Book(id=1, name="Book 1", author="Author 1", published_year=2020, book_summary="Summary 1"),
        Book(id=2, name="Book 2", author="Author 2", published_year=2021, book_summary="Summary 2"),
    ]

    mock_db.query().all.return_value = books

    response = await get_all_books(db=mock_db)  # Await the asynchronous function

    assert response == books
    mock_db.query().all.assert_called_once()
