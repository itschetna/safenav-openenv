from my_env.api import app   # this is correct

def main():
    return app# import your FastAPI app


# (optional: keep this for local running)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)