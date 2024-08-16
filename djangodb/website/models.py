from django.db import models

class Member(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)    
    email = models.EmailField(max_length=200)
    passwd = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self) -> str:
        return self.fname + ' ' + self.lname
    

class CSVFile(models.Model):
    file = models.FileField(upload_to='csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.file.name

class Audit(models.Model):
    asin = models.CharField(max_length=20)
    brand_name = models.CharField(max_length=20)
    generic_name = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    availablity = models.CharField(max_length=20)
    browser_node = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    reviews = models.CharField(max_length=20)
    rating = models.CharField(max_length=20)
    deal = models.CharField(max_length=20)
    sold_by = models.CharField(max_length=20)
    buybox = models.CharField(max_length=20)
    image_len = models.CharField(max_length=20)
    main_img_url = models.CharField(max_length=20)
    bullet_point_len = models.CharField(max_length=20)
    bsr1 = models.CharField(max_length=20)
    bsr2 = models.CharField(max_length=20)   
    price = models.CharField(max_length=20)
    MRP = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    A_plus = models.CharField(max_length=20)
    store_link = models.CharField(max_length=20)

    
    def __str__(self):
        return self.file.name
  