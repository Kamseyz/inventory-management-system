from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

# Regex to ensure no leading spaces and at least one character
no_leading_space_validator = RegexValidator(
    r'^\S.*$',
    'The name cannot begin with a space.',
    code='invalid_name'
)


#Product
class ProductModel(models.Model):
    
    class ProductStatus(models.TextChoices):
        IN_STOCK= 'in-stock', 'In-Stock'
        OUT_OF_STOCK = 'out-of-stock', 'Out-of-stock'
        PREORDER= 'preorder', 'Preorder'
        LOWSTOCK = 'lowstock', 'Lowstock'
        
    name = models.CharField(
    unique=True,
    max_length=100,
    validators=[
        no_leading_space_validator,
        MinLengthValidator(3)
    ],
    error_messages={
        'unique': "This product name already exists.",
    }
)
    
    
    status = models.CharField(12, choices=ProductStatus.choices, default=ProductStatus.IN_STOCK)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    
    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.status = self.ProductStatus.OUT_OF_STOCK
        elif self.quantity <= 5:
            self.status = self.ProductStatus.LOWSTOCK
        else:
            self.status = self.ProductStatus.IN_STOCK
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name} is {self.status} and it has a quantity of {self.quantity}'
    
    class Meta:
        ordering = ['-timestamp']
    
    

#ORDERS

class OrdersModel(models.Model):
    product_name = models.ForeignKey(ProductModel, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.product_name} was ordered by {self.ordered_by} at {self.ordered_at}'