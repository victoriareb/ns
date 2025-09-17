from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import io
from fastapi import Response

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.get("/ping")
def ping():
    return {"status": "ok"}


from fastapi import FastAPI, HTTPException, Response
import httpx

# app = FastAPI()
UPSTREAM = "https://templates.invoicehome.com/invoice-template-us-neat-750px.png"

@app.head("/image.png")
async def head_image():
    async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
        r = await client.head(UPSTREAM)
        r.raise_for_status()
    ct = r.headers.get("content-type", "").split(";",1)[0].strip()
    if not ct.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upstream not an image")
    headers = {
        "Content-Type": ct,
        "Content-Length": r.headers.get("content-length", ""),
        "Content-Disposition": 'inline; filename="invoice.png"',
        "Cache-Control": "public, max-age=3600",
    }
    return Response(content=b"", headers=headers)

@app.get("/image.png")
async def get_image():
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        r = await client.get(UPSTREAM)
        r.raise_for_status()
    ct = r.headers.get("content-type", "").split(";",1)[0].strip()
    if not ct.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upstream not an image")
    content = r.content  # small images OK; ensures Content-Length can be set
    headers = {
        "Content-Disposition": 'inline; filename="invoice.png"',
        "Cache-Control": "public, max-age=3600",
        "Content-Length": str(len(content)),
    }
    return Response(content=content, media_type=ct, headers=headers)


# @app.get("/image")
# async def get_image():
#     """
#     Fetch an image (PNG, JPG, or JPEG) from the provided URL and stream it back with proper Content-Type headers.
    
#     Returns:
#         StreamingResponse: The image data with proper headers
#     """
#     try:
#         url = "https://www.invoicesimple.com/wp-content/uploads/2024/08/simple-invoice-template-light-blue-en.jpg"
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url)
#             response.raise_for_status()
            
#             # Check if the content is actually an image (PNG, JPG, or JPEG)
#             content_type = response.headers.get('content-type', '').lower()
#             if not any(img_type in content_type for img_type in ['image/png', 'image/jpeg', 'image/jpg']):
#                 raise HTTPException(status_code=400, detail="URL does not point to a supported image format (PNG, JPG, or JPEG)")
            
#             # Determine the correct media type
#             if 'image/png' in content_type:
#                 media_type = "image/png"
#             elif 'image/jpeg' in content_type or 'image/jpg' in content_type:
#                 media_type = "image/jpeg"
#             else:
#                 media_type = "image/jpeg"  # Default fallback
            
#             # Stream the image data back
#             return Response(
#                 content=response.content,
#                 media_type=media_type,
#                 headers={
#                     "Content-Disposition": "inline",
#                     "Cache-Control": "public, max-age=3600",
#                     "Content-Length": str(len(response.content))  # 👈 ensure length
#                 }
#             )
            
#     except httpx.HTTPError as e:
#         raise HTTPException(status_code=400, detail=f"Failed to fetch image: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
