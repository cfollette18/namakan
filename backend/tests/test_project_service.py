import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


@pytest.mark.asyncio
async def test_project_service_list_projects():
    """Test listing projects for a user"""
    from app.services.project_service import ProjectService

    service = ProjectService()

    with patch("app.services.project_service.ProjectModel") as MockProject:
        mock_project = MagicMock()
        mock_project.id = "project-1"
        mock_project.name = "Test Project"
        mock_project.description = "A test project"
        mock_project.status = "active"
        mock_project.complexity = "medium"
        mock_project.user_id = "user-1"
        mock_project.created_at = datetime.now()
        mock_project.updated_at = datetime.now()

        MockProject.find_many = AsyncMock(return_value=[mock_project])

        result = await service.list_projects("user-1")

        assert len(result) == 1
        assert result[0].name == "Test Project"
        assert result[0].user_id == "user-1"


@pytest.mark.asyncio
async def test_project_service_get_project():
    """Test getting a single project"""
    from app.services.project_service import ProjectService

    service = ProjectService()

    with patch("app.services.project_service.ProjectModel") as MockProject:
        mock_project = MagicMock()
        mock_project.id = "project-1"
        mock_project.name = "Test Project"
        mock_project.description = "A test project"
        mock_project.status = "active"
        mock_project.complexity = "medium"
        mock_project.user_id = "user-1"
        mock_project.created_at = datetime.now()
        mock_project.updated_at = datetime.now()

        MockProject.find_first = AsyncMock(return_value=mock_project)

        result = await service.get_project("project-1")

        assert result is not None
        assert result.id == "project-1"
        assert result.name == "Test Project"


@pytest.mark.asyncio
async def test_project_service_get_project_not_found():
    """Test getting a non-existent project returns None"""
    from app.services.project_service import ProjectService

    service = ProjectService()

    with patch("app.services.project_service.ProjectModel") as MockProject:
        MockProject.find_first = AsyncMock(return_value=None)

        result = await service.get_project("non-existent")

        assert result is None


@pytest.mark.asyncio
async def test_project_service_start_project():
    """Test starting a project"""
    from app.services.project_service import ProjectService

    service = ProjectService()

    with patch("app.services.project_service.ProjectModel") as MockProject:
        MockProject.update = AsyncMock(return_value=MagicMock())

        await service.start_project("project-1")

        MockProject.update.assert_called_once_with(
            where={"id": "project-1"},
            data={"status": "in_progress"}
        )


@pytest.mark.asyncio
async def test_project_service_cancel_project():
    """Test cancelling a project"""
    from app.services.project_service import ProjectService

    service = ProjectService()

    with patch("app.services.project_service.ProjectModel") as MockProject:
        MockProject.update = AsyncMock(return_value=MagicMock())

        await service.cancel_project("project-1")

        MockProject.update.assert_called_once_with(
            where={"id": "project-1"},
            data={"status": "cancelled"}
        )


@pytest.mark.asyncio
async def test_project_service_create_saves_to_db():
    """Test that create_project saves project to database"""
    from app.services.project_service import ProjectService
    from app.models.project import ProjectCreate

    service = ProjectService()

    with patch("app.services.project_service.ProjectModel") as MockProject:
        MockProject.create = AsyncMock(return_value=MagicMock())

        project = ProjectCreate(
            name="New Project",
            description="A new project description",
            user_id="user-1"
        )

        result = await service.create_project(project)

        MockProject.create.assert_called_once()
        # Verify the project was created with correct fields
        call_args = MockProject.create.call_args
        assert call_args[1]["name"] == "New Project"
        assert call_args[1]["user_id"] == "user-1"