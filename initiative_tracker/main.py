import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from initiative_tracker.views.chat import chat_router
from initiative_tracker.views.session import session_router
from initiative_tracker.views.user import user_router

app = FastAPI(title="Tortoise ORM FastAPI example")
app.include_router(chat_router)
app.include_router(session_router)
app.include_router(user_router)


register_tortoise(
    app,
    db_url=os.environ["DATABASE_URL"],
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
