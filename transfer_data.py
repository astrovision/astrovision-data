import os
import shutil

import hashlib
import json
import dropbox


CHUNK_SIZE = 2 * 32768


def generate_file_md5(fpath: str, blocksize: int = 2 ** 20) -> str:
    """Calculates MD5 checksum for the input file, which is used to verify that the file was properly downloaded"""
    m = hashlib.md5()
    with open(fpath, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2"""
        dbx = dropbox.Dropbox(self.access_token)

        file_size = os.path.getsize(file_from)
        with open(file_from, "rb") as f:
            if file_size <= CHUNK_SIZE:
                dbx.files_upload(f.read(), file_to)
            else:
                upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id, offset=f.tell()
                )
                commit = dropbox.files.CommitInfo(path=file_to)

                while f.tell() < file_size:
                    print(f"{f.tell()}/{file_size} {f.tell() / file_size * 100}%")
                    if (file_size - f.tell()) <= CHUNK_SIZE:
                        dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit)
                    else:
                        dbx.files_upload_session_append(f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                        cursor.offset = f.tell()


def main():
    access_token = "sl.Bc3UiEE8s3a5doYWpgkiGRLbRVlV7BcjqvAIbxzOGFq24LEpuIhpyDz9nbqn2fEEnZRsc2UG-rwnsEcAGvOv8-KpP2lY3Tsiexuo7-VUNTpjsWqSInD_NsN2msLDzu6JOzkU5vH-gI3d"
    transferData = TransferData(access_token)

    # Read in MD5 checksums.
    with open(os.path.join("lists", "md5.json")) as fin:
        md5_checksums = json.load(fin)

    LOCAL_ROOT_DIR = "/hdd/tdriver6/astrovision/clusters/train/rosiris_67p"
    # LOCAL_ROOT_DIR = "/hdd/tdriver6/astrovision/segments/orex_bennu"
    dataset_name = LOCAL_ROOT_DIR.split("/")[-1]
    # REMOTE_ROOT_DIR = "/research/astrovision/clusters/train/dawn_ceres"
    dir_list = os.listdir(LOCAL_ROOT_DIR)
    dir_list.sort()
    for dir in dir_list:
        if not os.path.isdir(os.path.join(LOCAL_ROOT_DIR, dir)):
            continue
        # ZIP contents.
        print("Zipping contents...")
        shutil.make_archive(os.path.join(LOCAL_ROOT_DIR, dir), "zip", os.path.join(LOCAL_ROOT_DIR, dir))

        # Transfer to DropBox.
        file_from_path = os.path.join(LOCAL_ROOT_DIR, dir + ".zip")
        # file_to_path = os.path.join(REMOTE_ROOT_DIR, dir + ".zip")
        # print(f"Transfering local file {file_from_path} to Dropbox file {file_to_path}...")
        # transferData.upload_file(file_from_path, file_to_path)
        # print("Done.")
        # os.remove(os.path.join(LOCAL_ROOT_DIR, dir + ".zip"))

        # Compute MD5 hash.
        hash = generate_file_md5(file_from_path)
        print(file_from_path, hash)
        md5_checksums[dataset_name][dir] = hash

    with open(os.path.join("lists", "md5.json"), "w") as fout:
        json.dump(md5_checksums, fout)


if __name__ == "__main__":
    main()
