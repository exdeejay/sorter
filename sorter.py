import glob
import shutil
import os
import re
from datetime import datetime
from exif import Image
import ffmpeg

month = [
    '01. January', '02. February', '03. March',
    '04. April', '05. May', '06. June',
    '07. July', '08. August', '09. September',
    '10. October', '11. November', '12. December'
    ]

for jpg in glob.glob('*.jpg') + glob.glob('*.jpeg'):
    file = open(jpg, 'rb')
    img = Image(file)
    if 'datetime_original' in img.list_all():
        date_taken = datetime.fromisoformat(re.sub('^([0-9]{4}):([0-9]{2}):([0-9]{2}) ', '\\1-\\2-\\3 ', img.datetime_original))
        file.close()
        path = f'{date_taken.year}/{month[date_taken.month-1]}'
        os.makedirs(path, exist_ok=True)
        shutil.move(jpg, f'{path}/{jpg}')
    else:
        file.close()
        os.makedirs('unknown', exist_ok=True)
        shutil.move(jpg, f'unknown/{jpg}')

for mov in glob.glob('*.mp4') + glob.glob('*.mov'):
    metadata = ffmpeg.probe(mov)
    date_taken = datetime.fromisoformat(metadata['streams'][1]['tags']['creation_time'][:-1])
    path = f'{date_taken.year}/{month[date_taken.month-1]}'
    os.makedirs(path, exist_ok=True)
    shutil.move(mov, f'{path}/{mov}')
        
for png in glob.glob('*.png'):
    os.makedirs('unknown', exist_ok=True)
    shutil.move(png, f'unknown/{png}')        
