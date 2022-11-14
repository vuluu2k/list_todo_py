import pprint
from fastapi import Body, Request, HTTPException, status, APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import TaskModel, UpdateTaskModel, GroupTaskModel
from app.auth.jwt_bearer import JwtBearer
from app.auth.jwt_handler import get_user

router = APIRouter()


@router.post("/group", dependencies=[Depends(JwtBearer())], response_description="Add new group task")
async def create_group(request: Request, group_task: GroupTaskModel = Body(...)):
    decoded_user = get_user(request)
    user_id = decoded_user["userID"]

    group_task = jsonable_encoder(group_task)
    group_task["user_id"] = user_id

    new_group_task = await request.app.mongodb["groups"].insert_one(group_task)
    created_group_task = await request.app.mongodb["groups"].find_one(
        {"_id": new_group_task.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"new_group": created_group_task, "message": "create group successfully"})


@router.get("/group", dependencies=[Depends(JwtBearer())], response_description="Get groups task")
async def get_group(request: Request):
    decoded_user = get_user(request)
    user_id = decoded_user["userID"]

    groups = await request.app.mongodb["groups"].find({"user_id": user_id}).to_list(length=20)

    if groups is not None:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Lấy dữ liệu thành công", "success": True, "groups": groups})

    raise HTTPException(status_code=404, detail=f"Group {user_id} not found")


@router.post("/", dependencies=[Depends(JwtBearer())], response_description="Add new task")
async def create_task(request: Request, task: TaskModel = Body(...)):
    decoded_user = get_user(request)
    user_id = decoded_user["userID"]

    task = jsonable_encoder(task)
    task["user_id"] = user_id
    new_task = await request.app.mongodb["tasks"].insert_one(task)
    created_task = await request.app.mongodb["tasks"].find_one(
        {"_id": new_task.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"new_task": created_task, "message": "create task successfully"})


@router.get("/{group_id}", dependencies=[Depends(JwtBearer())], response_description="List all tasks")
async def list_tasks(group_id: str, request: Request):
    decoded_user = get_user(request)
    user_id = decoded_user["userID"]

    tasks_with_user_id_and_groups = await request.app.mongodb["tasks"].find(
        {"$and": [{"user_id": user_id}, {"group_id": group_id}]}).to_list(length=100)

    if tasks_with_user_id_and_groups is not None:
        group_name = await request.app.mongodb["groups"].find_one({"_id": group_id})
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"tasks": tasks_with_user_id_and_groups, "message": "load tasks successfully",
                                     "group": group_name})


@router.get("/{id}", dependencies=[Depends(JwtBearer())], response_description="get task with id")
async def get_task(id: str, request: Request):
    task = await request.app.mongodb["tasks"].find_one({"_id": id})
    if task:
        return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.patch("/{id}", dependencies=[Depends(JwtBearer())], response_description="edit task with id and params")
async def edit_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
    decoded_user = get_user(request)
    user_id = decoded_user["userID"]
    check_user = await request.app.mongodb["tasks"].find_one({"$and": [{"_id": id}, {"user_id": user_id}]})

    if check_user is None:
        return HTTPException(status_code=404, detail=f"Task {id} not found")

    task = {key: value for key, value in task.dict().items() if value is not None}

    if len(task) >= 1:
        edit_task_result = await request.app.mongodb["tasks"].update_one({"_id": id}, {"$set": jsonable_encoder(task)})
        if edit_task_result.modified_count == 1:
            if (update_task := await request.app.mongodb["tasks"].find_one({"_id": id})) is not None:
                return update_task
    if (existing_task := await request.app.mongodb["tasks"].find_one({"_id": id})) is not None:
        return existing_task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", dependencies=[Depends(JwtBearer())], response_description="delete task with id")
async def delete_task(id: str, request: Request):
    delete_task_result = await request.app.mongodb["tasks"].delete_one({"_id": id})
    if delete_task_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": id, "message": f"delete {id} successfully"})

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
