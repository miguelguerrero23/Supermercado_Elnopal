import imp, os
from datetime import datetime, date
from multiprocessing import context
from django.shortcuts import render , redirect
from django.contrib import messages
from django.http import  JsonResponse
from management.forms import *
from management.models import *
from personal.forms import *
from personal.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Create your views here.

def index_admin(request):
    location = True
    admin = True
    title_pag = "Menú de Administracion"
    registros=DetailSale.objects.all()
    registrosci=Sale.objects.all()
    
    registros_stats=registros.values('product').annotate(total_registros=Sum(('amount'), output_field=models.PositiveIntegerField())).order_by('total_registros')
    total_registros=DetailSale.objects.aggregate(Sum('amount'))['amount__sum']

    for i in registros_stats:
        i['product']=Product.objects.get(id=i['product'])
    registros_grupos=registros_stats.all()
    registros_grupos_final={}
    for j in registros_grupos:
        j['product']=Product.objects.get(id=j['product']).subcategory
        if registros_grupos_final.get(j['product']) != None:
           registros_grupos_final[j['product']]+= j['total_registros']
        else:
           registros_grupos_final[j['product']]= j['total_registros']

    fecha_stats=registrosci.values('date')

    # fecha_stats=registros.values('date').annotate(total_registros=Sum(('amount'), output_field=models.PositiveIntegerField()))
    
    context = {
        'title_pag':title_pag,
        'admin':admin,
        'location':location,
        'registros_stats':registros_stats,
        'fecha_stats':fecha_stats,
        'total_registros':total_registros,
        'registros_grupos':registros_grupos_final
    }
    return render(request, "admin/index-admin.html", context)

########################### SUBCATEGORY ############################
########################### SUBCATEGORY ############################

def subcategory(request):
    location = True
    admin = True
    title_pag = "Subcategoría"
    registers = Subcategory.objects.all()
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request,f'La subcategoría {name} se agregó correctamente!')
            return redirect('subcategory')
    else:
        form = SubcategoryForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
    }
    return render(request, 'admin/subcategory.html', context)
def subcategory_modal(request, modal, pk):
    location = True
    admin = True
    title_pag = "Subcategoría"
    modal_title = ''
    modal_txt = ''
    modal_submit = ''
    url_back="/administracion/subcategoria/"
    registers = Subcategory.objects.all()
    register_id = Subcategory.objects.get(id=pk)
    
    
    
    if modal == 'eliminar':
        modal_title = 'Eliminar subcategoría'
        modal_txt = 'eliminar la subcategoría'
        modal_submit = 'eliminar'
        form = SubcategoryForm(request.POST, request.FILES)
        if request.method == 'POST' :
            print('----------------------------------------ELIMINANDO')
            Subcategory.objects.filter(id=pk).update(
                status = False
            )
            print('-------------------------------------------------SE ELIMINÓ')
            subcategoryName = register_id.name.title()
            messages.success(request, f'La subcategoría {subcategoryName} se eliminó correctamente!')

            return redirect ('subcategory')
        else:
            form=SubcategoryForm()
            
            
            
    elif modal == 'editar':
        modal_title = 'Editar subcategoría'
        modal_txt = 'editar la subcategoría'
        modal_submit = 'guardar'
        form = SubcategoryForm(request.POST, request.FILES, instance=register_id)
        if request.method == 'POST':
            print('----------------------------------------EDITANDO')                
            if form.is_valid():
                form.save()
                subcategoryName = form.cleaned_data.get('name')
                messages.success(request, f'La subcategoría {subcategoryName} se editó correctamente!')
                return redirect ('subcategory')
        else:
            form=SubcategoryForm(instance=register_id)
    context ={
        'form':form,
        'modal_title':modal_title,
        'modal_txt':modal_txt,
        'modal_submit':modal_submit,
        'url_back':url_back,
        'modal':modal,
        'register_id':register_id,
        'title_pag':title_pag,
        'admin':admin,
        'registers':registers,
        'location':location
    }
    return render(request, 'admin/modal-category.html', context)

############################# CATEGORY #############################

def category(request):
    location = True
    admin = True
    title_pag = "Categoría"
    registers = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request,f'La categoría {name} se agregó correctamente!')
            return redirect('category')
    else:
        form = CategoryForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
    }
    return render(request, 'admin/category.html', context)


