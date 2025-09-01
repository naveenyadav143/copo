from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0002_remove_coattainment_attainment_percentage_and_more'),
        ('calculate', '0002_remove_studentmark'),
    ]

    operations = [
        # Merge migration to resolve conflicting 0002 leaf nodes. No schema operations required.
    ]
