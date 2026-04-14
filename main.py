import uuid #產生唯一ID的標準庫
from fastapi import HTTPException # 引入錯誤處理工具
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id:Optional[str] = None #預設為None,由後端產生
    title: str  #標題（必填,string)
    description: Optional[str] = None  #說明 (選填,預設為None)
    completed: bool = False     #是否完成（預設為False)

#初始化 FastAPI
app = FastAPI()

# 模擬一個暫時的資料庫 (List)
todo_db = []

#定義一個 GET 請求路由
@app.get("/")
def read_root():
    return {"message": "我的第一個 API 運作中"}

#定義一個獲取特定 ID任務的路由
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query_param": q}

@app.get("/status")
def read_status():
    return {"status": "online"}

@app.post("/todo/")
def create_todo(todo:Todo):
    #將Pydantic model轉為 Python dictionary
    todo_data = todo.model_dump()

    # 自動產生唯一一個ID
    todo_data["id"] = str(uuid.uuid4())

    #存入暫時資料庫
    todo_db.append(todo_data)
    return {"message": "任務新增成功", "data": todo_data}

@app.get("/todo/")
def get_all_todo():
    return todo_db

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: str):
    
    # 1. 尋找該 ID 在 list 中的位置 (index)
    find_index = None
    for index, data in enumerate(todo_db):
        if data["id"] == todo_id:
            find_index = index
            break

    # 2. 如果沒找到，拋出 404 錯誤給前端      
    if find_index == None:
        raise HTTPException(status_code=404,detail=f"找不到該ID:{todo_id}")

    # 3. 從 list 中移除該項目    
    delete_data = todo_db.pop(find_index)
    
    
    return {"message": "任務已成功刪除", "deleted_todo": delete_data }
    
