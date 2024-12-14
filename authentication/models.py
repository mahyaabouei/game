from django.db import models
from django.contrib.auth.models import User

class Otp(models.Model):
    code = models.CharField(max_length=6)
    mobile = models.CharField(max_length=11)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.code
    

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    agent = models.CharField(max_length= 200 , null=True, blank=True )
    email = models.EmailField( null=True, blank=True)
    mobile = models.CharField(max_length=14)
    status = models.CharField(max_length=150 , null=True, blank=True)
    type = models.CharField(max_length=200)
    uniqueIdentifier = models.CharField(max_length=150 , unique=True)
    
    def __str__(self):
        return self.mobile
    

class Accounts (models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    accountNumber = models.CharField(max_length=200)
    bank = models.CharField(max_length=200)
    branchCity = models.CharField( max_length=200, null=True, blank=True)
    branchCode = models.CharField(max_length=20, null=True, blank=True)
    branchName = models.CharField(max_length=200, null=True, blank=True)
    isDefault = models.CharField( max_length=200, null=True, blank=True)
    modifiedDate = models.CharField( max_length=200, null=True, blank=True)
    type = models.CharField(max_length= 200, null=True, blank=True)
    sheba = models.CharField(max_length= 200)
    def __str__(self):
        return f'{self.accountNumber} {self.bank} {self.branchName}'




class Addresses (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    alley = models.CharField(max_length=1000 ,  blank=True , null= True)
    city = models.CharField(max_length=1000 ,  blank=True , null= True)
    cityPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    country =models.CharField(max_length=1000 ,  blank=True , null= True)
    countryPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    email = models.EmailField ( blank=True , null= True)
    emergencyTel =  models.CharField(max_length=1000 ,  blank=True , null= True) 
    emergencyTelCityPrefix =  models.CharField(max_length=1000 ,  blank=True , null= True)
    emergencyTelCountryPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    fax = models.CharField(max_length=1000 ,  blank=True , null= True)
    faxPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    mobile = models.CharField(max_length=1000 ,  blank=True , null= True)
    plaque = models.CharField(max_length=1000 ,  blank=True , null= True)
    postalCode = models.CharField(max_length=1000 ,  blank=True , null= True)
    province = models.CharField(max_length=1000 ,  blank=True , null= True)
    remnantAddress = models.CharField(max_length=1000 ,  blank=True , null= True)
    section =models.CharField(max_length=1000 ,  blank=True , null= True)
    tel =  models.CharField(max_length=1000 ,  blank=True , null= True)
    website = models.CharField(max_length=1000 ,  blank=True , null= True)
    def __str__(self):
        return f'{self.city} {self.country} {self.email}'




class JobInfo (models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)                   
    companyAddress = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyCityPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyEmail = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyFax =  models.CharField(max_length=1000 ,  blank=True , null= True)
    companyFaxPrefix = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyName = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyPhone = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyPostalCode = models.CharField(max_length=1000 ,  blank=True , null= True)
    companyWebSite = models.CharField(max_length=1000 ,  blank=True , null= True)
    employmentDate = models.CharField(max_length=1000 ,  blank=True , null= True)
    job = models.CharField(max_length=1000 ,  blank=True , null= True)
    jobDescription = models.CharField(max_length=1000 ,  blank=True , null= True)
    position = models.CharField(max_length=1000 ,  blank=True , null= True)
    def __str__(self):
        return f'{self.companyName} {self.job} {self.position}' 


class PrivatePerson (models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birthDate = models.CharField(max_length=255, blank=True)
    fatherName = models.CharField(max_length=255, blank=True)
    firstName = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=255, blank=True)
    placeOfBirth = models.CharField(max_length=255, blank=True)
    placeOfIssue = models.CharField(max_length=255, blank=True)
    seriSh = models.CharField(max_length=255, blank=True)
    serial = models.CharField(max_length=255, blank=True)
    shNumber = models.CharField(max_length=255, blank=True)
    signatureFile = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class TradingCodes (models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
    firstPart =  models.CharField(max_length=200)
    secondPart  = models.CharField(max_length=200 , null=True, blank=True)
    thirdPart = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f'{self.code}'

