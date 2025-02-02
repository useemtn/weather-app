import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import Pais, Frontera, Temperatura
from .forms import BuscarPaisForm
import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string  
import xml.etree.ElementTree as ET


"""

Funciones de la app

"""
def index(request):
    """
    
    Muestra la página principal de la app.

    """
    return render(request, 'temperaturas_app/index.html')
def borrar_bd(request):
    """
    
    Borra la base de datos

    """
    if request.method == 'POST':
        Pais.objects.all().delete()
        Frontera.objects.all().delete()
        Temperatura.objects.all().delete()
        return HttpResponse("Base de datos borrada.<br><a href='/'>Volver</a>")
    return render(request, 'borrar_bd.html')

def insertar_paises(request):
    """
    
    Inserta paises en la base de datos obteniendolos de la api

    """
    if request.method == 'POST':
        try:
            # Obtener datos de la API
            url = "https://restcountries.com/v3.1/region/europe"
            response = requests.get(url)
            data = response.json()

            # Insertar países en la base de datos
            for pais_data in data:
                Pais.objects.get_or_create(
                    cca2=pais_data.get("cca2", ""),
                    cca3=pais_data.get("cca3", ""),
                    defaults={
                        "nombre": pais_data.get("name", {}).get("common", ""),
                        "capital": pais_data.get("capital", [""])[0],
                        "region": pais_data.get("region", ""),
                        "subregion": pais_data.get("subregion", ""),
                        "miembroUE": pais_data.get("unMember", False),
                        "latitud": pais_data.get("latlng", [None, None])[0],
                        "longitud": pais_data.get("latlng", [None, None])[1],
                    }
                )
            return HttpResponse("Países insertados correctamente.<br><a href='/'>Volver</a>")
        except Exception as e:
            return HttpResponse(f"Error al insertar países: {str(e)}. <br><a href='/'>Volver</a>")
    return render(request, 'insertar_paises.html')

def insertar_fronteras(request):
    """
    
    Inserta las fronteras en la base de datos mediante la api

    """
    if request.method == 'POST':
        if not Pais.objects.exists():
            return HttpResponse("Error: Primero debes insertar los países.<br><a href='/'>Volver</a>", status=400)
        try:
            # Obtener todos los países de la base de datos
            paises = Pais.objects.all()

            # Insertar fronteras
            for pais in paises:
                # Obtener datos de la API para el país actual
                url = f"https://restcountries.com/v3.1/alpha/{pais.cca3}"
                response = requests.get(url)
                data = response.json()

                # Obtener las fronteras del país
                fronteras = data[0].get("borders", [])

                # Insertar cada frontera en la base de datos
                for frontera_cca3 in fronteras:
                    Frontera.objects.get_or_create(
                        idpais=pais,
                        cca3_frontera=frontera_cca3
                    )
            return HttpResponse("Fronteras insertadas correctamente.<br><a href='/'>Volver</a>")
        except Exception as e:
            # Manejar cualquier otra excepción
            return HttpResponse(f"Error al insertar fronteras: {str(e)}. <br><a href='/'>Volver</a>", status=500)
    return render(request, 'insertar_fronteras.html')

