"""
Merge migration: combines the server branch (0021_event_story_poster ->
0022_volunteergallery) with the local branch (0021_add_amharic_translations
-> 0022_add_site_content -> 0023_sitecontent_bilingual).
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rotom', '0021_event_story_poster'),
        ('rotom', '0021_add_amharic_translations'),
        ('rotom', '0022_volunteergallery'),
        ('rotom', '0022_add_site_content'),
        ('rotom', '0023_sitecontent_bilingual'),
    ]

    operations = [
    ]
