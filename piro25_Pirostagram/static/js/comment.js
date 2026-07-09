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

const commentModal = document.querySelector("#commentModal");
const commentModalOverlay = document.querySelector("#commentModalOverlay");
const commentModalCloseBtn = document.querySelector("#commentModalCloseBtn");

const commentModalImg = document.querySelector("#commentModalImg");
const commentPostAuthor = document.querySelector("#commentPostAuthor");
const commentPostContent = document.querySelector("#commentPostContent");

const commentList = document.querySelector("#commentList");
const commentForm = document.querySelector("#commentForm");
const commentInput = document.querySelector("#commentInput");

const commentOpenButtons = document.querySelectorAll(".comment-open-btn");

let currentPostId = null;
let currentCommentCountElement = null;

function openCommentModal(button) {
    currentPostId = button.dataset.postId;
    currentCommentCountElement = button.parentElement.querySelector(".comment-count");

    commentModalImg.src = button.dataset.postImage;
    commentPostAuthor.textContent = button.dataset.postAuthor;
    commentPostContent.textContent = button.dataset.postContent;

    commentInput.value = "";
    commentModal.classList.add("active");

    loadComments();
}

function closeCommentModal() {
    commentModal.classList.remove("active");
    currentPostId = null;
    currentCommentCountElement = null;
    commentList.innerHTML = "";
}

commentOpenButtons.forEach((button) => {
    button.addEventListener("click", () => {
        openCommentModal(button);
    });
});

commentModalOverlay.addEventListener("click", closeCommentModal);
commentModalCloseBtn.addEventListener("click", closeCommentModal);

function loadComments() {
    fetch(`/posts/${currentPostId}/comments/`)
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert("댓글을 불러오지 못했습니다.");
                return;
            }

            commentList.innerHTML = "";

            data.comments.forEach((comment) => {
                addCommentToList(comment);
            });

            if (currentCommentCountElement) {
                currentCommentCountElement.textContent = data.comment_count;
            }
        });
}

function addCommentToList(comment) {
    const commentItem = document.createElement("div");
    commentItem.classList.add("comment-item");
    commentItem.dataset.commentId = comment.id;

    let actionButtons = "";

    if (comment.is_owner) {
        actionButtons = `
            <div class="comment-actions">
                <button type="button" class="comment-edit-btn">수정</button>
                <button type="button" class="comment-delete-btn">삭제</button>
            </div>
        `;
    }

    commentItem.innerHTML = `
        <div class="comment-main">
            <strong class="comment-username">${comment.username}</strong>
            <span class="comment-content">${comment.content}</span>
        </div>
        ${actionButtons}
    `;

    commentList.appendChild(commentItem);

    if (comment.is_owner) {
        const editBtn = commentItem.querySelector(".comment-edit-btn");
        const deleteBtn = commentItem.querySelector(".comment-delete-btn");

        editBtn.addEventListener("click", () => {
            editComment(commentItem);
        });

        deleteBtn.addEventListener("click", () => {
            deleteComment(commentItem);
        });
    }
}

commentForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const content = commentInput.value.trim();

    if (!content) {
        return;
    }

    const formData = new FormData();
    formData.append("content", content);

    fetch(`/posts/${currentPostId}/comments/create/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert(data.message || "댓글 작성에 실패했습니다.");
                return;
            }

            addCommentToList(data.comment);
            commentInput.value = "";

            if (currentCommentCountElement) {
                currentCommentCountElement.textContent = data.comment_count;
            }
        });
});

function editComment(commentItem) {
    const commentId = commentItem.dataset.commentId;
    const contentSpan = commentItem.querySelector(".comment-content");
    const editBtn = commentItem.querySelector(".comment-edit-btn");

    if (editBtn.textContent === "수정") {
        const currentContent = contentSpan.textContent;

        contentSpan.innerHTML = `
            <input 
                type="text" 
                class="comment-edit-input" 
                value="${currentContent}"
            >
        `;

        editBtn.textContent = "저장";
        return;
    }

    const editInput = commentItem.querySelector(".comment-edit-input");
    const newContent = editInput.value.trim();

    if (!newContent) {
        return;
    }

    const formData = new FormData();
    formData.append("content", newContent);

    fetch(`/comments/${commentId}/update/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert(data.message || "댓글 수정에 실패했습니다.");
                return;
            }

            contentSpan.textContent = data.content;
            editBtn.textContent = "수정";
        });
}

function deleteComment(commentItem) {
    const commentId = commentItem.dataset.commentId;

    const isConfirmed = confirm("댓글을 삭제하시겠습니까?");

    if (!isConfirmed) {
        return;
    }

    fetch(`/comments/${commentId}/delete/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert("댓글 삭제에 실패했습니다.");
                return;
            }

            commentItem.remove();

            if (currentCommentCountElement) {
                currentCommentCountElement.textContent = data.comment_count;
            }
        });
}