def insertar_temperaturas(request):
    """
    
    Insertar temperaturas en la base de datos obteniéndolas de la API (mitad en JSON, mitad en XML).
    
    """
    if request.method == 'POST':
        if not Pais.objects.exists():
            return HttpResponse("Error: Primero debes insertar los países.<br><a href='/'>Volver</a>", status=400)

        try:
            paises = list(Pais.objects.all())
            api_key = "a60fef3fc371c50c0c57c17361925fad"
            mitad = len(paises) // 2  # Dividir en dos mitades

            # Función para insertar la temperatura en la base de datos
            def guardar_temperatura(pais, datos):
                Temperatura.objects.create(
                    idpais=pais,
                    timestamp=datetime.datetime.now(),
                    temperatura=datos.get('temperatura'),
                    sensacion=datos.get('sensacion'),
                    minima=datos.get('minima'),
                    maxima=datos.get('maxima'),
                    humedad=datos.get('humedad'),
                    amanecer=datos.get('amanecer'),
                    atardecer=datos.get('atardecer')
                )

            # 1. Obtener datos en formato JSON
            for pais in paises[:mitad]:
                if pais.latitud and pais.longitud:
                    url = f"http://api.openweathermap.org/data/2.5/weather?lat={pais.latitud}&lon={pais.longitud}&appid={api_key}&units=metric"
                    response = requests.get(url)
                    data = response.json()

                    datos_climaticos = {
                        'temperatura': data["main"]["temp"],
                        'sensacion': data["main"]["feels_like"],
                        'minima': data["main"]["temp_min"],
                        'maxima': data["main"]["temp_max"],
                        'humedad': data["main"]["humidity"],
                        'amanecer': datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).time(),
                        'atardecer': datetime.datetime.fromtimestamp(data["sys"]["sunset"]).time(),
                    }

                    guardar_temperatura(pais, datos_climaticos)

            # 2. Obtener datos en formato XML
            for pais in paises[mitad:]:
                if pais.latitud and pais.longitud:
                    url = f"http://api.openweathermap.org/data/2.5/weather?lat={pais.latitud}&lon={pais.longitud}&appid={api_key}&mode=xml&units=metric"
                    response = requests.get(url)
                    root = ET.fromstring(response.content)

                    temperatura = root.find('temperature').attrib.get('value')
                    sensacion = root.find('feels_like').attrib.get('value')
                    minima = root.find('temperature').attrib.get('min')
                    maxima = root.find('temperature').attrib.get('max')
                    humedad = root.find('humidity').attrib.get('value')

                    # Convertir el amanecer y atardecer a objetos de tiempo
                    amanecer_str = root.find('city/sun').attrib.get('rise')
                    atardecer_str = root.find('city/sun').attrib.get('set')
                    amanecer = datetime.datetime.fromisoformat(amanecer_str).time()
                    atardecer = datetime.datetime.fromisoformat(atardecer_str).time()

                    datos_climaticos = {
                        'temperatura': float(temperatura),
                        'sensacion': float(sensacion),
                        'minima': float(minima),
                        'maxima': float(maxima),
                        'humedad': int(humedad),
                        'amanecer': amanecer,
                        'atardecer': atardecer,
                    }

                    guardar_temperatura(pais, datos_climaticos)

            return HttpResponse("Temperaturas insertadas correctamente.<br><a href='/'>Volver</a>")

        except Exception as e:
            return HttpResponse(f"Error al insertar temperaturas: {str(e)}.<br><a href='/'>Volver</a>", status=500)

    return render(request, 'insertar_temperaturas.html')

def obtener_temperaturas(request):
    """
    
    Muestra todas las temperaturas de la base de datos

    """
    if request.method == 'POST':
        try:
            # Obtener todas las temperaturas de la base de datos
            temperaturas = Temperatura.objects.all()

            # Renderizar las temperaturas 
            html = render_to_string('temperaturas_app/temperaturas.html', {
                'temperaturas': temperaturas,
            })

            return JsonResponse({'html': html})  # Devuelve el HTML en formato JSON
        except Exception as e:
            return JsonResponse({'html': f'<p>Error al obtener temperaturas: {str(e)}</p>'})
    return JsonResponse({'html': '<p>Método no permitido.</p>'})
def mostrar_temperatura(request):
    """
    
    Muestra la temperatura del país buscado en el formulario junto con sus fronteras y tenmperaturas

    """
    if request.method == 'POST':
        form = BuscarPaisForm(request.POST)
        if form.is_valid():
            nombre_pais = form.cleaned_data['nombre_pais']
            pais = Pais.objects.filter(nombre=nombre_pais).first()

            if pais:
                # Temperatura del país principal
                temperaturas = Temperatura.objects.filter(idpais=pais).order_by('-timestamp')
                
                # Obtener las fronteras del país
                fronteras = Frontera.objects.filter(idpais=pais)
                
                # Temperaturas de los países fronterizos
                temperaturas_fronteras = []
                for frontera in fronteras:
                    pais_frontera = Pais.objects.filter(cca3=frontera.cca3_frontera).first()
                    if pais_frontera:
                        temp_frontera = Temperatura.objects.filter(idpais=pais_frontera).order_by('-timestamp').first()
                        if temp_frontera:
                            temperaturas_fronteras.append({
                                'pais': pais_frontera,
                                'temperatura': temp_frontera
                            })

                # Renderizar resultados
                html = render_to_string('temperaturas_app/resultados.html', {
                    'pais': pais,
                    'temperaturas': temperaturas,
                    'fronteras': fronteras,
                    'temperaturas_fronteras': temperaturas_fronteras,
                })
                return JsonResponse({'html': html})
            else:
                return JsonResponse({'html': '<p>País no encontrado.</p>'})
        else:
            return JsonResponse({'html': '<p>Formulario no válido.</p>'})
    return JsonResponse({'html': '<p>Método no permitido.</p>'})