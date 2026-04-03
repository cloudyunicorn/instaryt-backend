from fastapi import APIRouter, UploadFile, File, Form
import time

from app.services.cloudinary_service import upload_file
from app.services.instagram_service import create_container, publish_container
from app.utils.file_handler import save_temp_file, delete_file

router = APIRouter()

@router.post("/post")
async def post_to_instagram(
    file: UploadFile = File(...),
    caption: str = Form(...)
):
    try:
        content = await file.read()
        temp_path = save_temp_file(content, file.filename)

        is_video = file.content_type.startswith("video")

        # Upload to Cloudinary
        media_url = upload_file(temp_path)

        # Create container
        container = create_container(media_url, caption, is_video)

        if "id" not in container:
            return {"error": "Container creation failed", "details": container}

        container_id = container["id"]

        # Wait for processing
        time.sleep(5 if not is_video else 15)

        # Publish
        publish_res = publish_container(container_id)

        # Cleanup
        delete_file(temp_path)

        return {
            "status": "success",
            "media_url": media_url,
            "instagram_response": publish_res
        }

    except Exception as e:
        return {"error": str(e)}