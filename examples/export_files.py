import time
from dotenv import load_dotenv
load_dotenv()
import os
import sys
import csv
import random as rnd
import pandas as pd
from pprint import pprint as pp
from pypipedrive.models.files import Files
from tqdm import tqdm

"""
https://your-company.pipedrive.com/settings/subscription/change

API usage: https://your-company.pipedrive.com/settings/usage-caps/api-usage
API tokens (Professional plan):
    - 90,000 x postes / day.
    - So 990,000/day
    - Download file 22 tokens. So 45,000 files/day max.
"""

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

# method to load the files.csv file
def load_csv(file_path: str) -> list[dict]:
    """
    Sort files by ID asc to keep track and have consistent order.
    """
    data = []
    with open(file_path, mode="r", encoding="utf-8-sig") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=";")
        for row in csvreader:
            row["ID"] = int(row["ID"])
            data.append(row)
    return sorted(data, key=lambda x: x["ID"])

FP = "./pipedrive_files/"
FP_CLEAN = "./pipedrive_files_clean/"

FILES_IDS = set()
for file_type in os.listdir(FP):
    if file_type.startswith(".") or "DS_Store" in file_type:
        continue
    file_type_path = f"{FP}{file_type}/"
    for file_name in os.listdir(file_type_path):
        if file_name.startswith(".") or "DS_Store" in file_name:
            continue
        file_id = file_name.split("-")[0]
        # print(f"{file_name} {file_id}")
        if "." in file_id:
            file_id = file_id.split(".")[0]
        FILES_IDS.add(int(file_id))


def save_file(file: Files):
    fn = f"{str(file.id)}-{file.file_name}"    
    file_extension = fn.split(".")[-1]
    
    if file.file_type in [None, ""] or "blob" in file.file_name:
        file_extension = "blob"

    fp = f"{FP}{file_extension}/"  # Create subfolder with name file_extesion
    if not os.path.exists(fp):
        os.makedirs(fp)
    
    if os.path.exists(f"{FP}{fn}"):
        fn = f"{str(file.id)}.{rnd.randint(1000,9999)}-{file.file_name}"
    with open(f"{fp}{fn}", "wb") as f:
        f.write(file.content)
        # print(f"File saved as {file_name}")


def save_fid_idx(idx: dict):
    data = []
    for finfo, duplicates in idx.items():
        data.append({"FileType": finfo[1], "FileID": finfo[0], "DuplicateOf": None})
        for dup in duplicates:
            data.append({"FileType": finfo[1], "FileID": dup, "DuplicateOf": finfo[0]})
    pd.DataFrame(data).to_csv("Pipedrive Duplicates Index.csv", index=False)


def save_file_root(file_id: int, file_type: str, data: bytes):    
    # Check if the file has already been saved
    fids = [
        int(fp.split(" - ")[0])
        for fp in os.listdir(f"{FP_CLEAN}{file_type}/")
        if not fp.startswith(".") and "DS_Store" not in fp
        ]
    if file_id in fids:
        return

    f = Files.get(id=file_id)
    with open(f"{FP_CLEAN}{file_type}/{file_id} - {f.name}", "wb") as f:
        f.write(data)


def check_duplicates():
    # Type is "root" or "child" whether the file is the first occurence or the
    # first duplicated occurrence.
    df = pd.DataFrame(columns=["Type", "FileID", "DuplicateOf"])
    fid_idx = {}
    bytes_fid = {}

    files_data = {}
    nb_files = 0
    for file_type in os.listdir(FP):
        if file_type.startswith(".") or "DS_Store" in file_type:
            continue
        file_type_path = f"{FP}{file_type}/"
        files_data[file_type] = {}
        files = os.listdir(file_type_path)

        fp_clean_type = f"{FP_CLEAN}{file_type}/"
        os.makedirs(fp_clean_type, exist_ok=True)

        for file_name in tqdm(files, desc=f"Checking files {file_type}", unit="file", total=len(files)):
            nb_files += 1
            if file_name.startswith(".") or "DS_Store" in file_name:
                continue

            # Read the file bytes to check for duplicates
            with open(f"{file_type_path}{file_name}", "rb") as f:
                file_bytes = f.read()
                file_id = file_name.split("-")[0]
                file_id = int(file_id.split(".")[0]) if "." in file_id else int(file_id)
                if files_data[file_type].get(file_bytes, None) is None:
                    files_data[file_type][file_bytes] = [file_name]

                    bytes_fid[file_bytes] = file_id
                    fid_idx[(file_id,file_type)] = set()
                    save_file_root(file_id=file_id, file_type=file_type, data=file_bytes)
                    save_fid_idx(idx=fid_idx)

                else:
                    files_data[file_type][file_bytes].append(file_name)
                    fid_idx[(bytes_fid[file_bytes],file_type)].add(file_id)
                    # df = pd.concat([df, pd.DataFrame([{"Type": "duplicate", "FileID": file_id, "DuplicateOf": files_data[file_type][file_bytes][0]}])], ignore_index=True)

    """TODO
    - Build an index table of duplicates
    - Save to CSV
    - Delete duplicates (keep a single copy)
    - Upload to Google Drive and share link to RG/LG
    """

    save_fid_idx(idx=fid_idx)

    total_files  = 0
    unique_files = 0
    print(list(files_data.keys()))
    for file_type, file_bytes_dict in files_data.items():
        unique_files += len(list(file_bytes_dict.keys()))
        for _, file_names in sorted(file_bytes_dict.items(), key=lambda x: len(x[1]), reverse=True):
            # print(f"  {file_type} {file_names[0]} duplicates: {len(file_names)}")
            total_files += len(file_names)
    # There should be 96513 files in total
    print(
        f"Total files checked: {total_files}.\n"
        f"Unique: {unique_files}.\n"
        f"Duplicates: {total_files - unique_files}.\n"
        f"NbFiles: {nb_files}.")

if __name__ == "__main__":
    check_duplicates()
    RUN_PIPEDRIVE_ETL = 0

    if RUN_PIPEDRIVE_ETL:
        files = load_csv("files.csv")
        files_size = 0
        files_processed = 0
        tokens = 0
        t0 = time.time()
        try:
            for file in tqdm(files, desc="Dowloading Pipedrive files", unit="file", total=len(files)):
                file_id = int(file["ID"])
                files_processed += 1
                if file_id in FILES_IDS:
                    # print(f"File ID={file_id} already downloaded, skipping.")
                    continue
                f = Files.download(id=int(file_id))
                files_size += f.file_size
                tokens += 22
                save_file(file=f)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error downloading file ID={file['ID']}: {e}")
        print(
            f"Total files downloaded: {files_processed}/{len(files)} "
            f"| Total size: {files_size/1024/1024:.2f} MB "
            f"| Time taken: {time.time() - t0:.2f} seconds "
            f"| Tokens used: {tokens} "
        )
    # As of 10/11/2025 47700/98115 files processed for 1.08M tokens used.


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