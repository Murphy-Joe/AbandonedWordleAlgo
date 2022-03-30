from fastapi import FastAPI
import multi_process


app = FastAPI()


@app.get("/")
async def root():
    best_words = multi_process.run_multi()
    return {"best words": best_words}
