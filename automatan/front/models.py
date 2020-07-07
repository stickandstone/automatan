from django.db import models


class CarNames(models.Model):
    id = models.TextField(db_column='Id', blank=True,
                          primary_key=True)
    brand_name = models.TextField(
        db_column='Brand_name', blank=True, null=True)
    model_link = models.TextField(
        db_column='Model_Link', blank=True, null=True)
    model_name = models.TextField(
        db_column='Model_name', blank=True, null=True)
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_names'

    # def __str__(self):
    #     return self.model_name


class Cars(models.Model):
    id = models.IntegerField(unique=True, blank=True,
                             null=False, primary_key=True)
    brand = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    engine_power = models.TextField(
        db_column='engine power', blank=True, null=True)
    # Field renamed to remove unsuitable characters.
    fuel_type = models.TextField(db_column='fuel type', blank=True, null=True)
    gearbox = models.TextField(blank=True, null=True)
    transmission = models.TextField(blank=True, null=True)
    milage = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'

    # def __str__(self):
    #     return self.cars


class Manufactories(models.Model):
    id = models.TextField(blank=True, null=False, primary_key=True)
    company_link = models.TextField(blank=True, null=True)
    company_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manufactories'

    def __str__(self):
        return self.company_name

    def get_list_ofLetters(self, company_name):

        list_ofLetters = []
        for i in company_name:
            i = str(i)
            if i[0] not in list_ofLetters:
                list_ofLetters.append(i[0])
        return list_ofLetters
