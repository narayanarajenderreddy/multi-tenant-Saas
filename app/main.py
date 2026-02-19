
from fastapi import FastAPI
from app.api import auth
from app.api import tenant
from app.api import project
app = FastAPI()
from app.core.exception import register_exception_handlers
register_exception_handlers(app)

@app.get("/")
def read_root():
    return {"message":"multi-tenant-system project started!"}

#auth api list.
app.include_router(auth.router)
app.include_router(tenant.router)
app.include_router(project.router)



