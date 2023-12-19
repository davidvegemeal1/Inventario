from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Image
from io import BytesIO
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, inventarioform
from django.db import IntegrityError
from .models import monitoreo_del_conteo, login_escritorio
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import hashlib
import os

# Create your views here.

def iniciar(request):
     if request.method == 'GET':
         return render(request, 'iniciar.html', {
            'form': AuthenticationForm
        })
     else:
        user= authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'iniciar.html', {
                'form': AuthenticationForm,
                'error':'Usuario o Contraseña Incorrecta'
            })
        else:
            login(request, user)
            return redirect('principal')

@login_required
def salir(request):
    logout(request)
    return redirect('iniciar')

        
def home(request):
    usuarios=User.objects.all()
    return render(request, 'home.html',{'usuarios': usuarios} )

def somos(request):
    return render(request, 'somos.html')

@login_required
def principal(request):
    if request.user.is_superuser:    
        inventario= monitoreo_del_conteo.objects.all()
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')

        if year:
            inventario = inventario.filter(fecha__year=year)

        if month:
            inventario = inventario.filter(fecha__month=month)

        if day:
            inventario = inventario.filter(fecha__day=day)

        if not inventario.exists():
            inventario = None

        return render(request, 'principalAD.html', {'inventario': inventario})

    else:
        inventario=monitoreo_del_conteo.objects.filter(user=request.user)
        return render(request, 'principalUS.html', {'inventario':inventario} )        

@login_required
@user_passes_test(lambda u: u.is_superuser)

def delete_pan (request, pan_id):
    inventario= get_object_or_404(monitoreo_del_conteo, pk=pan_id)
    if request.method =='POST':
        inventario.delete()
        return redirect ('home')


@login_required       
@user_passes_test(lambda u: u.is_superuser)

def editar(request, pan_id):
    usuarios=User.objects.all()
    inventario= get_object_or_404(monitoreo_del_conteo, pk=pan_id)
    if request.method == 'POST':
        formulario = inventarioform(request.POST, instance=inventario)
        if formulario.is_valid():
            formulario.save()
            return redirect('principal')
    else:
        formulario = inventarioform(instance=inventario)

    return render(request, 'editar.html', {'formulario': formulario, 'usuarios': usuarios})



@login_required
def crear(request):
    if request.method == 'GET':
        return render(request, 'crear.html', {
        'form':CustomUserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'],
                                                 last_name=request.POST['last_name'], email=request.POST['email']  )
                user.save()
                hashed_password = hashlib.sha256(request.POST['password1'].encode()).hexdigest()
                login_escritorio_obj=login_escritorio.objects.create(id_usuario=user.id, nombre=request.POST['first_name'], apellidos=request.POST['last_name'], contrasenia=hashed_password,
                                                                     usuario=request.POST['username'])
                login_escritorio_obj.save()

                return redirect('principal')
            except IntegrityError:
                return render(request, 'crear.html', {
                    'form':CustomUserCreationForm,
                    "error": 'Nombre de usuario ya existe'
                })
        return render(request, 'crear.html', {
                    'form':CustomUserCreationForm,
                    "error": 'Las contraseñas no coinciden'
                })


@login_required

@user_passes_test(lambda u: u.is_superuser)     
def generar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventario.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(buffer, pagesize=(letter[1], letter[0]))

    title = 'Inventario de Productos'
    elements = []  
    title_paragraph = Paragraph(title, styles['Title'])
 
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, 'static', 'HIC.png')
    img = Image(image_path, width=30, height=50)  
    
    elements.append(img)
    elements.append(title_paragraph)
    data = []
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
    inventario = monitoreo_del_conteo.objects.all()

    if year:
        inventario = inventario.filter(fecha__year=year)

    if month:
        inventario = inventario.filter(fecha__month=month)

    if day:
        inventario = inventario.filter(fecha__day=day)


    data.append(['id','Tipo de pan', 'Panes contados', 'Fecha escaneo', 'Inicio conteo', 'Fin conteo', 'Descripción','Caducidad', 'Usuario','Matricula trabajador'])  # Encabezados de la tabla

    for item in inventario:
        descripcion = f'<font>{item.descripcion}</font>'  # Convierte el texto en HTML
        desc_paragraph = Paragraph(descripcion, styles['Normal'])

        data.append([item.id, item.nombre, item.cantidad, item.fecha, item.hora_inicio, item.hora_fin, desc_paragraph, item.fecha_caducidad, item.user, item.user.id])  # Agrega más campos según tus modelos




    table = Table(data)

    # Estilos para la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Color de fondo de la tabla
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alineación vertical media
    ])

    table.setStyle(style)
    elements.append(table)  # Agregar la tabla a la lista de elemento
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response