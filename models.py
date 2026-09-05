from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='book_covers/')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=499.00)
    stock = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.title

class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically track and reduce inventory stock upon order creation
        if self.pk is None:
            self.book.stock -= self.quantity
            self.book.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order by {self.customer_name} for {self.book.title}"
