import os 
import cloudinary
import cloudinary.uploader


cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
)

def upload_on_cloudinary(file_path: str):
    """
    Takes the file from local server and upload it on cloudinary 
    """
    try:
        if not file_path:
          return None
        
        # uplaod 
        response = cloudinary.uploader.upload(file_path)

        # remove from server
        if os.path.exists(file_path):
           os.remove(file_path)
        
        return response
    except Exception as e:
       print(f"Cloudinary Upload Error: {e}")
       if os.path.exists(file_path):
        os.remove(file_path)
        return None
    