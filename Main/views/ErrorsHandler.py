from django.shortcuts import render


def error_404(request,*args, **argv):
        data = {}
        return render(request,'error_404.html', data)