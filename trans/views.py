from django.shortcuts import render
import googletrans
from googletrans import Translator
from googletrans import LANGUAGES

# Create your views here.

def index(request):
    context = {
        "ndict" : LANGUAGES
    }
    if request.method == "POST":
        b = request.POST.get("bf")
        s = request.POST.get("fr")
        d = request.POST.get("to")
        tra = Translator()
        after = tra.translate(b, src=s, dest=d).text
        context.update({
            "af" : after,
            "bf" : b,
            "fr" : s,
            "to" : d,
        })
    return render(request, "trans/index.html", context)