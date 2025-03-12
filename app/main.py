from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import uvicorn
from typing import List
import asyncio

from app.database import get_db, engine, Base
from app.schemas import ProjectCreate, ProjectResponse, TaskResponse
from app.models import Project, Task
from app.services import get_project_tasks

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запущено!")
    yield
    print("Приложение завершает работу.")

app = FastAPI(lifespan=lifespan)


@app.post("/projects/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        print(f"Received project request: {project.project_name} in {project.location}")
        
        # Create a new project in the database
        db_project = Project(
            project_name=project.project_name,
            location=project.location,
            status="processing"
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        print(f"Project created with ID: {db_project.id}")
        
        # Generate tasks using Gemini API
        print("Calling Gemini API...")
        tasks = await get_project_tasks(project.project_name, project.location)
        print(f"Received {len(tasks)} tasks from Gemini API")
        
        # Add tasks to the database
        for task_data in tasks:
            db_task = Task(
                project_id=db_project.id,
                name=task_data["name"],
                status=task_data["status"]
            )
            db.add(db_task)
        
        db.commit()
        print("Tasks committed to database")
        
        # Update project status
        db_project.status = "in_progress"
        db.commit()
        print("Project status updated to in_progress")
        
        # Return the created project with tasks
        response = get_project_response(db_project, db)
        print(f"Returning response with {len(response.tasks)} tasks")
        return response
    except Exception as e:
        print(f"ERROR in create_project: {str(e)}")
        raise




@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    # Retrieve the project
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return get_project_response(db_project, db)

def get_project_response(db_project: Project, db: Session) -> ProjectResponse:
    # Get tasks for the project
    tasks = db.query(Task).filter(Task.project_id == db_project.id).all()
    task_responses = [
        TaskResponse(name=task.name, status=task.status) 
        for task in tasks
    ]
    
    # Create ProjectResponse
    return ProjectResponse(
        id=db_project.id,
        project_name=db_project.project_name,
        location=db_project.location,
        status=db_project.status,
        tasks=task_responses
    )
 

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)