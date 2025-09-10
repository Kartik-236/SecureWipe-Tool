import os

def wipe_file(file_path, passes=3):
    """
    Securely overwrite a file and delete it.
    passes: how many overwrite passes to make.
    """
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return False

    file_size = os.path.getsize(file_path)
    try:
        # Overwrite file with random data multiple times
        with open(file_path, "r+b") as f:
            for p in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())  # ensure write to disk
                print(f"Pass {p+1}/{passes} complete.")

        # Optionally overwrite with zeros once
        with open(file_path, "r+b") as f:
            f.seek(0)
            f.write(b"\x00" * file_size)
            f.flush()
            os.fsync(f.fileno())
            print("Final zeroing pass complete.")

        # Delete the file after overwriting
        os.remove(file_path)
        print(f"File securely wiped and deleted: {file_path}")
        return True

    except Exception as e:
        print(f"Error wiping file: {e}")
        return False
