from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0004_studenttotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obtained_marks', models.FloatField()),
                ('total_marks', models.FloatField()),
                ('co', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculate.co')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculate.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculate.student')),
            ],
        ),
    ]
