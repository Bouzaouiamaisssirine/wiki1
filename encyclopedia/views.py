import markdown2
import random
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.files.storage import default_storage
from . import util



class SearchForm(forms.Form):
    query = forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search Wiki', 
            'style': 'width:100%'}))



class NewPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
            'placeholder': 'Enter your subject', 'id': 'new-entry-title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'new-entry','style': 'width:50%','placeholder': 'Enter your text'}))



class EditPage(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={
        'id': 'edit-entry-title'}))
    data = forms.CharField(label="", widget=forms.Textarea(attrs={
        'id': 'edit-entry'}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def entry(request, title):
    entry = util.get_entry(title)
    
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": SearchForm()
        })
    
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry),
            "entry_raw": entry,
            "form": SearchForm()
        })


def search(request):
    if request.method == "POST":
        entries_found = [] 
        entries_all = util.list_entries()  
        form = SearchForm(request.POST) 
        
        if form.is_valid():
         
            query = form.cleaned_data["query"]
            
           
            for entry in entries_all:
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse("entry", args=[title]))
              
                if query.lower() in entry.lower():
                    entries_found.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "results": entries_found,
                "query": query,
                "form": SearchForm()
            })
   
    return render(request, "encyclopedia/search.html", {
        "results": "",
        "query": "",
        "form": SearchForm()
    })

def crt(request):
    if request.method == "POST":
        new_entry = NewPage(request.POST) 
       
        if new_entry.is_valid():
            
            title = new_entry.cleaned_data["title"]
            data = new_entry.cleaned_data["data"]
            
            entries_all = util.list_entries()
          
            for entry in entries_all:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/crt.html", {
                        "form": SearchForm(),
                        "newPage": NewPage(),
                        "error": "That entry already exists!"
                    })
           
            new_entry_title = "# " + title
           
            new_entry_data = "\n" + data
       
            new_entry_content = new_entry_title + new_entry_data
            
            util.save_entry(title, new_entry_content)
            entry = util.get_entry(title)
           
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(entry),
                "form": SearchForm()
            })
    
    return render(request, "encyclopedia/crt.html", {
        "form": SearchForm(),
        "newPage": NewPage()
    })


def editEntry(request, title):
    if request.method == "POST":
       
        entry = util.get_entry(title)
       
        edit_form = EditPage(initial={'title': title, 'data': entry})
     
        return render(request, "encyclopedia/change.html", {
            "form": SearchForm(),
            "editPage": edit_form,
            "entry": entry,
            "title": title
        })


def submitEditEntry(request, title):
    if request.method == "POST":
     
        edit_entry = EditPage(request.POST)
        if edit_entry.is_valid():
        
            content = edit_entry.cleaned_data["data"]
            
            title_edit = edit_entry.cleaned_data["title"]
            
            if title_edit != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
          
            util.save_entry(title_edit, content)
           
            entry = util.get_entry(title_edit)
            msg_success = "Done (??u??) updated!"
       
        return render(request, "encyclopedia/entry.html", {
            "title": title_edit,
            "entry": markdown2.markdown(entry),
            "form": SearchForm(),
            "msg_success": msg_success
        })


def randomEntry(request):
    
    entries = util.list_entries()
  
    title = random.choice(entries)
   
    entry = util.get_entry(title)
   
    return HttpResponseRedirect(reverse("entry", args=[title]))
