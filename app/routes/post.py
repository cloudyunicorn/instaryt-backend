from fastapi import APIRouter, UploadFile, File, Form
import time

from app.services.cloudinary_service import upload_file
from app.services.instagram_service import create_container, publish_container, check_container_status
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
        if is_video:
            max_retries = 15 # 1 minute 15 seconds max
            for _ in range(max_retries):
                status_res = check_container_status(container_id)
                status_code = status_res.get("status_code")
                if status_code == "FINISHED":
                    break
                elif status_code == "ERROR":
                    return {"error": "Video processing failed on Instagram", "details": status_res}
                time.sleep(5)
            else:
                return {"error": "Video processing timed out after 75 seconds", "details": {"container_id": container_id}}
        else:
            time.sleep(5)

        # Publish
        publish_res = publish_container(container_id)

        # Cleanup
        delete_file(temp_path)

        if "error" in publish_res:
            error_data = publish_res["error"]
            error_msg = error_data.get("message", "Unknown error") if isinstance(error_data, dict) else str(error_data)
            return {"error": error_msg, "details": publish_res}

        return {
            "status": "success",
            "media_url": media_url,
            "instagram_response": publish_res
        }

    except Exception as e:
        return {"error": str(e)}