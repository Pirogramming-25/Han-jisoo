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

const postModal = document.querySelector("#postModal");
const postModalOverlay = document.querySelector("#postModalOverlay");
const postModalCloseBtn = document.querySelector("#postModalCloseBtn");
const postModalImg = document.querySelector("#postModalImg");
const postModalCaptionInput = document.querySelector("#postModalCaptionInput");
const postEditBtn = document.querySelector("#postEditBtn");
const postDeleteBtn = document.querySelector("#postDeleteBtn");

const postOpenButtons = document.querySelectorAll(".post-modal-open-btn");

let currentPostId = null;
let currentPostButton = null;
let isEditMode = false;

postOpenButtons.forEach((button) => {
    button.addEventListener("click", () => {
        currentPostId = button.dataset.postId;
        currentPostButton = button;

        postModalImg.src = button.dataset.postImage;
        postModalCaptionInput.value = button.dataset.postContent;

        postModalCaptionInput.setAttribute("readonly", true);
        postEditBtn.textContent = "수정";
        isEditMode = false;

        postModal.classList.add("active");
    });
});

function closePostModal() {
    postModal.classList.remove("active");

    currentPostId = null;
    currentPostButton = null;
    isEditMode = false;

    postModalCaptionInput.setAttribute("readonly", true);
    postEditBtn.textContent = "수정";
}

postModalOverlay.addEventListener("click", closePostModal);
postModalCloseBtn.addEventListener("click", closePostModal);

postEditBtn.addEventListener("click", () => {
    if (!currentPostId) {
        return;
    }

    if (!isEditMode) {
        isEditMode = true;

        postModalCaptionInput.removeAttribute("readonly");
        postModalCaptionInput.focus();

        postEditBtn.textContent = "저장";
        return;
    }

    const formData = new FormData();
    formData.append("content", postModalCaptionInput.value);

    fetch(`/posts/${currentPostId}/update/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert("수정에 실패했습니다.");
                return;
            }

            currentPostButton.dataset.postContent = data.content;

            postModalCaptionInput.setAttribute("readonly", true);
            postEditBtn.textContent = "수정";
            isEditMode = false;

            alert("게시글이 수정되었습니다.");
        });
});

postDeleteBtn.addEventListener("click", () => {
    if (!currentPostId) {
        return;
    }

    const isConfirmed = confirm("정말 이 게시글을 삭제하시겠습니까?");

    if (!isConfirmed) {
        return;
    }

    fetch(`/posts/${currentPostId}/delete/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert("삭제에 실패했습니다.");
                return;
            }

            if (currentPostButton) {
                currentPostButton.remove();
            }

            const postCount = document.querySelector("#postCount");

            if (postCount) {
                const currentCount = Number(postCount.textContent);
                postCount.textContent = Math.max(currentCount - 1, 0);
            }

            closePostModal();
        });
});