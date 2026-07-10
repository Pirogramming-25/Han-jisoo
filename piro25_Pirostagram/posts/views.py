from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import Follow, Post, Like, Comment, Story, Profile

def main(request):
    ensure_demo_users()

    current_user = get_current_user(request)
    posts = Post.objects.all().order_by("-created_at")

    liked_post_ids = Like.objects.filter(
        user=current_user
    ).values_list("post_id", flat=True)

    story_users = User.objects.filter(
        stories__isnull=False
    ).exclude(
        username=current_user.username
    ).distinct()

    recommended_users = [
        {
            "username": "pirouser1",
            "name": "pirouser 1",
            "profile_img": "images/pirouser1.png",
        },
        {
            "username": "pirouser2",
            "name": "pirouser 2",
            "profile_img": "images/pirouser2.png",
        },
        {
            "username": "pirouser3",
            "name": "pirouser 3",
            "profile_img": "images/pirouser3.png",
        },
        {
            "username": "pirouser4",
            "name": "pirouser 4",
            "profile_img": "images/pirouser4.png",
        },
    ]

    for user in recommended_users:
        target_user = User.objects.get(username=user["username"])

        user["is_following"] = Follow.objects.filter(
            follower=current_user,
            following=target_user
        ).exists()

    return render(request, "posts/main.html", {
        "posts": posts,
        "liked_post_ids": liked_post_ids,
        "story_users": story_users,
        "recommended_users": recommended_users,
    })

def user_feed(request, username):
    ensure_demo_users()
    users = {
        "wltn1.2": {
            "username": "wltn1.2",
            "name": "한지수",
            "profile_img": "images/profile1.webp",
            "posts": 0,
            "followers": 0,
            "following": 0,
            "bio": "소개글이 없습니다.",
        },
        "pirogramming_official": {
            "username": "pirogramming_official",
            "name": "피로그래밍",
            "profile_img": "images/piro.png",
            "posts": 0,
            "followers": "0",
            "following": 0,
            "bio": "컴퓨터 회사",
        },
        "pirouser1": {
            "username": "pirouser1",
            "name": "pirouser 1",
            "profile_img": "images/pirouser1.png",
            "posts": 0,
            "followers": 0,
            "following": 0,
            "bio": "안녕하세요.",
        },
        "pirouser2": {
            "username": "pirouser2",
            "name": "pirouser 2",
            "profile_img": "images/pirouser2.png",
            "posts": 0,
            "followers": 0,
            "following": 0,
            "bio": "소개글이 없습니다.",
        },
        "pirouser3": {
            "username": "pirouser3",
            "name": "pirouser 3",
            "profile_img": "images/pirouser3.png",
            "posts": 0,
            "followers": 0,
            "following": 0,
            "bio": "나는 피로유저",
        },
        "pirouser4": {
            "username": "pirouser4",
            "name": "pirouser 4",
            "profile_img": "images/pirouser4.png",
            "posts": 0,
            "followers": 0,
            "following": 0,
            "bio": "아자아자 파이팅!",
        },
    }

    profile_user = users.get(username)
    target_user = get_object_or_404(User, username=username)
    current_user = get_current_user(request)

    is_following = Follow.objects.filter(
        follower=current_user,
        following=target_user
    ).exists()

    base_followers = int(str(profile_user["followers"]).replace(",", ""))
    base_following = int(str(profile_user["following"]).replace(",", ""))

    db_follower_count = Follow.objects.filter(following=target_user).count()
    db_following_count = Follow.objects.filter(follower=target_user).count()

    follower_count = base_followers + db_follower_count
    following_count = base_following + db_following_count

    posts = Post.objects.filter(author=target_user).order_by("-created_at")

    story_users = [
        users["pirogramming_official"],
        users["pirouser1"],
        users["pirouser2"],
        users["pirouser3"],
        users["pirouser4"],
    ]

    return render(request, 'posts/user_feed.html', {
        'profile_user': profile_user,
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
        'posts': posts,
    })

    user = users.get(username)

    return render(request, 'posts/user_feed.html', {'profile_user': user})

