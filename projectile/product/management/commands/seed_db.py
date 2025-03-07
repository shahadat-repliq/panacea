from django.core.management.base import BaseCommand
from product.models import Product, ProductForm
from decimal import Decimal
import random


class Command(BaseCommand):
    help("Populate database with products")

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            help="Number of products to create",
            default=10,
            required=False,
        )

    def handle(self, *args, **kwargs):
        number_of_products = kwargs["number"]
        sample_titles = ["Tablet", "Syrup", "Injection", "Ointment", "Capsule"]
        sample_descriptions = [
            "A useful product for health.",
            "A popular medication form.",
            "Used for injections.",
            "A healing ointment for skin.",
            "A common product for medicinal purposes.",
        ]
        sample_images = [None]

        for _ in range(number_of_products):
            # Randomly select the product type
            product_type = random.choice(ProductForm.choices)[
                0
            ]  # 'TABLETS', 'SYRUP', etc.

            # Randomly generate data for each product
            title = random.choice(sample_titles)
            description = random.choice(sample_descriptions)
            image = random.choice(
                sample_images
            )  # Assume these are image paths you want to use
            unit_price = Decimal(
                random.uniform(10, 100)
            )  # Random price between 10 and 100
            quantity = random.randint(1, 50)  # Random quantity between 1 and 50
            is_active = random.choice(
                [True, False]
            )  # Randomly choose if the product is active

            # Create the product
            product = Product.objects.create(
                title=title,
                description=description,
                image=image,  # Make sure the image file exists in the given path
                unit_price=unit_price,
                quantity=quantity,
                is_active=is_active,
                type=product_type,
            )

            # Log output to confirm each product created
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created product: {product.title}")
            )

            # Final message
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated {number_of_products} products in the database."
            )
        )
