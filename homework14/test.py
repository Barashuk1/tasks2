from fastapi.testclient import TestClient
from main import get_user_by_email
import unittest
from unittest.mock import MagicMock

import pytest
from main import app

class TestUserFunctions(unittest.TestCase):

    def test_get_user_by_email(self):
        # Створюємо фіктивну сесію бази даних
        fake_session = MagicMock()
        # Передаємо фіктивну сесію та електронну пошту
        user = get_user_by_email(fake_session, "test@example.com")
        # Перевіряємо, чи функція повертає користувача або None
        self.assertIsNotNone(user)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_get_contacts(client):
    response = client.get("/contacts/")
    assert response.status_code == 200
    # Перевірка вмісту відповіді, наприклад:
    assert response.json() == [{"id": 1, "name": "John Doe"}]