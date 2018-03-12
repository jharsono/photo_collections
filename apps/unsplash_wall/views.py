from django.shortcuts import render, redirect
from .models import User, SearchManager, SavedImage, Collection
import bcrypt
from django.contrib import messages

def index(request):
    if "logged_in" not in request.session or request.session["logged_in"] == False:
        return render(request, 'unsplash_wall/index.html')
    else:
        if request.session["logged_in"] == True:
            return redirect('/home')
        else:
            return render(request, 'unsplash_wall/index.html')


def login(request):

    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        email = request.POST['email']
        if "email" not in request.session:
            request.session['email'] = email
        if "logged_in" not in request.session:
            request.session['logged_in'] = True

        return redirect('/home')

def create_user(request):

    password = request.POST['password']
    hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)

        return redirect('/home')
    else:
        email = request.POST['email']
        if "email" not in request.session:
            request.session['email'] = email

        if "logged_in" not in request.session:
            request.session['logged_in'] = True

        User.objects.create(
        first=request.POST['first'],
        last=request.POST['last'],
        email=request.POST['email'],
        hash_pw=hash_pw )
        return redirect('/home')


def home(request):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        email = request.session["email"]
        user = User.objects.get(email=email)
        my_collections = Collection.objects.filter(creator=user)
        images = SavedImage.objects.filter(collection=my_collections)
        all_collections = Collection.objects.exclude(creator=user)
        context = {
                    "first": user.first,
                    "collections": my_collections,
                    "all_collections": all_collections,
                    "images": images
                }
        return render(request, 'unsplash_wall/home.html', context)

def search(request):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
    # errors = SearchManager.search_validator(request.POST)
    # if len(errors):
    #     for tag, error in errors.iteritems():
    #         messages.error(request, error, extra_tags=tag)
    #     return redirect('/')
    # else:
        if "query" not in request.session:
            request.session["query"] = request.POST.get("query")
        else:
            request.session["query"] = request.POST.get("query")
        return redirect("/results")


def results(request):
    email = request.session["email"]
    user = User.objects.get(email=email)
    my_collections = Collection.objects.filter(creator=user)
    context = {
                "collections": my_collections
                }
    return render(request,'unsplash_wall/results.html', context)

def add_to_collection(request):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        if request.POST.get("collection_list") != "none":
            select_collection = request.POST.get('collection_list')

        else:
            select_collection = request.POST["collection_name"]
        email = request.session["email"]
        user = User.objects.get(email=email)

        this_collection = Collection.objects.create(name=select_collection, creator=user)

        for i in range(len(request.POST.getlist('selected_images'))):
            SavedImage.objects.create(
                unsplash_data=request.POST.getlist('selected_images')[i],
                saved_by=user,
                collection=this_collection)


    return redirect('/home')

def view_collection(request, id):
    collection = Collection.objects.get(id=id)
    images = SavedImage.objects.filter(collection=collection)

    context = {
            "collection": collection,
            "images": images
            }
    return render(request, 'unsplash_wall/view.html', context)

def slideshow(request, id):
    collection = Collection.objects.get(id=id)
    images = SavedImage.objects.filter(collection=collection)
    context = {
                "collection": collection,
                "images":images
                }

    return render (request, 'unsplash_wall/slideshow.html', context)


def delete_collection(request, id):
    collection = Collection.objects.get(id=id)
    collection.delete()
    return redirect('/home')


def logout(request):
    request.session.clear()
    return redirect('/')
