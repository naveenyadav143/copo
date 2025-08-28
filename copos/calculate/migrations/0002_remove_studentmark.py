from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StudentMark',
        ),
    ]