def my_profile(request):
    ensure_demo_users()

    current_user = get_current_user(request)
    profile = get_user_profile(current_user)

    posts = Post.objects.filter(author=current_user).order_by("-created_at")

    post_count = posts.count()
    follower_count = Follow.objects.filter(following=current_user).count()
    following_count = Follow.objects.filter(follower=current_user).count()

    profile_image_url = "/static/images/profile1.webp"

    if profile.image:
        profile_image_url = profile.image.url

    return render(request, "posts/my_profile.html", {
        "posts": posts,
        "post_count": post_count,
        "follower_count": follower_count,
        "following_count": following_count,
        "profile": profile,
        "profile_image_url": profile_image_url,
    })

def user_search(request):
    ensure_demo_users()

    query = request.GET.get("q", "").strip()
    current_user = get_current_user(request)

    user_profiles = []

    profile_data = {
        "wltn1.2": {
            "name": "한지수",
            "profile_img": "images/profile1.webp",
        },
        "pirogramming_official": {
            "name": "피로그래밍",
            "profile_img": "images/piro.png",
        },
        "pirouser1": {
            "name": "pirouser 1",
            "profile_img": "images/pirouser1.png",
        },
        "pirouser2": {
            "name": "pirouser 2",
            "profile_img": "images/pirouser2.png",
        },
        "pirouser3": {
            "name": "pirouser 3",
            "profile_img": "images/pirouser3.png",
        },
        "pirouser4": {
            "name": "pirouser 4",
            "profile_img": "images/pirouser4.png",
        },
    }

    if query:
        users = User.objects.filter(username__icontains=query)

        for user in users:
            data = profile_data.get(user.username, {
                "name": user.username,
                "profile_img": "images/profile1.webp",
            })

            is_following = Follow.objects.filter(
                follower=current_user,
                following=user
            ).exists()

            user_profiles.append({
                "username": user.username,
                "name": data["name"],
                "profile_img": data["profile_img"],
                "is_following": is_following,
                "is_me": user.username == current_user.username,
            })

    return render(request, "posts/user_search.html", {
        "query": query,
        "users": user_profiles,
    })

def post_search(request):
    return render(request, 'posts/post_search.html')

def post_create(request):
    print("post_create view 들어옴:", request.method)

    ensure_demo_users()
    current_user = get_current_user(request)

    if request.method == "POST":
        image = request.FILES.get("image")
        content = request.POST.get("content", "")

        print("image:", image)
        print("content:", content)

        if image:
            Post.objects.create(
                author=current_user,
                image=image,
                content=content
            )

            return redirect("my_profile")

    return render(request, "posts/post_create.html")

def get_current_user(request):
    if request.user.is_authenticated:
        return request.user

    user, created = User.objects.get_or_create(username="wltn1.2")
    return user

def get_user_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile

def ensure_demo_users():
    usernames = [
        "wltn1.2",
        "pirogramming_official",
        "pirouser1",
        "pirouser2",
        "pirouser3",
        "pirouser4",
    ]

    for username in usernames:
        User.objects.get_or_create(username=username)

@require_POST
def toggle_follow(request, username):
    ensure_demo_users()

    current_user = get_current_user(request)
    target_user = get_object_or_404(User, username=username)

    if current_user == target_user:
        return JsonResponse({
            "success": False,
            "message": "자기 자신은 팔로우할 수 없습니다."
        }, status=400)

    follow, created = Follow.objects.get_or_create(
        follower=current_user,
        following=target_user
    )

    if created:
        is_following = True
    else:
        follow.delete()
        is_following = False

    demo_followers = {
        "pirogramming_official": 1387,
        "pirouser1": 120,
        "pirouser2": 95,
        "pirouser3": 77,
        "pirouser4": 50,
    }

    base_followers = demo_followers.get(username, 0)
    follower_count = base_followers + Follow.objects.filter(following=target_user).count()

    return JsonResponse({
        "success": True,
        "is_following": is_following,
        "follower_count": follower_count,
    })

