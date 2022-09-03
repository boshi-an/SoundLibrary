from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('App', '0002_initial')
    ]
    operations = [
        migrations.RunSQL('CREATE EXTENSION IF NOT EXISTS pg_trgm'),
    ]