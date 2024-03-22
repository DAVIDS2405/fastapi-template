from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes import user, student, subject, enrollment


app = FastAPI(
    docs_url="/api/v1/docs",
    title="Template FastAPI",
    description="Template for FastAPI",
    version="1.0",
    openapi_url="/api/v1/openapi.json",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(student.router, prefix="/api/v1")
app.include_router(subject.router, prefix="/api/v1")
app.include_router(enrollment.router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse("/api/v1/docs")
