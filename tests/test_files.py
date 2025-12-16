from dotenv import load_dotenv
load_dotenv()
from pprint import pprint as pp
from pypipedrive.models.files import Files

def save_file(data: bytes, file_name: str, file_type: str):
    with open(f"{file_name}", "wb") as f:
        f.write(data)
        print(f"File saved as {file_name}")

# files_id = {
#     "application/msword": 565956,
#     "application/octet-stream": 201252,
#     "application/pdf": 17468,
#     "application/vnd.ms-excel": 486428,
#     "application/vnd.openxmlformats-officedocument.presentationml.presentation": 530794,
#     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": 486463,
#     "application/vnd.openxmlformats-officedocument.wordprocessingml.document": 239991,
#     "application/zip": 544224,
#     "audio/mp4": 1,
#     "image/gif": 487453,
#     "image/heic": 573728,
#     "image/jpeg": 486412,
#     "image/png": 201253,
#     "image/webp": 497963,
#     "message/rfc822": 486870,
#     "text/calendar": 492113,
# }

# for file_type, file_id in files_id.items():
#     print(f"Downloading file type: {file_type} (id={file_id})")
#     f = Files.download(id=file_id)
#     save_file(
#         data      = f.content,
#         file_name = f.file_name,
#         file_type = f.file_type
#     )

# ID = 17468 # PDF
# f = Files.get(id=ID)
# pp(f.to_record())
# f = Files.download(id=ID)
# save_file(
#     data      = f.content,
#     file_name = f.file_name,
#     file_type = f.file_type
# )