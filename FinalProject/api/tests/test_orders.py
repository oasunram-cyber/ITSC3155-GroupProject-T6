<<<<<<< HEAD
from fastapi.testclient import TestClient
from controllers import orders as controller
from main import app
import pytest
from models import orders as model

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }

    order_object = model.Order(**order_data)

    created_order = controller.create(db_session, order_object)

    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"
=======
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest

from main import app
from controllers import orders as controller
from schemas import orders as schema

# Create a test client for the app (you can use this later for endpoint tests)
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    """
    Mocked DB session with the minimum methods used by the controller.
    """
    db = mocker.Mock()
    db.add = MagicMock()
    db.commit = MagicMock()
    db.refresh = MagicMock()
    db.query = MagicMock()
    return db


def test_create_order(db_session):
    """
    Test creating an order via the orders controller.
    Uses the OrderCreate schema (not the SQLAlchemy model directly).
    """
    order_request = schema.OrderCreate(
        customer_name="John Doe",
        phone_number="1234567890",
        address="123 Test St",
        description="Test order",
        total_price=0,  # will be updated as order_details are added
        order_status=schema.OrderStatus.PENDING,
        tracking_number="TRACK123",
    )

    created_order = controller.create(db_session, order_request)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"
    assert created_order.tracking_number == "TRACK123"
>>>>>>> cf68c60 (feat: implement orders, order details, payments + fix models and db relationships)
