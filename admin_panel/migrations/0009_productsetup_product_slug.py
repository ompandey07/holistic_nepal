from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    ProductSetup = apps.get_model('admin_panel', 'ProductSetup')
    for product in ProductSetup.objects.all():
        if not product.PRODUCT_SLUG:
            orig_slug = slugify(product.PRODUCT_NAME) or f"product-{product.id}"
            slug = orig_slug
            counter = 1
            while ProductSetup.objects.filter(PRODUCT_SLUG=slug).exclude(id=product.id).exists():
                slug = f"{orig_slug}-{counter}"
                counter += 1
            product.PRODUCT_SLUG = slug
            product.save(update_fields=['PRODUCT_SLUG'])


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_productcategory_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsetup',
            name='PRODUCT_SLUG',
            field=models.SlugField(blank=True, max_length=500, null=True),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='productsetup',
            name='PRODUCT_SLUG',
            field=models.SlugField(blank=True, default='', max_length=500, unique=True),
            preserve_default=False,
        ),
    ]

