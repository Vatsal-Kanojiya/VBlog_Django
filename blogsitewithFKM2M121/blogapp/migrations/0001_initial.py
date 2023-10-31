# Generated by Django 4.2.3 on 2023-09-26 12:23

import blogapp.models
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='bloguser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('idu', models.CharField(default='ooo', max_length=10)),
                ('user_name', models.CharField(blank=True, max_length=30, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(30)])),
                ('first_name', models.CharField(default='   ', max_length=30, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(20)])),
                ('last_name', models.CharField(default='   ', max_length=30, validators=[django.core.validators.MinLengthValidator(3), django.core.validators.MaxLengthValidator(20)])),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.MaxLengthValidator(50)])),
                ('mobile', models.IntegerField(validators=[django.core.validators.MinValueValidator(6000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=1)),
                ('date_of_birth', models.DateField(validators=[blogapp.models.validatedate])),
                ('bio', models.CharField(max_length=500, null=True, validators=[django.core.validators.MaxLengthValidator(300)])),
                ('status', models.BooleanField(default=False, null=True)),
                ('date_of_joining', models.DateField(null=True)),
                ('last_login', models.DateTimeField(null=True)),
                ('dp', models.ImageField(null=True, upload_to='user/images')),
                ('social_media', models.CharField(blank=True, max_length=10, null=True)),
                ('interests', models.CharField(blank=True, max_length=10, null=True)),
                ('settings', models.CharField(blank=True, max_length=10, null=True)),
                ('slug', models.SlugField(blank=True, default='slugdefault', null=True)),
                ('follows', models.ManyToManyField(blank=True, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idb', models.CharField(default='ooo', max_length=10)),
                ('title', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(50)])),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(3000), django.core.validators.MaxLengthValidator(6000)])),
                ('author', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(10), django.core.validators.MaxLengthValidator(50)])),
                ('date_of_publish', models.DateTimeField()),
                ('genre', models.CharField(max_length=30, validators=[django.core.validators.MaxLengthValidator(20)])),
                ('tags', models.CharField(max_length=200, validators=[django.core.validators.MaxLengthValidator(50)])),
                ('likes', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('likeuser', models.TextField(default=',')),
                ('views', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('slug', models.SlugField(blank=True, default='slugdefault')),
                ('likess', models.ManyToManyField(blank=True, related_name='blogs_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idc', models.CharField(default='ooo', max_length=10)),
                ('date_of_comment', models.DateField()),
                ('comment_content', models.TextField(validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(100)], verbose_name='Com__ment')),
                ('idb', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='blogapp.blog')),
                ('idu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bloguser',
            name='saves',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='blogapp.blog'),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]