def category_modal(request, modal, pk):
    title_pag = "Categoría"
    location = True
    admin = True
    modal_title = ''
    modal_txt = ''
    modal_submit = ''
    url_back="/administracion/categoria/"
    registers = Category.objects.all()
    register_id = Category.objects.get(id=pk)
    
    
    
    if modal == 'eliminar':
        modal_title = 'Eliminar categoría'
        modal_txt = 'eliminar la categoría'
        modal_submit = 'eliminar'
        form = SubcategoryForm(request.POST, request.FILES)
        if request.method == 'POST':
            print('----------------------------------------ELIMINANDO')
            Category.objects.filter(id=pk).update(
                status = False
            )
            print('Eliminado')
            categoryName = register_id.name.title()
            messages.success(request, f'La categoría {categoryName} se eliminó correctamente!')
            return redirect ('category')
        else:
            form = CategoryForm()
        
    
    
    elif modal == 'editar':
        modal_title = 'Editar categoría'
        modal_txt = 'editar la categoría'
        modal_submit = 'guardar'
        form = CategoryForm(request.POST, request.FILES, instance=register_id)
        if request.method == 'POST':
            print('----------------------------------------EDITANDO')                
            if form.is_valid():
                form.save()
                categoryName = form.cleaned_data.get('name')
                messages.success(request, f'La categoría {categoryName} se editó correctamente!')
                return redirect ('category')
        else:
            form = CategoryForm(instance=register_id)
            
            
            
            
    context ={
        'form':form,
        'modal_title':modal_title,
        'modal_txt':modal_txt,
        'modal_submit':modal_submit,
        'url_back':url_back,
        'modal':modal,
        'register_id':register_id,
        'title_pag':title_pag,
        'admin':admin,
        'registers':registers,
        'location':location,
    }
    return render(request, 'admin/modal-category.html', context)

############################## BRAND ###############################

def brand(request):
    location = True
    admin = True
    title_pag = "Marca"
    registers = Brand.objects.all()
    # fields = [f.name for f in Subcategory()._meta.get_fields()][2:-1]
    fields = ['name']
    # print(fields)
    atributes = ['Nombre']
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request,f'La marca {name} se agregó correctamente!')
            return redirect('brand')
    else:
        form = BrandForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'fields':fields,
        'atributes':atributes
    }
    return render(request, 'admin/brand.html', context)

def brand_modal(request, modal, pk):
    title_pag = "Marca"
    modal_title = ''
    modal_txt = ''
    location = True
    admin = True
    modal_submit = ''
    url_back="/administracion/marca/"
    registers = Brand.objects.all()
    register_id = Brand.objects.get(id=pk)
    if modal == 'eliminar':
        modal_title = 'Eliminar marca'
        modal_txt = 'eliminar la marca'
        modal_submit = 'eliminar'
        if request.method == 'POST':
            print('----------------------------------------ELIMINANDO')
            Brand.objects.filter(id=pk).update(
                status = False
            )
            brandName = register_id.name.title()
            messages.success(request, f'La marca {brandName} se eliminó correctamente!')
            return redirect ('brand')
        else:
            form=BrandForm()
    elif modal == 'editar':
        modal_title = 'Editar marca'
        modal_txt = 'editar la marca'
        modal_submit = 'guardar'
        form = BrandForm(request.POST, request.FILES, instance=register_id)
        if request.method == 'POST':
            print('----------------------------------------EDITANDO')                
            if form.is_valid():
                form.save()
                brandName = form.cleaned_data.get('name')
                messages.success(request, f'La marca {brandName} se editó correctamente!')
                return redirect ('brand')
        else:
            form=BrandForm(instance=register_id)
    context ={
        'form':form,
        'modal_title':modal_title,
        'modal_txt':modal_txt,
        'modal_submit':modal_submit,
        'url_back':url_back,
        'modal':modal,
        'register_id':register_id,
        'title_pag':title_pag,
        'admin':admin,
        'registers':registers,
        'location':location,
    }
    return render(request, 'admin/modal-brand.html', context)

############################# PRODUCT ##############################

