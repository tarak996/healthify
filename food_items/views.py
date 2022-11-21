from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import Additemform, AddDateForm, AddDetailForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import FoodItem, AddDate, AddDetail, TotalEnergies
from django.db.models import Sum


def additem(request):
    if request.method == 'POST':
        fm = Additemform(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['Fooditem']
            em = fm.cleaned_data['Protein']
            pu = fm.cleaned_data['Carbohydrates']
            dp = fm.cleaned_data['Fat']
            pr = fm.cleaned_data['Calories']
            reg = FoodItem(Fooditem=nm, Protein=em, Carbohydrates=pu, Fat=dp, Calories=pr)
            reg.save()
            fm = Additemform()
    else:
        fm = Additemform()
    stud = FoodItem.objects.all()
    return render(request, 'additem.html', {'form': fm, 'stu': stud})


@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = AddDateForm(request.POST)

        if form.is_valid():
            date = form.cleaned_data['date']
            form = AddDate(user=request.user, date=date).save()

            return HttpResponseRedirect('#')
    else:
        form = AddDateForm

        form2 = Additemform
    model = AddDate.objects.all()
    items = AddDetail.objects.all()
    total = TotalEnergies.objects.all()
    date_list = []
    date = ''
    food_dic = {'date': '', 'protien': 0, 'carbo': 0, 'fat': 0, 'calories': 0}
    for all in total:
        food_dic = {'date': '', 'protien': 0, 'carbo': 0, 'fat': 0, 'calories': 0}
        for item in items:
            if item.date_d is not None:
                if all.date.id == item.date_d.id:
                    food_dic['date'] = item.date_d.id
                    food_dic['protien'] += item.add_item.Protein
                    food_dic['carbo'] += item.add_item.Carbohydrates
                    food_dic['fat'] += item.add_item.Fat
                    food_dic['calories'] += item.add_item.Calories
        if food_dic['protien'] > 0 and food_dic['date'] != date:
            print(food_dic)
            date = food_dic['date']
            print(date)
            count = 0
            for i in date_list:
                if i['date'] == date:
                    count += 1
            if count == 0:
                date_list.append(food_dic)
    return render(request, 'home.html',{'form': form, 'model': model, 'items': items, 'total': total, 'date_list': date_list})

def details(request, id):
    if request.method == 'POST':
        form = AddDetailForm(request.POST)
        if form.is_valid():
            date = AddDate.objects.get(pk=id)
            print(date, 'yes')
            item = form.cleaned_data['add_item']
            model = AddDetail(add_item=item, date_d=date)
            model.save()
    form = AddDetailForm
    model = AddDetail.objects.all()
    food_dic = {'protien':0, 'carbo': 0, 'fat': 0, 'calories': 0}
    if AddDetailForm is not None:
        for item in model:
            if item.date_d is not None:
                date_to_total = item.date_d
                if item.date_d.id == int(id):
                    food_dic['protien'] += item.add_item.Protein
                    food_dic['carbo'] += item.add_item.Carbohydrates
                    food_dic['fat'] += item.add_item.Fat
                    food_dic['calories'] += item.add_item.Calories
                    date_to_total = item.date_d
        total = TotalEnergies(date=date_to_total, total_pro=food_dic['protien'], total_carbo=food_dic['carbo'],
                              total_fat=food_dic['fat'], total_cal=food_dic['calories'])
        total.save()
    id = int(id)
    return render(request, 'details.html', {'form': form, 'model': model, 'id': id, 'food_dic': food_dic})


def sign(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Account Created Successfully !!')
    else:
        fm = SignUpForm()
    return render(request, 'signup.html', {'form':fm})


def logins(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
      fm = AuthenticationForm(request=request, data=request.POST)
      if fm.is_valid():
        uname = fm.cleaned_data['username']
        upass = fm.cleaned_data['password']
        user = authenticate(username=uname, password=upass)
        if user is not None:
          login(request, user)
          messages.success(request, 'Logged in successfully !!')
          return HttpResponseRedirect('/home/')
    else:
      fm = AuthenticationForm()
    return render(request, 'login.html', {'form':fm})
  else:
    return HttpResponseRedirect('/additem/')


def profile(request):
  if request.user.is_authenticated:
    return render(request, 'profile.html', {'name': request.user})
  else:
    return HttpResponseRedirect('/login/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def base(request):
    return render(request, 'base.html')


def delete_date(request, id):
    fm=AddDate.objects.get(pk=id)
    fm.delete()
    return HttpResponseRedirect('/home')

def delete_item(request):
    print(type(request.POST["id"]),'..............')
    id = request.POST['id'][1:]
    id2 = request.POST['id'][:1]
    print(id,'............................')
    fm = AddDetail.objects.get(pk=int(id))
    fm.delete()
    return HttpResponseRedirect(f'/details/{id2}')
