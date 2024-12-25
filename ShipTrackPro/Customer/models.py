from django.db import models



class ExcelSheet(models.Model):
    volume = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    tankPressure = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    toGoMt = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    rate = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE,null=True,blank=True)
class Order(models.Model):
    customer = models.ForeignKey('signup.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Supplier.Product', on_delete=models.CASCADE)

    # documents
    billsOfLading = models.FileField(upload_to='billsOfLading/',null=True,blank=True)
    customDocumentation = models.FileField(upload_to='customDocumentation/',null=True,blank=True)
    exportDeclaration = models.FileField(upload_to='exportDeclaration/',null=True,blank=True)
    shippingManifest = models.FileField(upload_to='shippingManifest/',null=True,blank=True)
    vesselInformation = models.FileField(upload_to='vesselInformation/',null=True,blank=True)
    sealContainerNumber = models.FileField(upload_to='sealContainerNumber/',null=True,blank=True)
    diagram = models.FileField(upload_to='diagrams/',null=True,blank=True)
    # create a new table for excel sheet with the fields required and on viewing download csv file
    # show a table for updating excel sheet
    
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default="Order Placed")
    address = models.CharField(max_length=100,default="")
    oilReqSent = models.BooleanField(default=False)
    oilFilled = models.BooleanField(default=False)
    customReqSent = models.BooleanField(default=False)
    customTax = models.IntegerField(default=-1)
    customTaxSent = models.BooleanField(default = False)
    shipReqSent = models.BooleanField(default=False)
    shippingCost = models.IntegerField(default=-1)
    shippingCostSent = models.BooleanField(default = False)
    shippingCostVerified = models.BooleanField(default = False)
    tankerPicked = models.BooleanField(default=False)
    tankerDropedAtPort = models.BooleanField(default=False)
    customCleared = models.BooleanField(default=False)
    tankerDispatched = models.BooleanField(default=False)
    orderRecieved = models.BooleanField(default=False)
    total = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.customer.user.username} ordered {self.product.name} on {self.date} with status {self.status}"