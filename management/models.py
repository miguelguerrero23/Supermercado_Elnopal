import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from personal.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u"Nombre", blank=False, db_column="Nombre")
    status = models.BooleanField(default=True, db_column="Status")
    def __str__(self) -> str:
        return ' %s' %(self.name)
    def clean(self):
        self.name = self.name.title()
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        
class Subcategory(models.Model):
    name = models.CharField(max_length=50,  unique=True, verbose_name=u"Nombre", blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name=u"Categoría")
    image = models.ImageField(upload_to='subcategory', null=True, verbose_name=u"Imagen", default='subcategory/Logo.png')
    status = models.BooleanField(default=True)
    def __str__(self) -> str:
        return ' %s' %(self.name)
    def clean(self):
        self.name = self.name.title()
    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"

class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"Nombre", blank=False, db_column="Nombre")
    status = models.BooleanField(default=True)
    def __str__(self) -> str:
        return (self.name)
    def clean(self):
        self.name = self.name.title()
    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

class Product(models.Model):
    name = models.CharField(max_length=50,  unique=True, verbose_name=u"Nombre", blank=False)
    price = models.FloatField(blank=False, verbose_name=u"Precio")
    description = models.TextField(max_length=150, blank=True, verbose_name=u"Descripción")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, verbose_name=u"Subcategoría")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name=u"Marca")
    class UMeasurement(models.TextChoices):
        unit = 'unit', _('Unidad')
        pound = 'pound', _('Lb')
        kilogram ='kilogram', _('Kg')
        litre = 'litre',_('L')
    unitMeasurement = models.CharField(max_length=30, choices=UMeasurement.choices, default=UMeasurement.unit, verbose_name="Unidad de medida")
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1)], blank=False, null=True, verbose_name=u"Stock")
    image = models.ImageField(upload_to='product', null=True, verbose_name=u"Imagen", default='product/Logo.png')
    status = models.BooleanField(default=True)
    def __str__(self) -> str:
        return ' %s' %(self.name)
    def clean(self):
        self.name = self.name.title()
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    
class Provider(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"Nombre", blank=False)
    phone = models.CharField(max_length=10, verbose_name=u"Teléfono", blank=True)
    email = models.EmailField(max_length=254, verbose_name=u"Correo Electrónico")
    status = models.BooleanField(default=True)
    def __str__(self) -> str:
        return (self.name)
    def clean(self):
        self.name = self.name.title()
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        
class Payment(models.TextChoices):
        dtf = 'Datáfono', _('Datafono')
        eft = 'Efectivo', _('Efectivo')
        tsc = 'Transacción', _('Transaccion')
class Status(models.TextChoices):
        ABIERTA='Abierta', _('Abierta')
        CERRADA='Cerrada', _('Cerrada')
        ANULADA='Anulada', _('Anulada')
        
class Buy(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Compra")
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, verbose_name=u"Proveedor")
    payment = models.CharField(max_length=11, choices=Payment.choices, default=Payment.eft, verbose_name=u"Método de Pago", blank=False)
    finalPrice = models.IntegerField(default=0, null=False, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, verbose_name="Estado", default=Status.ABIERTA)
    statusBuy = models.BooleanField(default=True)
    def __str__(self) -> str:
        return ' %s' %(self.date)
    class Meta:
        verbose_name="Compra"
        verbose_name_plural = "Compras"
        
class DetailBuy(models.Model):
    buy = models.ForeignKey(Buy, on_delete=models.SET_NULL, null=True, verbose_name=u"Id Compra")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,verbose_name=u"Producto")
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=1, verbose_name=u"Cantidad")
    total = models.IntegerField(default=0, null=False, blank=True)
    status = models.BooleanField(default=True, verbose_name="Estado")
    class Meta:
        verbose_name="Detalle de compra"
        verbose_name_plural = "Detalle de compras"
        
class Sale(models.Model):
    date = models.DateField(auto_now=True, verbose_name="Fecha de Venta")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=u"Empleado")
    client = models.CharField(blank=True, null=False, max_length=50, verbose_name=u"Cliente", default=u"Cliente local")
    nDocument = models.CharField(blank=True, null=False, max_length=20, verbose_name=u"Número de Documento / NIT", default=1234567890)
    address = models.CharField(blank=True, null=False, verbose_name=u"Dirección", max_length=254, default=u"Local")
    class TypeSale(models.TextChoices):
        store = 'store', _('Local')
        address = 'Domicilio', _('Domicilio')
    typeSale = models.CharField(max_length=9, choices=TypeSale.choices, default=TypeSale.store, verbose_name=u"Tipo de Venta")
    finalPrice = models.IntegerField(default=0, null=False, blank=True)
    payment = models.CharField(max_length=11, choices=Payment.choices, default=Payment.eft, verbose_name=u"Método de Pago", blank=False)
    status = models.CharField(max_length=10, choices=Status.choices, verbose_name="Estado", default=Status.ABIERTA)
    statusSale = models.BooleanField(default=True)
    def __str__(self) -> str:
        return ' %s' %(self.date)
    def clean(self):
        self.client = self.client.title()
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        
class DetailSale(models.Model):
    date = models.DateField(auto_now=True, verbose_name="Fecha de Venta")
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, verbose_name=u"Id Venta")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,verbose_name=u"Producto")
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=1, verbose_name=u"Cantidad")
    total = models.IntegerField(default=0, null=False, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, verbose_name="Estado", default=Status.ABIERTA)
    class Meta:
        verbose_name="Detalle de venta"
        verbose_name_plural = "Detalle de ventas"
        
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.sql']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Archivo no válido')

class Backup(models.Model):
    name = models.CharField(max_length = 200,default="Copia de Seguridad", blank=True)
    file = models.FileField(upload_to="backup",validators=[validate_file_extension])
    date = models.DateTimeField(auto_now = True)
