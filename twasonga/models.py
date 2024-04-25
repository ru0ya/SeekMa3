from django.db import models
from django.utils import timezone


class Bus(models.Model):
    ROUTE_CHOICES = [ 
                     ("1", "Nairobi-Makongeni"),
                     ("2",  "Nairobi-Thika"),
                     ("3", "Nairobi-Juja"),
                     ("4", "Nairobi-Kikuyu"),
                     ("5", "Nairobi-Kitengela")
                     ]
    num_plate = models.CharField(max_length=10)
    price = models.DecimalField(decimal_places=2, max_digits=4)
    seats = models.IntegerField()
    route = models.CharField(max_length=50, choices=ROUTE_CHOICES, default="Nairobi-Juja")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.num_plate

    class Meta:
        ordering = ['num_plate']


class Booking(models.Model):
    STATUS_CHOICES = [
            ("Full", "Full"),
            ("Boarding", "Boarding"),
            ("In Transit", "In Transit"),
            ("Cancelled", "Cancelled"),
            ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    customer = models.CharField(max_length=80)
    seat = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    departure = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='Boarding'
            )

    def __str__(self):
        return self.customer

    class Meta:
        ordering = ['customer']
