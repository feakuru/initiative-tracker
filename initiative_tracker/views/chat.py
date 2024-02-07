from fastapi import APIRouter

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@chat_router.get("/")
async def list_chats():
    return {
        "chats": [
            {"id": 1, "name": "General"},
            {"id": 2, "name": "Party 1"}
        ]
    }
