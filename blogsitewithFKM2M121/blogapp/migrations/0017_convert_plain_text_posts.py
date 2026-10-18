from django.db import migrations

from blogapp import richtext


def to_html(apps, schema_editor):
    """Old posts are plain text: turn them into paragraphs and render them."""
    blog = apps.get_model('blogapp', 'blog')
    for post in blog.objects.all():
        post.content = richtext.clean_html(post.content)
        post.content_html = richtext.render_html(post.content)
        post.save(update_fields=['content', 'content_html'])


def to_text(apps, schema_editor):
    blog = apps.get_model('blogapp', 'blog')
    for post in blog.objects.all():
        post.content = richtext.plain_text(post.content.replace('</p>', '</p>\n\n').replace('<br>', '\n')).strip()
        post.save(update_fields=['content'])


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0016_rich_text_content'),
    ]

    operations = [
        migrations.RunPython(to_html, to_text),
    ]
