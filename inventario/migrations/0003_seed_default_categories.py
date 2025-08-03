from django.db import migrations

def crear_categorias(apps, schema_editor):
    Categoria = apps.get_model('inventario', 'Categoria')

    categorias_base = [
        "General",
        "Consumibles",
        "Servicios",
        "Electrónicos",
        "Ropa",
        "Otros",
    ]

    for nombre in categorias_base:
        # Crea solo si no existe
        Categoria.objects.get_or_create(nombre=nombre)

class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0002_alter_producto_categoria"),  # ← última migración existente
    ]

    operations = [
        migrations.RunPython(crear_categorias, migrations.RunPython.noop),
    ]

