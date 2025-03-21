from fastapi import FastAPI

# Create a FastAPI app
app = FastAPI()

# Define a basic GET route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)