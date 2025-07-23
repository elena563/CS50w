from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import re
import numpy as np
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title): 
    mdcontent = util.get_entry(title)

    markdowner = Markdown()
    content = markdowner.convert(mdcontent)

    if content is not None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "error": "Entry does not exist"
        })

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    results = []
    for entry in entries:
        if entry.lower() == query.lower():
            return HttpResponseRedirect(reverse('entry', args=[entry]))
        
        if re.search(query, entry, flags=re.IGNORECASE):
            results.append(entry)
    
    return render(request, "encyclopedia/search.html", {
        'results' : results
    })

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Entry title')
    content = forms.CharField(label='Entry content', widget=forms.Textarea)

class EditEntryForm(forms.Form):
    title = forms.CharField(label='Entry title')
    content = forms.CharField(label='Entry content', widget=forms.Textarea)
        
def create(request):
    entries = util.list_entries()
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data

            if entry['title'] in entries:
                return render(request, "encyclopedia/create.html", {
                    'form': NewEntryForm(),
                    "error": "Entry already exists"
                })
            
            util.save_entry(entry['title'], entry['content'])
            return HttpResponseRedirect(reverse('entry', args=[entry['title']]))
        else:
            return render(request, "encyclopedia/create.html", {
                    'form': NewEntryForm(),
                    "error": "Invalid data"
                })
    else:
        return render(request, "encyclopedia/create.html", {'form': NewEntryForm()})
    
def edit(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        form = EditEntryForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data
            
            util.save_entry(entry['title'], entry['content'])
            return HttpResponseRedirect(reverse('entry', args=[entry['title']]))
        else:
            return render(request, "encyclopedia/create.html", {
                    'form': NewEntryForm(),
                    "error": "Invalid data"
                })
    else:
        return render(request, "encyclopedia/edit.html", {'form': EditEntryForm(initial={
            'title': title,
            'content': content
            }),
            'title': title
        })

def random(request):
    entries = util.list_entries()
    i = np.random.randint(len(entries))
    markdowner = Markdown()
    content = util.get_entry(entries[i]) 
    return render(request, "encyclopedia/entry.html", {
        "title": entries[i],
        "content": markdowner.convert(content)
    })
