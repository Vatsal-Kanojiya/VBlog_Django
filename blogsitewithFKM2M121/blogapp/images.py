"""Uploaded images: check them, shrink them and strip their metadata.

Every upload is decoded and re-encoded with Pillow, so what gets stored is a
plain image we produced (no EXIF/GPS from phone photos, no smuggled payloads),
with a random file name.
"""

import uuid
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from PIL import Image, ImageOps, UnidentifiedImageError

MAX_BYTES = 5 * 1024 * 1024
MAX_PIXELS = 40_000_000          # refuse decompression bombs before decoding
MAX_EDGE = 1600                  # longest side after resizing
FORMATS = {'JPEG': 'jpg', 'PNG': 'png', 'WEBP': 'webp', 'GIF': 'gif'}
DAILY_UPLOADS = 30               # inline images per writer per day


def process(upload):
    """Return a cleaned ContentFile, or raise ValidationError with a readable message."""
    if upload.size > MAX_BYTES:
        raise ValidationError('Images can be at most 5 MB.')
    try:
        with Image.open(upload) as probe:
            fmt = probe.format
            if fmt not in FORMATS:
                raise ValidationError('Use a JPEG, PNG, WebP or GIF image.')
            if probe.width * probe.height > MAX_PIXELS:
                raise ValidationError('That image is too large.')
            probe.verify()
        upload.seek(0)
        with Image.open(upload) as img:
            img = ImageOps.exif_transpose(img)  # keep phone photos upright once EXIF is gone
            img.thumbnail((MAX_EDGE, MAX_EDGE))
            if fmt == 'JPEG' and img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            out = BytesIO()
            # GIFs keep only their first frame
            img.save(out, format=fmt, optimize=True, **({'quality': 85} if fmt in ('JPEG', 'WEBP') else {}))
    except (UnidentifiedImageError, OSError, SyntaxError, Image.DecompressionBombError):
        raise ValidationError('That file is not a readable image.')
    return ContentFile(out.getvalue(), name=f'{uuid.uuid4().hex}.{FORMATS[fmt]}')
