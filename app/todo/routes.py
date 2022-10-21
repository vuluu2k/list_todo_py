import pprint
from fastapi import Body, Request, HTTPException, status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import TaskModel, UpdateTaskModel
from app.auth.jwt_bearer import JwtBearer

router = APIRouter()


@router.post("/", dependencies=[Depends(JwtBearer())], response_description="Add new task")
async def create_task(request: Request, task: TaskModel = Body(...)):
    task = jsonable_encoder(task)
    new_task = await request.app.mongodb["tasks"].insert_one(task)
    created_task = await request.app.mongodb["tasks"].find_one(
        {"_id": new_task.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"new_task": created_task, "message": "create task successfully"})


@router.get("/", response_description="List all tasks")
async def list_tasks(request: Request):
    tasks = []
    for doc in await request.app.mongodb["tasks"].find().to_list(length=100):
        tasks.append(doc)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"tasks": tasks, "message": "load tasks successfully"})


@router.get("/{id}", response_description="get task with id")
async def get_task(id: str, request: Request):
    task = await request.app.mongodb["tasks"].find_one({"_id": id})
    if task:
        return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.patch("/{id}", response_description="edit task with id and params")
async def edit_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
    task = {key: value for key, value in task.dict().items() if value is not None}

    if len(task) >= 1:
        edit_task_result = await request.app.mongodb["tasks"].update_one({"_id": id}, {"$set": jsonable_encoder(task)})
        if edit_task_result.modified_count == 1:
            if (update_task := await request.app.mongodb["tasks"].find_one({"_id": id})) is not None:
                return update_task
    if (existing_task := await request.app.mongodb["tasks"].find_one({"_id": id})) is not None:
        return existing_task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", response_description="delete task with id")
async def delete_task(id: str, request: Request):
    delete_task_result = await request.app.mongodb["tasks"].delete_one({"_id": id})
    if delete_task_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": id, "message": f"delete {id} successfully"})

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