def product(request):
    location = True
    admin = True
    title_pag = "Producto"
    registers = Product.objects.all()
    # fields = [f.name for f in Subcategory()._meta.get_fields()][2:-1]
    fields = ['name','price','subcategory','brand','expirationDate','unitMeasurement','stock','description','image']
    # print(fields)
    atributes = ['Nombre','Precio','Subcategoría','Fecha de Vencimeinto','Unidad de Medida','Stock','Descripción','Imagen']
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request,f'El producto {name} se agregó correctamente!')
            return redirect('product')
    else:
        form = ProductForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'fields':fields,
        'atributes':atributes
    }
    return render(request, 'admin/product.html', context)

def product_modal(request, modal, pk):
    title_pag = "Producto"
    modal_title = ''
    modal_txt = ''
    location = True
    admin = True
    modal_submit = ''
    url_back="/administracion/producto/"
    registers = Product.objects.all()
    register_id = Product.objects.get(id=pk)
    if modal == 'eliminar':
        modal_title = 'Eliminar producto'
        modal_txt = 'eliminar el producto'
        modal_submit = 'eliminar'
        form = ProductForm(request.POST, request.FILES)
        if request.method == 'POST':
            print('----------------------------------------ELIMINANDO')
            Product.objects.filter(id=pk).update(
                status = False
            )
            productName = register_id.name.title()
            messages.success(request, f'El producto {productName} se eliminó correctamente!')
            return redirect ('product')
        else:
            form=ProductForm()
    elif modal == 'editar':
        modal_title = 'Editar producto'
        modal_txt = 'editar el producto'
        modal_submit = 'guardar'
        form = ProductForm(request.POST, request.FILES, instance=register_id)
        if request.method == 'POST':
            print('----------------------------------------EDITANDO')                
            if form.is_valid():
                form.save()
                productName = form.cleaned_data.get('name')
                messages.success(request, f'La producto {productName} se editó correctamente!')
                return redirect ('product')
        else:
            form=ProductForm(instance=register_id)
    context ={
        'form':form,
        'modal_title':modal_title,
        'modal_txt':modal_txt,
        'modal_submit':modal_submit,
        'url_back':url_back,
        'modal':modal,
        'register_id':register_id,
        'title_pag':title_pag,
        'admin':admin,
        'registers':registers,
        'location':location,
    }
    return render(request, 'admin/modal-product.html', context)

############################# PROVIDER #############################

def provider(request):
    location = True
    admin = True
    title_pag = "Proveedor"
    registers = Provider.objects.all()
    # fields = [f.name for f in Subcategory()._meta.get_fields()][2:-1]
    fields = ['name','phone','email']
    # print(fields)
    atributes = ['Nombre','Celular','Correo Electrónico']
    if request.method == 'POST':
        form = ProviderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            messages.success(request,f'El proveedor {name} se agregó correctamente!')
            return redirect('provider')
    else:
        form = ProviderForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'fields':fields,
        'atributes':atributes
    }
    return render(request, 'admin/provider.html', context)

def provider_modal(request, modal, pk):
    title_pag = "Proveedor"
    modal_title = ''
    location = True
    admin = True
    modal_txt = ''
    modal_submit = ''
    url_back="/administracion/proveedor/"
    registers = Provider.objects.all()
    register_id = Provider.objects.get(id=pk)
    if modal == 'eliminar':
        modal_title = 'Eliminar proveedor'
        modal_txt = 'eliminar el proveedor'
        modal_submit = 'eliminar'
        form = ProviderForm(request.POST, request.FILES)
        if request.method == 'POST':
            print('----------------------------------------ELIMINANDO')
            Provider.objects.filter(id=pk).update(
                status = False
            )
            providerName = register_id.name.title()
            messages.success(request, f'El proveedor {providerName} se eliminó correctamente!')
            return redirect ('provider')
        else:
            form=ProviderForm()
    elif modal == 'editar':
        modal_title = 'Editar proveedor'
        modal_txt = 'editar el proveedor'
        modal_submit = 'guardar'
        form = ProviderForm(request.POST, request.FILES, instance=register_id)
        if request.method == 'POST':
            print('----------------------------------------EDITANDO')                
            if form.is_valid():
                form.save()
                providerName = form.cleaned_data.get('name')
                messages.success(request, f'El proveedor {providerName} se editó correctamente!')
                return redirect ('provider')
        else:
            form=ProviderForm(instance=register_id)
    context ={
        'form':form,
        'modal_title':modal_title,
        'modal_txt':modal_txt,
        'modal_submit':modal_submit,
        'url_back':url_back,
        'modal':modal,
        'register_id':register_id,
        'title_pag':title_pag,
        'admin':admin,
        'registers':registers,
        'location':location,
    }
    return render(request, 'admin/modal-provider.html', context)
    
