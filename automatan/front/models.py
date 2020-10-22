from django.db import models


class CarNames(models.Model):
    # id = models.TextField(db_column='Id', blank=True,
    #                       primary_key=True)
    brand_name = models.TextField(
        db_column='brand_name', blank=True, null=True)
    model_link = models.TextField(
        db_column='model_link', blank=True, null=True)
    model_name = models.CharField(
        db_column='model_name', blank=True, null=False, max_length=30)
    quantity = models.IntegerField(db_column='quantity', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_names'

    # def query_list(self):
    #     query_list_res = ob
    #     return query_list_res


class Cars(models.Model):
    id = models.IntegerField(db_column='car_id', unique=True, blank=True,
                             null=False, primary_key=True)
    brand = models.TextField(db_column='brand', blank=True, null=True)
    model = models.TextField(db_column='model', blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    discripton = models.TextField(blank=True, null=True)
    posting_date = models.TextField(blank=True, null=True)
    add_to_db_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cars'


# car_id = models.IntegerField(unique=True, blank=True, null=True)
#     brand = models.TextField(blank=True, null=True)
#     model = models.TextField(blank=True, null=True)
#     year = models.IntegerField(blank=True, null=True)
#     location = models.TextField(blank=True, null=True)
#     price = models.IntegerField(blank=True, null=True)

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
