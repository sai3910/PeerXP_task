# Generated by Django 3.0 on 2020-10-27 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20201027_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='attach_file',
            field=models.FileField(null=True, upload_to='attachment_records', verbose_name='Data File'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('High', 'HIGH - Production System Down'), ('Med', 'MED - System Impaired'), ('Low', 'LOW - General Guidence')], max_length=30, null=True),
        ),
    ]