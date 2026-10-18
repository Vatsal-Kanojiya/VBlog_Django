# VBlog

A Django blogging platform with a social layer: write posts by genre and tag, follow writers, like, comment and save posts, browse latest and popular, and upgrade to a VIP plan with Razorpay.

Built in 2023; **v2** (this branch) upgrades the writing experience.

## What's new in v2

- **Rich-text editor** (TipTap): headings, bold/italic/underline/strike, lists, quotes, links, dividers.
- **Code snippets**: code blocks with a language picker, highlighted with Pygments on the post page.
- **Real tags**: a Tag table (up to 5 per post), a page per tag at `/tag/<slug>/`, and search over tags and titles.
- **Images**: an optional cover per post, plus inline images from a toolbar button, paste or drag-and-drop, with alt text.
- **Edit your posts**: only the author can edit.

Safety rails: post HTML is cleaned with nh3 on every save, so scripts, event handlers, `javascript:` links and outside images are all dropped. Uploads are checked, resized to 1600px and re-encoded, which strips EXIF and GPS data. Uploads need login and a CSRF token, with a limit of 30 a day per writer. Existing plain-text posts and comma-separated tags are migrated automatically.

## Run it

```bash
cd VBlog_Django
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp blogsitewithFKM2M121/blogsite/.env.example blogsitewithFKM2M121/blogsite/.env   # then fill it in
cd blogsitewithFKM2M121
python manage.py migrate
python manage.py runserver
```

Tests: `python manage.py test blogapp`

The editor loads TipTap from esm.sh, so writing posts needs an internet connection. Without JavaScript, the plain text box still works.

## Layout

- `blogapp/richtext.py`: HTML cleaning, plain-text conversion and code highlighting
- `blogapp/images.py`: upload checks and re-encoding
- `static/js/editor.js`: the editor; `static/css/post.css`: reading and writing styles
- `static/css/pygments.css`: generated code colours (the command is in the file's first line)