@require_POST
def update_post(request, post_id):
    current_user = get_current_user(request)

    post = get_object_or_404(Post, id=post_id, author=current_user)

    content = request.POST.get("content", "")
    post.content = content
    post.save()

    return JsonResponse({
        "success": True,
        "content": post.content,
    })


@require_POST
def delete_post(request, post_id):
    current_user = get_current_user(request)

    post = get_object_or_404(Post, id=post_id, author=current_user)
    post.delete()

    return JsonResponse({
        "success": True,
    })

@require_POST
def toggle_like(request, post_id):
    current_user = get_current_user(request)
    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        user=current_user,
        post=post
    )

    if created:
        is_liked = True
    else:
        like.delete()
        is_liked = False

    like_count = post.likes.count()

    return JsonResponse({
        "success": True,
        "is_liked": is_liked,
        "like_count": like_count,
    })

def get_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    comments = Comment.objects.filter(post=post).order_by("created_at")

    comment_list = []

    for comment in comments:
        comment_list.append({
            "id": comment.id,
            "username": comment.user.username,
            "content": comment.content,
            "is_owner": comment.user == get_current_user(request),
        })

    return JsonResponse({
        "success": True,
        "comments": comment_list,
        "comment_count": comments.count(),
    })


@require_POST
def create_comment(request, post_id):
    current_user = get_current_user(request)
    post = get_object_or_404(Post, id=post_id)

    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({
            "success": False,
            "message": "댓글 내용을 입력해주세요."
        }, status=400)

    comment = Comment.objects.create(
        user=current_user,
        post=post,
        content=content
    )

    comment_count = post.comments.count()

    return JsonResponse({
        "success": True,
        "comment": {
            "id": comment.id,
            "username": comment.user.username,
            "content": comment.content,
            "is_owner": True,
        },
        "comment_count": comment_count,
    })


@require_POST
def update_comment(request, comment_id):
    current_user = get_current_user(request)

    comment = get_object_or_404(Comment, id=comment_id, user=current_user)

    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({
            "success": False,
            "message": "댓글 내용을 입력해주세요."
        }, status=400)

    comment.content = content
    comment.save()

    return JsonResponse({
        "success": True,
        "content": comment.content,
    })


@require_POST
def delete_comment(request, comment_id):
    current_user = get_current_user(request)

    comment = get_object_or_404(Comment, id=comment_id, user=current_user)
    post = comment.post

    comment.delete()

    comment_count = post.comments.count()

    return JsonResponse({
        "success": True,
        "comment_count": comment_count,
    })

def get_user_stories(request, username):
    user = get_object_or_404(User, username=username)

    stories = Story.objects.filter(user=user).order_by("created_at")

    story_list = []

    for story in stories:
        story_list.append({
            "id": story.id,
            "image_url": story.image.url,
            "created_at": story.created_at.strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse({
        "success": True,
        "username": user.username,
        "stories": story_list,
    })


@require_POST
def create_story(request):
    ensure_demo_users()

    current_user = get_current_user(request)
    image = request.FILES.get("image")

    if not image:
        return JsonResponse({
            "success": False,
            "message": "이미지를 선택해주세요."
        }, status=400)

    story = Story.objects.create(
        user=current_user,
        image=image
    )

    return JsonResponse({
        "success": True,
        "story": {
            "id": story.id,
            "image_url": story.image.url,
        }
    })

def story_detail(request, user_id):
    story_user = get_object_or_404(User, id=user_id)
    stories = Story.objects.filter(user=story_user).order_by("-created_at")

    return render(request, "posts/story_detail.html", {
        "story_user": story_user,
        "stories": stories,
    })

@require_POST
def update_profile(request):
    current_user = get_current_user(request)
    profile = get_user_profile(current_user)

    bio = request.POST.get("bio", "")
    image = request.FILES.get("image")

    print("업로드 이미지:", image)

    profile.bio = bio

    if image:
        profile.image = image

    profile.save()

    profile_image_url = "/static/images/profile1.webp"

    if profile.image:
        profile_image_url = profile.image.url

    return JsonResponse({
        "success": True,
        "bio": profile.bio,
        "profile_image_url": profile_image_url,
    })