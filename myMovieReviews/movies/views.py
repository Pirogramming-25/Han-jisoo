from django.shortcuts import render, get_object_or_404, redirect
from .models import Review


def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'movies/review_list.html', {'reviews': reviews})


def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'movies/review_detail.html', {'review': review})


def review_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        director = request.POST.get('director')
        actor = request.POST.get('actor')
        genre = request.POST.get('genre')
        rating = request.POST.get('rating')
        running_time = request.POST.get('running_time')
        content = request.POST.get('content')
        release_year = request.POST.get('release_year')
        image = request.FILES.get('image')

        Review.objects.create(
            title=title,
            director=director,
            actor=actor,
            genre=genre,
            rating=rating,
            running_time=running_time,
            content=content,
            release_year=release_year,
            image=image,
        )
        return redirect('review-list')
    return render(request, 'movies/review_form.html')


def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor')
        review.genre = request.POST.get('genre')
        review.rating = request.POST.get('rating')
        review.running_time = request.POST.get('running_time')
        review.content = request.POST.get('content')
        review.release_year = request.POST.get('release_year')

        if request.FILES.get('image'):
            review.image = request.FILES.get('image')

        review.save()
        return redirect('review-detail', pk=pk)
    return render(request, 'movies/review_form.html', {'review': review})


def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review-list')
    return render(request, 'movies/review_delete.html', {'review': review})

def review_ver2(request):
    return render(request, 'movies/review_ver2.html')