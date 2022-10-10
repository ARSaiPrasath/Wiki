from django.shortcuts import render
import markdown2
import random
from . import util

def convert(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return(markdowner.convert(content))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_convert = convert(title)
    if html_convert:
        return render(request, "encyclopedia/entry.html", {
            'title':title,
            'content':html_convert
        })
    else:
        return render(request, "encyclopedia/errorpage.html", {
            'message': 'This entry is Invalid'
        })

def search(request):
    if request.method == "POST":
        entrysearch = request.POST['q']
        html_convert = convert(entrysearch)
        if html_convert:
            return render(request, "encyclopedia/entry.html",{
                'title': entrysearch,
                'content':html_convert
            })
        else:
            entries = util.list_entries()
            arr1 = []
            for entry in entries:
                if entrysearch.lower() in entry.lower():
                    arr1.append(entry)
                    return render(request, "encyclopedia/search.html",{
                        'arr1': arr1
                    })
                else:
                    return render(request, "encyclopedia/errorpage.html",{
                        'message1':"This Page does not exist"
                    })
def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/errorpage.html",{
                'message':'Page already Exists!'
            })
        else:
            util.save_entry(title, content)
            html_convert = convert(title)
            return render(request, "encyclopedia/entry.html",{
                "title":title,
                "content":html_convert
            })
def randomit(request):
    randomize = random.choice(util.list_entries())
    html_convert = convert(randomize)
    return render(request, "encyclopedia/entry.html",{
        'title':randomize,
        'content':html_convert
    })

def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            'title':title,
            'content':content
    })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_convert = convert(title)
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":html_convert
        })
