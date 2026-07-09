function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }

    return null;
}

const likeButtons = document.querySelectorAll(".like-toggle-btn");

likeButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const postId = button.dataset.postId;
        const likeCount = button.parentElement.querySelector(".like-count");

        fetch(`/posts/${postId}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    alert("좋아요 처리에 실패했습니다.");
                    return;
                }

                likeCount.textContent = data.like_count;

                const heartIcon = button.querySelector(".post-action-icon");

                if (data.is_liked) {
                    button.classList.add("liked");
                    heartIcon.src = heartIcon.dataset.filledSrc;
                } else {
                    button.classList.remove("liked");
                    heartIcon.src = heartIcon.dataset.emptySrc;
                }
            });
    });
});