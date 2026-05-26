from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import predict

app = FastAPI(
    title="CV-Intelligence Recommender API",
    description="API untuk ekstraksi CV dan rekomendasi pekerjaan — Capstone PJK-GM075",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware — allow Streamlit frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "status": "CV-IR API is running 🚀",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "predict": "POST /api/v1/predict",
        },
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
