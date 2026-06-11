from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
# from store.models import Product

User = get_user_model()

PRODUCTS = [
    # WOMEN - DRESSES & CLOTHING
    ("Floral Wrap Dress", "women", 799, 1999, "https://picsum.photos/seed/floraldress/400/500", 4.5, 234),
    ("Casual Kurti Set", "women", 599, 1299, "https://picsum.photos/seed/kurti/400/500", 4.3, 156),
    ("Formal Blazer", "women", 1499, 2999, "https://picsum.photos/seed/blazer/400/500", 4.6, 89),
    ("Ethnic Salwar Suit", "women", 1199, 2499, "https://picsum.photos/seed/salwar/400/500", 4.4, 312),
    ("Denim Jacket", "women", 1299, 2499, "https://picsum.photos/seed/denimjacket/400/500", 4.2, 178),
    ("Crop Top", "women", 399, 799, "https://picsum.photos/seed/croptop/400/500", 4.0, 445),
    ("Maxi Skirt", "women", 699, 1399, "https://picsum.photos/seed/maxiskirt/400/500", 4.3, 201),
    ("Night Gown Set", "women", 899, 1799, "https://picsum.photos/seed/nightgown/400/500", 4.1, 123),
]


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@stylehub.com', 'admin123', role='admin')
            self.stdout.write(self.style.SUCCESS('Admin user created: admin / admin123'))

        if not User.objects.filter(username='staff1').exists():
            User.objects.create_user('staff1', 'staff@stylehub.com', 'staff123', role='staff')
            self.stdout.write(self.style.SUCCESS('Staff user created: staff1 / staff123'))

        if not User.objects.filter(username='user1').exists():
            User.objects.create_user('user1', 'user@stylehub.com', 'user123', role='user')
            self.stdout.write(self.style.SUCCESS('User created: user1 / user123'))

        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Old products deleted!'))

        count = 0
        for name, cat, price, orig, img, rating, reviews in PRODUCTS:
            Product.objects.create(
                name=name, category=cat, price=price, original_price=orig,
                image_url=img, rating=rating, reviews_count=reviews, stock=50
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} products created!'))
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
