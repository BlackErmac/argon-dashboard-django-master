from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from ..transportation.models import Car , Driver , Task , Notification , Route
import json

@login_required(login_url="/login/")
def index(request):
    cars_info = Car.get_count()
    drivers_info = Driver.get_count()
    tasks_info = Task.get_count()
    notification_info = Notification.get_count()

    routes = Route.objects.all()
    route_data = [
        {
            "start": {"lat": route.start_point.latitude, "lng": route.start_point.longitude, "name": route.start_point.name},
            "end": {"lat": route.end_point.latitude, "lng": route.end_point.longitude, "name": route.end_point.name},
            "distance": route.distance_km
        }
        for route in routes
    ]


    map = render(request, "transportation/routes_map.html", {"routes": json.dumps(route_data)}).content.decode("utf-8")

    return render(request, 'home/index.html', {'cars_info':cars_info ,
                                            'drivers_info':drivers_info ,
                                            'tasks_info':tasks_info,
                                            'notification_info':notification_info,
                                            'map':map})

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
