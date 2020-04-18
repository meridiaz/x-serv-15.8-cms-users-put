from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.contrib.auth import logout

from .models import Contenido, Comentario

@csrf_exempt
def get_content(request, llave):
    if request.method == "PUT":
        valor = request.body.decode('utf-8')
    elif request.method == "POST":
        action = request.POST['action']
        if action == "Enviar Contenido":
            valor = request.POST['valor']
    if request.method == "PUT" or (request.method == "POST" and action == "Enviar Contenido"):
        try:
            c = Contenido.objects.get(clave=llave)
            c.valor = valor
        except Contenido.DoesNotExist:
            c = Contenido(clave=llave, valor=valor)
        c.save()
    if request.method == "POST" and action == "Enviar Comentario":
            c = get_object_or_404(Contenido, clave=llave)
            titulo = request.POST['titulo']
            cuerpo = request.POST['cuerpo']
            q = Comentario(contenido=c, titulo=titulo, cuerpo=cuerpo, fecha=timezone.now())
            q.save()

    contenido = get_object_or_404(Contenido, clave=llave)
    context = {'contenido': contenido, 'user': request.user}
    return render(request, 'cms/content.html', context)

@csrf_exempt
def index(request):
    content_list = Contenido.objects.all()
    context = {
        'content_list': content_list,
    }
    return render(request, 'cms/index.html', context)

def logout_view(request):
    logout(request)
    return redirect("/cms/")
