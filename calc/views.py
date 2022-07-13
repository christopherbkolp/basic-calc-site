from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.core.cache import cache

from .forms import CalcForm
from .calculator import Calculate

def CalcView(request):
    template = loader.get_template('calc/calculator.html')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CalcForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                user = Calculate()
                # form.cleaned_data.get('expression')
                user.get_equation(form.cleaned_data.get('expression'))
                user.math_check()
            except SystemExit:
                error_msg = user.error_msg
                cache.set('error', error_msg, None)
                return HttpResponseRedirect(reverse('calc:error'))

            cache.set('result', user.return_result(), None)
            return HttpResponseRedirect(reverse('calc:results'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CalcForm()

    return render(request, 'calc/calculator.html', {'form': form})

def ResultsView(request):
    template = loader.get_template('calc/results.html')
    result = cache.get('result')
    context = {
        'result': result,
    }

    return HttpResponse(template.render(context, request))

def ErrorView(request):
    template = loader.get_template('calc/error.html')
    error = cache.get('error')
    context = {
        'error_msg': error,
    }

    return HttpResponse(template.render(context, request))