################################ USER ##############################

def user(request):
    location = True
    admin = True
    title_pag = "Usuario"
    registers = User.objects.all()
    # fields = [f.name for f in Subcategory()._meta.get_fields()][2:-1]
    fields = ['username','email','name','lastName','tDocument','nDocument','phone','dateBirth','user_admin']
    # print(fields)
    atributes = ['Username','Correo Electrónico','Nombre','Apellido','Tipo de Documento','Número de Documento','Celular','Fecha de Nacimiento','¿Es administrador?']
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            messages.success(request,f'El usuario {name} se agregó correctamente!')
            return redirect('user')
    else:
        form = UserForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'fields':fields,
        'atributes':atributes
    }
    return render(request, 'admin/user.html', context)

def user_modal(request, modal, pk):
    title_pag = "Usuario"
    modal_title = ''
    modal_txt = ''
    location = True
    admin = True
    modal_submit = ''
    url_back="/administracion/usuario/"
    registers = User.objects.all()
    register_id = User.objects.get(id=pk)
    if modal == 'eliminar':
        modal_title = 'Eliminar usuario'
        modal_txt = 'eliminar el usuario'
        modal_submit = 'eliminar'
        form = UserForm(request.POST, request.FILES)
        if request.method == 'POST':
            print('----------------------------------------ELIMINANDO')
            User.objects.filter(id=pk).update(
                status = False
            )
            userName = register_id.username.title()
            messages.success(request, f'El usuario {userName} se eliminó correctamente!')
            return redirect ('user')
        else:
            form=UserForm()
    elif modal == 'editar':
        modal_title = 'Editar usuario'
        modal_txt = 'editar el usuario'
        modal_submit = 'guardar'
        form = UserForm(request.POST, request.FILES, instance=register_id)
        if request.method == 'POST':
            print('----------------------------------------EDITANDO')                
            if form.is_valid():
                form.save()
                userName = form.cleaned_data.get('username')
                messages.success(request, f'El proveedor {userName} se editó correctamente!')
                return redirect ('user')
        else:
            form=UserForm(instance=register_id)
    context ={
        'form':form,
        'modal_title':modal_title,
        'modal_txt':modal_txt,
        'modal_submit':modal_submit,
        'url_back':url_back,
        'modal':modal,
        'register_id':register_id,
        'title_pag':title_pag,
        'admin':admin,
        'registers':registers,
        'location':location,
    }
    return render(request, 'admin/modal-user.html', context)
############################# BACKUP ###############################
def export_data():
    date_now = date.today()
    print('JUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEPUTA')
    os.system(f"mysqldump --add-drop-table --column-statistics=0 --password=Angie1053442155 -u root db_elnopal> nopal/static/backup/BKP_{date_now}.sql")
    print('-------------------------------------------------------Hecho')
def import_data(file):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>LISTO PA´ IMPRIMIR')
    try:
        print('------------------------IMPORTAR')
        os.system(f"mysql --password=Angie1053442155 -u root db_elnopal < {file[1:]}")
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><Salio')
    except:
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<< CHALE')
        print("Problemas al importar")

def backup(request, tipo):
    title_pag = "Backup"
    location = True
    admin = True
    example_dir = 'nopal/static/backup/'
    with os.scandir (example_dir) as ficheros:
        ficheros = [fichero.name for fichero in ficheros if fichero.is_file()]
    print(ficheros)
    backups = Backup.objects.all()
    if request.method == 'POST' and tipo== "U":
        print('----------------------------------INTENTO')
        form = BackupForm(request.POST, request.FILES)
        if form.is_valid():
            name= request.POST['name']
            file = request.FILES['file']
            insert = Backup(name=name, file=file)
            import_data(insert.file.url)
            insert.save()
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<GUARDÓ')
            return redirect('backup','A')
        else:
            print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Error al procesar el formulario")
              
    elif request.method == 'POST' and tipo== "D":
        export_data()
        return redirect('backup','A')
    
    else:
        form = BackupForm()
        
    context ={
        "ficheros":ficheros,
        "form":form,
        "backups":backups,
        'title_pag':title_pag,
        'admin':admin,
        'location':location
    }
    return render(request, 'admin/backup.html',context) 

