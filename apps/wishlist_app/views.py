from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

def loginregpage(request):
    return render(request, "wishlist_app/loginregpage.html")

def registration(request):
    errors = Users.objects.reg_validator(request.POST)
    hashedpw = bcrypt.hashpw(request.POST['reg_pass1'].encode(), bcrypt.gensalt())

    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        user = Users.objects.create(name=request.POST['reg_name'], username=request.POST['reg_username'], password=hashedpw, datehired=request.POST['reg_datehired'])
        user.save()
        request.session['name'] = user.name
        request.session['id'] = user.id
        return redirect('/dashboard')

def login(request):
    log_username = request.POST['login_username']
    errors = Users.objects.log_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        request.session['name'] = Users.objects.get(username=log_username).name
        request.session['id'] = Users.objects.get(username=log_username).id
        return redirect("/dashboard")

def renderdash(request):
    current_user = Users.objects.get(name=request.session['name'])
    context = {
        'current_user': current_user,
        'items': Items.objects.all(),
        'current_user_list': current_user.items.all()
   }
    return render(request, "wishlist_app/dashboard.html", context)

def additemrender(request):
    return render(request, "wishlist_app/itemadd.html")

def additem(request, userid):
    current_user = Users.objects.get(id=userid)
    errors = Items.objects.item_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/additemrender')
    else:
        item = Items.objects.create(name=request.POST['itemtoadd'], added_by = current_user)
        item.users.add(current_user)
        return redirect("/dashboard")

def addtowishlist(request, itemid):
    current_user = Users.objects.get(id=request.session['id'])
    current_item = Items.objects.get(id=itemid)
    current_user.items.add(current_item)
    return redirect("/dashboard")

def remove(request, itemid):
    current_user = Users.objects.get(id=request.session['id'])
    current_item = Items.objects.get(id=itemid)
    current_user.items.remove(current_item)
    current_user.save()
    return redirect("/dashboard")

def delete(request, itemid):
    current_item = Items.objects.get(id=itemid)
    current_item.delete()
    return redirect("/dashboard")

def itemdisplay(request, itemid):
    current_item = Items.objects.get(id=itemid)
    context = {
        "item_name": current_item.name,
        "userswhowantitem": current_item.users.all()
    }
    return render(request, "wishlist_app/itemdisplay.html", context)
        
def logout(request):
    request.session['name'] = False
    request.session['id'] = False
    return redirect('/main')