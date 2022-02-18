# Generated by Django 4.0.2 on 2022-02-18 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='clases_de_palabras',
            fields=[
                ('id', models.IntegerField()),
                ('clase', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('determinante_1', models.CharField(max_length=30)),
                ('determinante_2', models.CharField(max_length=30)),
                ('determinante_3', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='determinante_1',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('determinante', models.CharField(max_length=45)),
                ('tipo', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='determinante_2',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('determinante', models.CharField(max_length=45)),
                ('tipo', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='determinante_3',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('determinante', models.CharField(max_length=45)),
                ('tipo', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='fuente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fuente', models.CharField(max_length=35)),
                ('link', models.CharField(max_length=200)),
                ('referencia', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='lemas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lema', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='temas',
            fields=[
                ('id', models.IntegerField()),
                ('tema', models.CharField(max_length=35, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='tipo_documento',
            fields=[
                ('id', models.IntegerField()),
                ('tipo', models.CharField(max_length=35, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='zonas',
            fields=[
                ('id', models.IntegerField()),
                ('zona', models.CharField(max_length=35, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='subzonas',
            fields=[
                ('id', models.IntegerField()),
                ('subzona', models.CharField(max_length=35, primary_key=True, serialize=False)),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.zonas')),
            ],
        ),
        migrations.CreateModel(
            name='documentos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=120)),
                ('fecha_incorporacion', models.DateField()),
                ('fecha_publicacion', models.DateField()),
                ('parrafos', models.IntegerField()),
                ('extension_tokens', models.IntegerField()),
                ('documento', models.CharField(max_length=25000)),
                ('fuente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.fuente')),
                ('subzona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.subzonas')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.temas')),
                ('tipo_documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.tipo_documento')),
                ('zona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.zonas')),
            ],
        ),
        migrations.CreateModel(
            name='casos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('caso', models.CharField(max_length=35)),
                ('mayuscula', models.BooleanField(default=False)),
                ('posicion', models.IntegerField()),
                ('lema_anterior', models.CharField(max_length=35)),
                ('lema_posterior', models.CharField(max_length=35)),
                ('desinencia', models.CharField(max_length=5)),
                ('prefijos', models.CharField(max_length=5)),
                ('clase_de_palabra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.clases_de_palabras')),
                ('determinante_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.determinante_1')),
                ('determinante_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.determinante_2')),
                ('determinante_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.determinante_3')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.documentos')),
                ('lema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corpus_base.lemas')),
            ],
        ),
    ]