def buy(request):
    location = True
    admin = True
    buy_template = True
    title_pag = "Compra"
    registers = Buy.objects.all()
    if request.method == 'POST':
        print('COMPRA-------------------------------->')
        form = BuyForm(request.POST)
        if form.is_valid():
            print(request.POST)
            date_aux = datetime.now().strftime("%Y-%m-%d")
            buy = Buy.objects.create(
                date = date_aux,
                provider = form.cleaned_data['provider'],
                payment = request.POST['payment']
            )
            messages.success(
                request, f'La compra #{buy.id} está lista para añadir productos')
            return redirect('buy-detail', pk=buy.id)
    else:
        form = BuyForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'buy_template':buy_template,
    }
    return render(request, 'admin/buy.html', context)

def detail_buy(request, pk):
    location = True
    admin = True
    buy_template = True
    title_pag = "Compra"
    modal = True
    
    registers = DetailBuy.objects.filter(buy=pk)
    buy_a = Buy.objects.filter(id=pk)
    buy_id = Buy.objects.get(id=pk)
    total = 0
    
    factura = Buy.objects.get(id=pk)

    if request.method == 'POST':
        form = DetailBuyForm(request.POST)
        if form.is_valid():
            print('------------------------> Formato válido')
            product = Product.objects.get(
                id=request.POST['product']
            )
            print('------------------------> Producto con id')
            
            detail = DetailBuy.objects.filter(
                buy = buy_id,
                product = request.POST['product'],
            )
            print('------------------------> Filtra si hay detalle')
            
            if detail.exists(): # ------------------------ Busca detalle, si existe, la filtra
                print('------------------------> Detalle Existe')
                detail_a = DetailBuy.objects.filter(
                    buy = pk,
                    product = request.POST['product'], 
                )
                print('------------------------> Busca si ya está el producto')
                if detail_a.exists():
                    print('Producto encontrado ')
                    total = form.cleaned_data.get('amount') * int(form.cleaned_data.get('product').price)
                    print('------------------------> ',total)
                    detail_a.update(
                        amount =  detail_a[0].amount + form.cleaned_data.get('amount'),
                        total = detail_a[0].total + total
                    )
                    print('------------------------> Actualización de la cantidad de producto en el detalle existente')
                    
                    Product.objects.filter(id = product.id).update(
                        stock = product.stock + form.cleaned_data.get('amount')
                    )
                    print('------------------------> Stock actualizado')

                    Buy.objects.filter(
                        id=pk
                        ).update(
                            finalPrice = buy_a[0].finalPrice + total
                        )
                    print('------------------------> Total actualizado')
                    
                    messages.success(request,f'{product} se añadió a la compra!')
                    return redirect('buy-detail', pk=pk) 
           
            else:
                detail_a = DetailBuy.objects.filter(
                    buy = pk,
                    product = request.POST['product'], 
                )
                print('------------------------> Detalle NO Existe')
                
                DetailBuy.objects.create( # ------------------------ Crea un detalle
                    buy = buy_id,
                    product = product,
                    amount = request.POST['amount'], 
                )
                print('------------------------> Detalle creado:')
                
                Product.objects.filter(id = product.id).update(
                    stock = int(product.stock) + int(request.POST['amount'])
                )
                print('------------------------> Stock actualizado')

                total = form.cleaned_data.get('amount') * int(form.cleaned_data.get('product').price)
                print('------------------------> ',total)
                detail_a.update(
                    total = detail_a[0].total + total
                )
                print('------------------------> Total ')

                Buy.objects.filter(
                        id=pk
                        ).update(
                            finalPrice = buy_a[0].finalPrice + total
                        )
                print('------------------------> Total Compra actualizado')
                messages.success(request,f'{product} se añadió a la compra!')
                return redirect('buy-detail', pk=pk)
    else:
        form = DetailBuyForm()
        
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'buy_template':buy_template,
        'factura':factura,
        'modal':modal
    }
    return render(request, 'admin/detail.html', context)

