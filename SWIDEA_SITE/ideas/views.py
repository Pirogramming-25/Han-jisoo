#ideas/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, IdeaStar, DevTool
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Case, When, Value, IntegerField


def idea_list(request):
    sort = request.GET.get('sort', 'latest')

    ideas = Idea.objects.all()

    if sort == 'star':
        ideas = ideas.annotate(
            starred_order=Case(
                When(ideastar__is_starred=True, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('-starred_order', '-created_at')

    elif sort == 'name':
        ideas = ideas.order_by('title')

    elif sort == 'oldest':
        ideas = ideas.order_by('created_at')

    else:
        ideas = ideas.order_by('-created_at')

    for idea in ideas:
        star = IdeaStar.objects.filter(idea=idea).first()
        idea.is_starred = star.is_starred if star else False

    paginator = Paginator(ideas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'ideas/idea_list.html', {
        'page_obj': page_obj,
        'sort': sort,
    })


def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    devtool = DevTool.objects.filter(name=idea.expected_devtool).first()

    return render(request, 'ideas/idea_detail.html', {
        'idea': idea,
        'devtool': devtool,
    })

def idea_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        expected_devtool = request.POST.get('expected_devtool')
        interest = request.POST.get('interest')
        image = request.FILES.get('image')

        if interest == '' or interest is None:
            interest = 0
        else:
            interest = int(interest)

        Idea.objects.create(
            title=title,
            content=content,
            image=image,
            expected_devtool = expected_devtool,
            interest = interest,
            )
        return redirect('idea-list')
    return render(request, 'ideas/idea_form.html')


def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        idea.title = request.POST.get('title')
        idea.content = request.POST.get('content')
        idea.expected_devtool = request.POST.get('expected_devtool')
        idea.interest = request.POST.get('interest') or 0

        if request.FILES.get('image'):
            idea.image = request.FILES.get('image')

        idea.save()
        return redirect('idea-detail', pk=pk)
    return render(request, 'ideas/idea_form.html', {'idea': idea})


def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        idea.delete()
        return redirect('idea-list')

    return render(request, 'ideas/idea_delete.html', {'idea': idea})

def idea_star(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        star, created = IdeaStar.objects.get_or_create(idea=idea)
        star.is_starred = not star.is_starred
        star.save()

        return JsonResponse({
            'success': True,
            'is_starred': star.is_starred,
        })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request',
    })

def devtool_manage(request):
    devtools = DevTool.objects.all()

    return render(request, 'ideas/devtool_manage.html', {
        'devtools': devtools,
    })


def devtool_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        kind = request.POST.get('kind')
        content = request.POST.get('content')

        DevTool.objects.create(
            name=name,
            kind=kind,
            content=content,
        )

        return redirect('devtool-manage')

    return render(request, 'ideas/devtool_form.html')


def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    ideas = Idea.objects.filter(expected_devtool=devtool.name)

    return render(request, 'ideas/devtool_detail.html', {
        'devtool': devtool,
        'ideas': ideas,
    })


def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)

    if request.method == 'POST':
        devtool.name = request.POST.get('name')
        devtool.kind = request.POST.get('kind')
        devtool.content = request.POST.get('content')
        devtool.save()

        return redirect('devtool-detail', pk=pk)

    return render(request, 'ideas/devtool_form.html', {
        'devtool': devtool,
    })


def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)

    if request.method == 'POST':
        devtool.delete()
        return redirect('devtool-manage')

    return render(request, 'ideas/devtool_delete.html', {
        'devtool': devtool,
    })

def idea_interest_ajax(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'plus':
            idea.interest += 1
        elif action == 'minus':
            if idea.interest > 0:
                idea.interest -= 1

        idea.save()

        return JsonResponse({
            'success': True,
            'interest': idea.interest,
        })

    return JsonResponse({
        'success': False,
        'error': 'Invalid request',
    })