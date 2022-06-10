from django.shortcuts import render, redirect
from .models import Topic, Choice
from django.utils import timezone

# Create your views here.
def index(request):
    t = Topic.objects.all()
    t = t.order_by("-pubdate")
    context = {
        "tset" : t
    }
    return render(request, "vote/index.html", context)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        "t" : t,
        "cset" : c,
    }
    return render(request, "vote/detail.html", context)

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cpk = request.POST.get("cho")
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
    return redirect("vote:detail", tpk)

def cancel(request,tpk):
    u = request.user
    t = Topic.objects.get(id=tpk)
    if u in t.voter.all():
        t.voter.remove(u)
        u.choice_set.get(topic=t).choicer.remove(u)
    return redirect("vote:detail", tpk)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        cn = request.POST.getlist("cname")
        cp = request.FILES.getlist("cpic")
        cc = request.POST.getlist("ccon")
        t = Topic(subject=s, maker=request.user, content=c, pubdate=timezone.now())
        t.save()
        for na, co, pi in zip(cn, cc, cp):
            Choice(topic=t, name=na, con=co, pic=pi).save()
        return redirect("vote:index")
        # 각 리스트에서 같은 인덱스끼리 마늗ㄹ어진 튜플들의 리스트
    return render(request, "vote/create.html")

def delete(request, tpk):
    t = Topic.objects.get(id=tpk)
    if request.user == t.maker:
        cset = t.choice_set.all()
        for i in cset:
            i.pic.delete()
        t.delete()
    else:
        pass
    return redirect("vote:index")