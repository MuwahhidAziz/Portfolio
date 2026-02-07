from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms

from . import util

import markdown2
from random import choice

class frm(forms.Form):
    title = forms.CharField(label="Title")
    md = forms.CharField(label="MarkDown Content", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display(request, TITLE):
    content = util.get_entry(TITLE)
    if content is None:
        return render(request, "encyclopedia/404.html", {"title":TITLE})
    content = markdown2.markdown(content)
    return render(request, "encyclopedia/display.html", {"title":TITLE, "content":content})

def new(request):
    if request.method == 'POST':

        form = frm(request.POST)

        if form.is_valid():

            if form.cleaned_data['title'] in util.list_entries():
                return render(request, "encyclopedia/exist.html", {"title":form.cleaned_data["title"]})

            util.save_entry(form.cleaned_data['title'], form.cleaned_data['md'])
            return HttpResponseRedirect(reverse("display", args=[form.cleaned_data['title']]))

    return render(request, "encyclopedia/new.html", {'form':frm()})

def rndm(request):
    title = choice(util.list_entries())
    return HttpResponseRedirect(reverse("display", args=[title]))

def edit(request, TITLE):
    if request.method == 'POST':

        form = frm(request.POST)

        if form.is_valid():

            if TITLE not in util.list_entries():
                return render(request, "encyclopedia/404.html", {"title":TITLE})

            util.save_entry(TITLE, form.cleaned_data['md'])
            return HttpResponseRedirect(reverse("display", args=[TITLE]))

    title = TITLE
    content = util.get_entry(title)

    return render(request, "encyclopedia/new.html", {'form':frm(initial={'title':title, 'md':content})})

def result(request):
    entries = util.list_entries()
    TITLE = request.GET.get('q', '')
    if TITLE not in entries:
        matches = [entry for entry in entries if TITLE.lower() in entry.lower(d)]
        if not matches:
            return render(request, "encyclopedia/404.html", {"title":TITLE})
        return render(request, "encyclopedia/index.html", {'entries':matches})
    return HttpResponseRedirect(reverse("display", args=[TITLE]))