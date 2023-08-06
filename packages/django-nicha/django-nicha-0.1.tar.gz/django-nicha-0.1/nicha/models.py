from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.
# business_status = (('PENDING','PENDING'),('ACTIVE','ACTIVE'))
# branch_status = (('PENDING','PENDING'),('ACTIVE','ACTIVE'))
# social_account_type = (('FACEBOOK','FACEBOOK'),('TWITTER','TWITTER'),('YOUTUBE','YOUTUBE'),('INSTAGRAM','INSTAGRAM'))

# def cover_directory_path(instance,filename):
# 	return 'covers/cover_{0}'.format( filename)

# def logo_directory_path(instance,filename):
# 	return 'logos/logo_{0}'.format( filename)

# class Branch(models.Model):
# 	branch_ref = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
# 	business=models.ForeignKey(Business,on_delete=models.CASCADE)
# 	address = models.OneToOneField(Address)
# 	branch_status = models.CharField(blank=True,null=True,choices=business_status,default="PENDING",max_length=20)
# 	cover_1=models.ImageField(null=True,blank=True,upload_to=cover_directory_path) 
# 	cover_2=models.ImageField(null=True,blank=True,upload_to=cover_directory_path)
# 	cover_3=models.ImageField(null=True,blank=True,upload_to=cover_directory_path)
# 	cover_4=models.ImageField(null=True,blank=True,upload_to=cover_directory_path)
# 	cover_5=models.ImageField(null=True,blank=True,upload_to=cover_directory_path)
# 	def __str__(self):
# 		return self.business.name


