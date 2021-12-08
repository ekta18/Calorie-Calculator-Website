from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .filters import fooditemFilter

@login_required(login_url='login')
@admin_only
def home(request):
    breakfast=Category.objects.filter(name='breakfast')[0].fooditem_set.all()[:5]
    lunch=Category.objects.filter(name='lunch')[0].fooditem_set.all()[:5]
    dinner=Category.objects.filter(name='dinner')[0].fooditem_set.all()[:5]
    snacks=Category.objects.filter(name='snacks')[0].fooditem_set.all()[:5]
    customers=Customer.objects.all()
    context={'breakfast':breakfast,
              'lunch':lunch,
              'dinner':dinner,
              'snacks':snacks,
              'customers':customers,
            }
    return render(request,'main.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def fooditem(request):
    breakfast=Category.objects.filter(name='breakfast')[0].fooditem_set.all()
    bcnt=breakfast.count()
    lunch=Category.objects.filter(name='lunch')[0].fooditem_set.all()
    lcnt=lunch.count()
    dinner=Category.objects.filter(name='dinner')[0].fooditem_set.all()
    dcnt=dinner.count()
    snacks=Category.objects.filter(name='snacks')[0].fooditem_set.all()
    scnt=snacks.count()
    context={'breakfast':breakfast,
              'bcnt':bcnt,
              'lcnt':lcnt,
              'scnt':scnt,
              'dcnt':dcnt,
              'lunch':lunch,
              'dinner':dinner,
              'snacks':snacks,
            }
    return render(request,'fooditem.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createfooditem(request):
    form = fooditemForm()
    if request.method == 'POST':
        form = fooditemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'createfooditem.html',context)

@unauthorized_user
def registerPage(request):
    form=createUserForm()
    if request.method=='POST':
        form=createUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='user')
            user.groups.add(group)
            email=form.cleaned_data.get('email')
            Customer.objects.create(user=user, name=username,email=email,calorie_limit=0)
            messages.success(request,'Account created for '+username)
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)

@unauthorized_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is invalid')
    return render(request,'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

def userPage(request):
    user=request.user
    cust=user.customer
    print(cust)
    exercise = Exercise.objects.filter(user_id=cust.id)
    e_ctotal = 0
    ecnt = 0
    for exr in exercise:
        e_cal = exr.calorie
        e_ctotal = e_ctotal + e_cal
        ecnt = ecnt + 1
    print(e_ctotal)
    fooditems=Fooditem.objects.filter()
    myfilter = fooditemFilter(request.GET,queryset=fooditems)
    fooditems=myfilter.qs
    total=UserFooditem.objects.all()
    myfooditems=total.filter(customer=cust)
    cnt=myfooditems.count()
    querysetFood=[]
    calorielimit=cust.calorie_limit
    print(calorielimit)
    for food in myfooditems:
        querysetFood.append(food.fooditem.all())
    finalFoodItems=[]
    for items in querysetFood:
        for food_items in items:
            finalFoodItems.append(food_items)
    totalCalories=0
    cnt = 0
    for foods in finalFoodItems:
        totalCalories+=foods.calorie
        cnt = cnt + 1
    ftotalCalories = totalCalories - e_ctotal
    CalorieLeft=calorielimit-ftotalCalories
    context={'Setlimit':calorielimit,'CalorieLeft':CalorieLeft,'totalCalories':ftotalCalories,'cnt':cnt,'foodlist':finalFoodItems,'fooditem':fooditems,'myfilter':myfilter,'exercise':exercise,'etotal':e_ctotal,'ecnt':ecnt,'totalcCalories': totalCalories}
    return render(request,'user.html',context)

def viewresult(request):
    user=request.user
    cust=user.customer
    print(cust)
    exercise = Exercise.objects.filter(user_id=cust.id)
    e_ctotal = 0
    for exr in exercise:
        e_cal = exr.calorie
        e_ctotal = e_ctotal + e_cal
    print(e_ctotal)
    fooditems=Fooditem.objects.filter()
    myfilter = fooditemFilter(request.GET,queryset=fooditems)
    fooditems=myfilter.qs
    total=UserFooditem.objects.all()
    myfooditems=total.filter(customer=cust)
    cnt=myfooditems.count()
    querysetFood=[]
    calorielimit=cust.calorie_limit
    print(calorielimit)
    for food in myfooditems:
        querysetFood.append(food.fooditem.all())
    finalFoodItems=[]
    for items in querysetFood:
        for food_items in items:
            finalFoodItems.append(food_items)
    totalCalories=0
    for foods in finalFoodItems:
        totalCalories+=foods.calorie
    ttotalCalories = totalCalories - e_ctotal
    CalorieLeft=calorielimit-ttotalCalories
    context={'Setlimit':calorielimit,'CalorieLeft':CalorieLeft,'totalCalories':totalCalories,'cnt':cnt,'foodlist':finalFoodItems,'fooditem':fooditems,'myfilter':myfilter,'exercise':exercise,'etotalCalories':e_ctotal,'ttotalCalories':ttotalCalories}
    return render(request,'result.html',context)


def addFooditem(request):
    user=request.user
    cust=user.customer
    if request.method=="POST":
        form =addUserFooditem(request.POST)
        if form.is_valid():
            fi = form.cleaned_data.get('fooditem_list')
            print("FoodItem",fi[0])
            print("Customer",cust)
            ufi = UserFooditem.objects.filter(customer=cust)
            print("UFI ",ufi)
            if not ufi:
                ufi = UserFooditem.objects.create(customer=cust)
                ufi.fooditem.set(fi)
            else:
                uufi = UserFooditem.objects.get(customer=cust)
                uufi.fooditem.add(*fi)            
            return redirect('/')
    form=addUserFooditem()
    context={'form':form}
    return render(request,'addUserFooditem.html',context)

def setcalorie(request):
    if request.method=='POST':
        limit=request.POST.get('setcalorie')
        print(limit)
        name=request.user
        user=Customer.objects.get(name=name)
        print(user)
        user.calorie_limit=limit
        user.save()
        return redirect('home')
    return render(request,'setcalorie.html')

def setexercise(request):
    if request.method=='POST':
        form =addExercise(request.POST)
        if form.is_valid():
            ename = form.cleaned_data.get('name')
            etime = form.cleaned_data.get('time')
            ecalorie = form.cleaned_data.get('calorie')
            usr = request.user
            cust = Customer.objects.get(name=usr)
            user_id = cust.id
            print("uid ",user_id)
            Exercise.objects.create(name=ename,time=etime,calorie=ecalorie,user_id=user_id)
            return redirect('home')
    form=addExercise()
    context={'form':form}
    return render(request,'setexercise.html',context)

def viewfood(request):
    fooditems=Fooditem.objects.filter()
    myfilter = fooditemFilter(request.GET,queryset=fooditems)
    fooditems=myfilter.qs
    context={'fooditem':fooditems,'myfilter':myfilter}
    return render(request,'viewfood.html',context)