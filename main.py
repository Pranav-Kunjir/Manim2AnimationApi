from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import subprocess
from fastapi.responses import FileResponse
import glob
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # <- frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"hello": "world"}

class CodeRequest(BaseModel):
    auth: str
    code: str

# def clean_code_block(code_block: str) -> str:
#     if code_block.startswith("python"):
#         code_block = code_block[len("python"):].strip()
#     return code_block

def clean_code_block(code_block: str) -> str:
    # Remove leading "python" or "python\n"
    if code_block.strip().startswith("`python"):
        code_block = code_block.strip()[7:].lstrip()

    # Remove any wrapping backticks
    code_block = code_block.strip("`").strip()

    return code_block


def makefile(file,text):
    with open(file,"w") as f:
        f.seek(0)
        f.truncate()
        f.write(text)
        f.close()


def get_latest_video_file() -> str:
    """Find the most recently created .mp4 file from Manim's output directory."""
    files = glob.glob("media/videos/**/**/*.mp4", recursive=True)
    if not files:
        return None
    latest_file = max(files, key=os.path.getctime)
    return latest_file

# def renderVideo(file):
#     os.system(f"manim -pql {file}")
    
def renderVideo(file):
    # subprocess.run(["manim", "-v", "WARNING", "--format", "mp4", file], check=True)
    result = subprocess.run(
        ["manim", "-v", "WARNING", "--format", "mp4", file],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            returncode=result.returncode,
            cmd=result.args,
            output=result.stdout,
            stderr=result.stderr
        )



def delete_manim_cache():
    if os.path.exists("media"):
        subprocess.call(["rm", "-rf", "media/"])
        


def wait_for_file_ready(filepath, timeout=10):
    for _ in range(timeout * 10):  # Check every 0.1s
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            return True
        time.sleep(0.1)
    return False



# @app.post("/render/")
# def render_video(request: CodeRequest):
#     if request.auth == "pranavbhai":
#         delete_manim_cache()
#         code = request.code
#         code_block = clean_code_block(code)
#         makefile("./animation.py", code_block)
#         renderVideo("./animation.py")

#         video_file = get_latest_video_file()
#         if not video_file or not wait_for_file_ready(video_file):
#             raise HTTPException(status_code=404, detail="Video not ready or not found")

#         # ✅ Return the video file here
#         return FileResponse(video_file, media_type="video/mp4", filename="output.mp4")

#     else:
#         return {"error": "invalid api key"}




from fastapi.responses import JSONResponse

@app.post("/render/")
async def render_video(request: CodeRequest):
    if request.auth != "pranavbhai":
        return JSONResponse(
            status_code=403,
            content={"error": "Invalid API key", "details": "Auth failed"},
        )

    try:
        delete_manim_cache()
        code_block = clean_code_block(request.code)
        makefile("./animation.py", code_block)
        renderVideo("./animation.py")

        video_file = get_latest_video_file()
        if not video_file:
            return JSONResponse(
                status_code=404,
                content={"error": "No video file found", "details": "Manim did not produce output"},
            )

        if not wait_for_file_ready(video_file):
            return JSONResponse(
                status_code=408,
                content={"error": "Video not ready in time", "details": "File did not reach minimum size in time"},
            )

        print("Returning video:", video_file)
        return FileResponse(video_file, media_type="video/mp4", filename="output.mp4")

    except subprocess.CalledProcessError as e:
        print("Manim rendering error:", e.stderr)
        return JSONResponse(
            status_code=500,
            content={"error": "Manim rendering failed", "details": e.stderr},
        )

    except Exception as e:
        print("Unhandled error:", e)
        return JSONResponse(
            status_code=500,
            content={"error": "Unhandled server error", "details": str(e)},
        )


