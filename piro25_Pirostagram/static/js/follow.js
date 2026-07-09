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

const followButtons = document.querySelectorAll(".follow-toggle-btn");

followButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const username = button.dataset.username;

        fetch(`/users/${username}/follow/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (!data.success) {
                    alert(data.message);
                    return;
                }

                if (data.is_following) {
                    button.textContent = "팔로잉";
                    button.classList.remove("not-following");
                    button.classList.add("following");
                } else {
                    button.textContent = "팔로우";
                    button.classList.remove("following");
                    button.classList.add("not-following");
                }

                const followerCount = document.querySelector("#followerCount");

                if (followerCount) {
                    followerCount.textContent = data.follower_count;
                }
            });
    });
});