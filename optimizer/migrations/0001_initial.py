# Generated by Django 2.0.9 on 2019-01-03 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddComponent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=10)),
                ('comp_type', models.CharField(max_length=10)),
                ('comp_num', models.IntegerField()),
                ('zone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CreateSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AddToController',
            fields=[
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
                ('configured', models.BooleanField(default=False)),
                ('mode', models.CharField(choices=[('nc', 'Not Configured'), ('ss', 'Solar Support'), ('ab', 'Arbitrage'), ('ps', 'Peak Shaving')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='ComponentOutputs',
            fields=[
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
                ('output', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CreateBattery',
            fields=[
                ('energy_capacity', models.IntegerField()),
                ('soc_min', models.IntegerField()),
                ('soc_max', models.IntegerField()),
                ('base_cost', models.FloatField()),
                ('energy_cost', models.FloatField()),
                ('controller_configured', models.BooleanField(default=False)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
            ],
        ),
        migrations.CreateModel(
            name='CreateController',
            fields=[
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
            ],
        ),
        migrations.CreateModel(
            name='CreateConverter',
            fields=[
                ('power', models.IntegerField()),
                ('base_cost', models.FloatField()),
                ('power_cost', models.FloatField()),
                ('controller_configured', models.BooleanField(default=False)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
            ],
        ),
        migrations.CreateModel(
            name='CreateDemand',
            fields=[
                ('demand_file', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
                ('data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CreateGenerator',
            fields=[
                ('power', models.IntegerField()),
                ('base_cost', models.FloatField()),
                ('fuel_cost', models.FloatField()),
                ('controller_configured', models.BooleanField(default=False)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
            ],
        ),
        migrations.CreateModel(
            name='CreateGrid',
            fields=[
                ('energy_cost', models.FloatField()),
                ('nm_allowed', models.BooleanField(default=False)),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
            ],
        ),
        migrations.CreateModel(
            name='CreateSolar',
            fields=[
                ('system_capacity', models.IntegerField()),
                ('base_cost', models.FloatField()),
                ('perw_cost', models.FloatField()),
                ('demand_file', models.FileField(upload_to='documents/')),
                ('component', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='optimizer.AddComponent')),
                ('data', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='addcomponent',
            name='system_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optimizer.CreateSystem'),
        ),
    ]
