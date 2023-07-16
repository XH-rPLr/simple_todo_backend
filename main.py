# Import required libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import todo_routes
import uvicorn

# Run the application
# if __name__ == "__main__":   
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# Create FastAPI instance
app = FastAPI()

app.include_router(todo_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

