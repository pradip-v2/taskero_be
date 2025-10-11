from django.db import models

from taskero_be.tenants.models import Tenant


class TenantTheme(models.Model):
    tenant = models.OneToOneField[Tenant](Tenant, on_delete=models.CASCADE)
    logo_short_sm = models.ImageField(upload_to="themes/logo_short_sm/")
    logo_short_lg = models.ImageField(upload_to="themes/logo_short_lg/")
    logo_long_sm = models.ImageField(upload_to="themes/logo_long_sm/")
    logo_long_lg = models.ImageField(upload_to="themes/logo_long_lg/")
    logo_square_sm = models.ImageField(upload_to="themes/logo_square_sm/")
    logo_square_lg = models.ImageField(upload_to="themes/logo_square_lg/")
    logo_circle_sm = models.ImageField(upload_to="themes/logo_circle_sm/")
    logo_circle_lg = models.ImageField(upload_to="themes/logo_circle_lg/")

    # fields for gradient color theme
    primary_gradient_color_1 = models.CharField(max_length=32, default="blue")
    primary_gradient_color_2 = models.CharField(max_length=32, default="grape")
    gradient_degree = models.IntegerField(default=142)

    # fields for fonts
    font_family = models.CharField(max_length=100, default="Arial")

    default_border_radius = models.IntegerField(default=8)

    # fields for shadows
    default_shadow = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tenant.name} theme"
