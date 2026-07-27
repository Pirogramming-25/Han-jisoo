from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import PostForm
from .models import Post


def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get("search_txt")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    if search_txt:
        posts = posts.filter(
            title__icontains=search_txt
        )

    try:
        if min_price:
            posts = posts.filter(
                price__gte=int(min_price)
            )

        if max_price:
            posts = posts.filter(
                price__lte=int(max_price)
            )

    except (ValueError, TypeError):
        pass

    context = {
        "posts": posts,
        "search_txt": search_txt,
        "min_price": min_price,
        "max_price": max_price,
    }

    return render(
        request,
        "posts/list.html",
        context=context,
    )


def create(request):
    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            post = form.save()

            return redirect(
                "posts:detail",
                pk=post.pk,
            )

    else:
        form = PostForm()

    return render(
        request,
        "posts/create.html",
        {
            "form": form,
        },
    )


def detail(request, pk):
    post = get_object_or_404(
        Post,
        pk=pk,
    )

    return render(
        request,
        "posts/detail.html",
        {
            "post": post,
        },
    )


def update(request, pk):
    post = get_object_or_404(
        Post,
        pk=pk,
    )

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "posts:detail",
                pk=pk,
            )

    else:
        form = PostForm(
            instance=post,
        )

    return render(
        request,
        "posts/update.html",
        {
            "form": form,
            "post": post,
        },
    )


def delete(request, pk):
    post = get_object_or_404(
        Post,
        pk=pk,
    )

    post.delete()

    return redirect("/")