def sale(request):
    location = True
    admin = True
    buy_template = False
    title_pag = "Venta"
    registers = Sale.objects.all()
    if request.method == 'POST':
        print('VENTA-------------------------------->')
        form = SaleForm(request.POST)
        if form.is_valid():
            print(request.POST)
            date_aux = datetime.now().strftime("%Y-%m-%d")
            sale = Sale.objects.create(
                date = date_aux,
                user = form.cleaned_data['user'],
                payment = request.POST['payment'],
            )
            if request.POST['client'] or request.POST['address'] or request.POST['nDocument']:
                Sale.objects.filter(id=sale.id).update(
                    client = request.POST['client'],
                    address = request.POST['address'],
                    nDocument = request.POST['nDocument'],
                )
            messages.success(
                request, f'La venta #{sale.id} está lista para añadir productos')
            return redirect('sale-detail', pk=sale.id)
    else:
        form = SaleForm()
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'buy_template':buy_template,
    }
    return render(request, 'admin/sale.html', context)

def detail_sale(request, pk):
    location = True
    admin = True
    buy_template = False
    title_pag = "Venta"
    modal = False
    
    registers = DetailSale.objects.filter(sale=pk)
    sale_a = Sale.objects.filter(id=pk)
    sale_id = Sale.objects.get(id=pk)
    total = 0
    
    factura = Sale.objects.get(id=pk)

    if request.method == 'POST':
        form = DetailSaleForm(request.POST)
        if form.is_valid():
            print('------------------------> Formato válido')
            product = Product.objects.get(
                id=request.POST['product']
            )
            print('------------------------> Producto con id')
            
            detail = DetailSale.objects.filter(
                sale = sale_id,
                product = request.POST['product'],
            )
            print('------------------------> Filtra si hay detalle')
            
            
            if(product.stock >= int(request.POST['amount'])):
                if detail.exists(): # ------------------------ Busca detalle, si existe, la filtra
                    print('------------------------> Detalle Existe')
                    detail_a = DetailSale.objects.filter(
                        sale = pk,
                        product = request.POST['product'], 
                    )
                    print('------------------------> Busca si ya está el producto')
                    if detail_a.exists():
                        print('Producto encontrado ')
                        
                    
                        total = form.cleaned_data.get('amount') * int(form.cleaned_data.get('product').price)
                        print('------------------------> ',total)
                        detail_a.update(
                            amount =  detail_a[0].amount + form.cleaned_data.get('amount'),
                            total = detail_a[0].total + total
                        )
                        print('------------------------> Actualización de la cantidad de producto en el detalle existente')
                        
                        Product.objects.filter(id = product.id).update(
                            stock = product.stock - form.cleaned_data.get('amount')
                        )
                        print('------------------------> Stock actualizado')

                        Sale.objects.filter(
                            id=pk
                            ).update(
                                finalPrice = sale_a[0].finalPrice + total
                            )
                        print('------------------------> Total actualizado')
                        
                        messages.success(request,f'{product} se añadió a la venta!')
                        return redirect('sale-detail', pk=pk) 
            
                else:
                    detail_a = DetailSale.objects.filter(
                        sale = pk,
                        product = request.POST['product'], 
                    )
                    print('------------------------> Detalle NO Existe')
                    
                    DetailSale.objects.create( # ------------------------ Crea un detalle
                        sale = sale_id,
                        product = product,
                        amount = request.POST['amount'], 
                    )
                    print('------------------------> Detalle creado:')
                    
                    Product.objects.filter(id = product.id).update(
                        stock = int(product.stock) - int(request.POST['amount'])
                    )
                    print('------------------------> Stock actualizado')

                    total = form.cleaned_data.get('amount') * int(form.cleaned_data.get('product').price)
                    print('------------------------> ',total)
                    detail_a.update(
                        total = detail_a[0].total + total
                    )
                    print('------------------------> Total ')

                    Sale.objects.filter(
                            id=pk
                            ).update(
                                finalPrice = sale_a[0].finalPrice + total
                            )
                    print('------------------------> Total Venta actualizado')
                    messages.success(request,f'{product} se añadió a la venta!')
                    return redirect('sale-detail', pk=pk)
            else:
                messages.warning(request, f'Sólo tenemos {product.stock} disponibles de {product} :c')
    else:
        form = DetailSaleForm()
        
    context = {
        'form':form,
        'title_pag':title_pag,
        'admin':admin,
        'registers': registers,
        'location':location,
        'buy_template':buy_template,
        'factura':factura,
        'modal':modal
    }
    return render(request, 'admin/detail.html', context)
