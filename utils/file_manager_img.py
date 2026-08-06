import os
import shutil
import tempfile


def save_file_temp_img(upload_file):
   if upload_file:
    with tempfile.NamedTemporaryFile(
        delete=False,  # ne pas supprimer le fichier après utilisation
        suffix=os.path.splitext(upload_file.filename)[
            1
        ],  # extension du fichier (ex: .mp3)
    ) as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)
        return temp_file.name
   else:
    return None
