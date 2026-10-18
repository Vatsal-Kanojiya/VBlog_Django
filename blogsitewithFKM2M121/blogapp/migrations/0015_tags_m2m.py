from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0014_split_tag_strings'),
    ]

    operations = [
        migrations.RemoveField(model_name='blog', name='tags'),
        migrations.RenameField(model_name='blog', old_name='topics', new_name='tags'),
    ]
