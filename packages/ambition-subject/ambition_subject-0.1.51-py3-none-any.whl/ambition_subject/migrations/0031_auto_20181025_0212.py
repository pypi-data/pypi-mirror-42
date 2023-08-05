# Generated by Django 2.1.2 on 2018-10-25 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("ambition_subject", "0030_auto_20181025_0155")]

    operations = [
        migrations.RenameField(
            model_name="flucytosinemisseddoses",
            old_name="flucy_day_missed",
            new_name="day_missed",
        ),
        migrations.RenameField(
            model_name="flucytosinemisseddoses",
            old_name="flucy_doses_missed",
            new_name="doses_missed",
        ),
        migrations.RenameField(
            model_name="flucytosinemisseddoses",
            old_name="flucy_missed_reason",
            new_name="missed_reason",
        ),
        migrations.RenameField(
            model_name="historicalflucytosinemisseddoses",
            old_name="flucy_day_missed",
            new_name="day_missed",
        ),
        migrations.RenameField(
            model_name="historicalflucytosinemisseddoses",
            old_name="flucy_doses_missed",
            new_name="doses_missed",
        ),
        migrations.RenameField(
            model_name="historicalflucytosinemisseddoses",
            old_name="flucy_missed_reason",
            new_name="missed_reason",
        ),
        migrations.AlterUniqueTogether(
            name="amphotericinmisseddoses", unique_together={("week2", "day_missed")}
        ),
        migrations.AlterUniqueTogether(
            name="flucytosinemisseddoses", unique_together={("week2", "day_missed")}
        ),
    ]
