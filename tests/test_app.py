import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import Project, Task
from app.schemas import ProjectCreate, TaskResponse


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)  
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)  


@pytest.fixture(scope="module")
def mock_get_project_tasks():

    with patch("app.services.get_project_tasks") as mock:
        mock.return_value = [
            {"name": "Task 1", "status": "pending"},
            {"name": "Task 2", "status": "pending"},
        ]
        yield mock


@pytest.fixture
def create_project_data():
    return ProjectCreate(project_name="New Project", location="New Location")


def test_create_project(client, mock_get_project_tasks, create_project_data):
    response = client.post("/projects/", json=create_project_data.dict())

    assert response.status_code == 200
    project = response.json()
    assert project["project_name"] == "New Project"
    assert project["location"] == "New Location"
    assert len(project["tasks"]) == 5
    assert project["tasks"][0]["name"] == "Task 1"
    assert project["tasks"][1]["name"] == "Task 2"


def test_get_project(client, mock_get_project_tasks, create_project_data):

    create_response = client.post("/projects/", json=create_project_data.dict())
    project_id = create_response.json()["id"]


    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 200
    project = response.json()
    assert project["id"] == project_id
    assert project["project_name"] == "New Project"
    assert project["location"] == "New Location"
    assert len(project["tasks"]) == 5


def test_default_tasks_on_api_failure(client, create_project_data):

    with patch("app.services.get_project_tasks") as mock:
        mock.side_effect = Exception("API failure")

        response = client.post("/projects/", json=create_project_data.dict())

    assert response.status_code == 200
    project = response.json()
    assert len(project["tasks"]) == 5  
    assert project["tasks"][0]["name"] == "Find suitable location"
    assert project["tasks"][4]["name"] == "Begin construction"
