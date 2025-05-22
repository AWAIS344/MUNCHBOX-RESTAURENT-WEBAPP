from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Cuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")
    description = models.TextField()
    image=models.ImageField()

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    manager_name = models.CharField(max_length=100)
    manager_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    DELIVERY_PICKUP_CHOICES = [
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
        ('both', 'Delivery & Pickup'),
    ]
    delivery_pickup = models.CharField(max_length=20, choices=DELIVERY_PICKUP_CHOICES)
    cuisines = models.ManyToManyField(Cuisine)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)  # e.g., "Home", "Work"
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    cross_street = models.CharField(max_length=200, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('amex_express', 'Amex Express Checkout')
    ])
    brand = models.CharField(max_length=20, blank=True, choices=[
        ('visa', 'Visa'), ('mastercard', 'MasterCard'), ('amex', 'American Express'), ('discover', 'Discover')
    ])
    last_4 = models.CharField(max_length=4, blank=True)
    exp_month = models.IntegerField(blank=True, null=True)
    exp_year = models.IntegerField(blank=True, null=True)
    paypal_email = models.EmailField(blank=True)
    token = models.CharField(max_length=100, blank=True)  # Token from payment gateway
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_method_display()} - {self.user.username}"
    
class GiftCard(models.Model):
    code = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gift Card - {self.code}"
    
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    # Delivery address
    delivery_street = models.CharField(max_length=200)
    delivery_city = models.CharField(max_length=100)
    delivery_state = models.CharField(max_length=100)
    delivery_zip_code = models.CharField(max_length=20)
    delivery_country = models.CharField(max_length=100)
    delivery_latitude = models.FloatField(null=True, blank=True)
    delivery_longitude = models.FloatField(null=True, blank=True)
    delivery_phone = models.CharField(max_length=20, blank=True)
    delivery_cross_street = models.CharField(max_length=200, blank=True)
    delivery_instructions = models.TextField(blank=True)
    # Financials
    items_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    gift_card_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promo_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # After discounts
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tip_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Payment
    payment_type = models.CharField(max_length=20, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')])
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery_time = models.CharField(max_length=50, blank=True)  # e.g., "9:00pm-9:10pm"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate a unique order number, e.g., based on timestamp and ID
            self.order_number = f"ORD{self.id or Order.objects.count() + 1:015d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username} from {self.restaurant.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.restaurant.name}"

class BlogReview(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.blog_post.title}"