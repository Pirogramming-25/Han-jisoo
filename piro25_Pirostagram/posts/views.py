from django.shortcuts import render

def main(request):
    return render(request, 'posts/main.html')

def user_feed(request, username):
    users = {
        "pirogramming_official": {
            "username": "pirogramming_official",
            "name": "피로그래밍",
            "profile_img": "images/piro.png",
            "posts": 399,
            "followers": "1,387",
            "following": 0,
            "bio": "컴퓨터 회사",
        },
        "pirouser1": {
            "username": "pirouser1",
            "name": "pirouser 1",
            "profile_img": "images/pirouser1.png",
            "posts": 0,
            "followers": 120,
            "following": 80,
            "bio": "안녕하세요.",
        },
        "pirouser2": {
            "username": "pirouser2",
            "name": "pirouser 2",
            "profile_img": "images/pirouser2.png",
            "posts": 0,
            "followers": 95,
            "following": 60,
            "bio": "소개글이 없습니다.",
        },
        "pirouser3": {
            "username": "pirouser3",
            "name": "pirouser 3",
            "profile_img": "images/pirouser3.png",
            "posts": 0,
            "followers": 77,
            "following": 42,
            "bio": "나는 피로유저",
        },
        "pirouser4": {
            "username": "pirouser4",
            "name": "pirouser 4",
            "profile_img": "images/pirouser4.png",
            "posts": 0,
            "followers": 50,
            "following": 33,
            "bio": "아자아자 파이팅!",
        },
    }

    user = users.get(username)

    return render(request, 'posts/user_feed.html', {'profile_user': user})

def my_profile(request):
    return render(request, 'posts/my_profile.html')

def user_search(request):
    return render(request, 'posts/user_search.html')

def post_search(request):
    return render(request, 'posts/post_search.html')

def post_create(request):
    return render(request, 'posts/post_create.html')