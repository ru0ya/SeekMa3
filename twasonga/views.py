import random
from datetime import timedelta, datetime
from django.utils import timezone
# from datetime import datetime
from twasonga.models import Booking, Bus
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        session_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')

        response = ""

        if text == "":
            response = "CON Karibu! \n Which service would you like to access? \n"
            response += "1. List all buses \n"
            response += "2. Check ticket status \n"
            response += "3. Book a bus seat \n"
            response += "4. Cancel a booking \n"
            response += "5. Report an issue"

        elif text == "1":
            results = Bus.objects.all()
            for i in results:
                response += f"END {i}: {i.is_available} {i.num_plate} \n \n"

        elif text == "2":
            response = "CON Choose an option \n"
            response += "1. All tickets \n"
            response += "2. Today active tickets"

        elif text == '2*1':
            tickets = Booking.objects.filter(
                    customer=phone_number
                    )
            for tkt in tickets:
                response += f"END Ticket {tkt.id} on \
                        {tkt.departure:%Y-%m-%d %H:%M:%S}"

        elif text == '2*2':
            now = timezone.now()
            tickets = Booking.objects.filter(
                    customer=phone_number,
                    departure=now
                    )

            if tickets:
                print('tikiti')
                for tkt in tickets:
                    response += f"END Ticket {tkt.id} on\
                            {tkt.departure:%Y-%m-%d %H:%M:%S}"
            else:
                response = 'END No tickets found'

        elif text == '3':
            response = "CON Okay, pick a route \n"
            response += "1. Nairobi-Makongeni \n"
            response += "2. Nairobi-Thika \n"
            response += "3. Nairobi-Juja \n"
            response += "4. Nairobi-Kikuyu \n"
            response += "5. Nairobi-Kitengela"

        elif text == '3*1' or text == '3*2' or text == '3*3' or text == '3*4'\
                or text == '3*5':
            # assuming each bus has a capacity of 37 seats
            seat = random.randint(1, 37)
            buses = Bus.objects.filter(is_available=True)

            if buses.exists():
                bus = buses.first()
                departure = timezone.now() + timedelta(hours=1)
                # available_seats = bus.seats
                # check if there are available seats
                if bus.seats > 0:
                    new_booking = Booking.objects.create(
                            bus=bus,
                            customer=phone_number,
                            seat=seat,
                            departure=departure
                            )
                    bus.seats -= 1
                    bus.save()
                    response = f"END Here is your booking info: \n TICKET \
                            NO {new_booking.id} \n Bus Number is {bus} \
                            \n Your seat number is {seat} \n Your bus leaves \
                            at {departure:%H:%M:%S}"

                    # check if all seats are booked
                    if bus.seats == 0:
                        bus.is_available = False
                        bus.save()
                else:
                    response = "END Sorry, no seats available on this bus."
            else:
                response = "END No buses available for this route."

        elif text == "4":
            response = "END Work in progress, check again soon"
        elif text == "5":
            response = "END Work in progress, check again soon"

        return HttpResponse(response)
