from django.shortcuts import render, redirect
from backend.methods.MCDMFactory import MCDAMethodFactory

available_methods = MCDAMethodFactory.get_available_methods()


def index(request):
    return render(request, "index.html", {"available_methods": available_methods})


def method(request, method_name):
    if method_name not in available_methods:
        return redirect("frontend:index")
    return render(
        request,
        f"method.html",
        {"method_name": method_name, "available_methods": available_methods},
    )
