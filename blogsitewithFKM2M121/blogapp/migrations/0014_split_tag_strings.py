from django.db import migrations
from django.utils.text import slugify


def split_tags(apps, schema_editor):
    """Turn each post's 'a, b, c' tag string into rows in the Tag table."""
    blog = apps.get_model('blogapp', 'blog')
    Tag = apps.get_model('blogapp', 'Tag')
    for post in blog.objects.all():
        names = []
        for part in (post.tags or '').split(','):
            name = ' '.join(part.split()).lower()[:30]
            if name and slugify(name) and name not in names:
                names.append(name)
        for name in names[:5]:
            tag = Tag.objects.filter(name=name).first()
            if tag is None:
                base, slug, n = slugify(name), slugify(name), 2
                while Tag.objects.filter(slug=slug).exists():
                    slug, n = f'{base}-{n}', n + 1
                tag = Tag.objects.create(name=name, slug=slug)
            post.topics.add(tag)


def join_tags(apps, schema_editor):
    blog = apps.get_model('blogapp', 'blog')
    for post in blog.objects.all():
        post.tags = ', '.join(t.name for t in post.topics.all())
        post.save(update_fields=['tags'])


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0013_tag_model'),
    ]

    operations = [
        migrations.RunPython(split_tags, join_tags),
    ]
