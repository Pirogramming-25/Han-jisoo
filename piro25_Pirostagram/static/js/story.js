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

/* =========================
스토리 보기
========================= */

const storyModal = document.querySelector("#storyModal");
const storyModalOverlay = document.querySelector("#storyModalOverlay");
const storyModalCloseBtn = document.querySelector("#storyModalCloseBtn");
const storyModalUsername = document.querySelector("#storyModalUsername");
const storyModalImg = document.querySelector("#storyModalImg");
const storyPrevBtn = document.querySelector("#storyPrevBtn");
const storyNextBtn = document.querySelector("#storyNextBtn");

const storyOpenButtons = document.querySelectorAll(".story-open-btn");

let currentStories = [];
let currentStoryIndex = 0;

storyOpenButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const username = button.dataset.username;

        fetch(`/stories/${username}/`)
            .then((response) => response.json())
            .then((data) => {
                if (!data.success || data.stories.length === 0) {
                    alert("볼 수 있는 스토리가 없습니다.");
                    return;
                }

                currentStories = data.stories;
                currentStoryIndex = 0;

                storyModalUsername.textContent = data.username;
                showCurrentStory();

                storyModal.classList.add("active");
            });
    });
});

function showCurrentStory() {
    const story = currentStories[currentStoryIndex];

    storyModalImg.src = story.image_url;

    if (currentStoryIndex === 0) {
        storyPrevBtn.style.visibility = "hidden";
    } else {
        storyPrevBtn.style.visibility = "visible";
    }

    if (currentStoryIndex === currentStories.length - 1) {
        storyNextBtn.style.visibility = "hidden";
    } else {
        storyNextBtn.style.visibility = "visible";
    }
}

storyPrevBtn.addEventListener("click", () => {
    if (currentStoryIndex > 0) {
        currentStoryIndex -= 1;
        showCurrentStory();
    }
});

storyNextBtn.addEventListener("click", () => {
    if (currentStoryIndex < currentStories.length - 1) {
        currentStoryIndex += 1;
        showCurrentStory();
    }
});

function closeStoryModal() {
    storyModal.classList.remove("active");
    currentStories = [];
    currentStoryIndex = 0;
    storyModalImg.src = "";
}

storyModalOverlay.addEventListener("click", closeStoryModal);
storyModalCloseBtn.addEventListener("click", closeStoryModal);


/* =========================
스토리 업로드
========================= */

const storyUploadOpenBtn = document.querySelector("#storyUploadOpenBtn");
const storyUploadModal = document.querySelector("#storyUploadModal");
const storyUploadOverlay = document.querySelector("#storyUploadOverlay");
const storyUploadCloseBtn = document.querySelector("#storyUploadCloseBtn");
const storyUploadForm = document.querySelector("#storyUploadForm");
const storyImageInput = document.querySelector("#storyImageInput");
const storyUploadBox = document.querySelector("#storyUploadBox");
const storyUploadIcon = document.querySelector("#storyUploadIcon");
const storyPreviewImg = document.querySelector("#storyPreviewImg");
const storyUploadText = document.querySelector("#storyUploadText");

storyUploadOpenBtn.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();

    storyUploadModal.classList.add("active");
});

storyUploadBox.addEventListener("click", () => {
    storyImageInput.click();
});

function closeStoryUploadModal() {
    storyUploadModal.classList.remove("active");

    storyImageInput.value = "";
    storyPreviewImg.src = "";
    storyPreviewImg.style.display = "none";

    storyUploadIcon.style.display = "block";
    storyUploadText.style.display = "block";
}

storyUploadOverlay.addEventListener("click", closeStoryUploadModal);
storyUploadCloseBtn.addEventListener("click", closeStoryUploadModal);

storyImageInput.addEventListener("change", () => {
    const file = storyImageInput.files[0];

    if (!file) {
        return;
    }

    const imageUrl = URL.createObjectURL(file);

    storyPreviewImg.src = imageUrl;
    storyPreviewImg.style.display = "block";

    storyUploadIcon.style.display = "none";
    storyUploadText.style.display = "none";
});

storyUploadForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const file = storyImageInput.files[0];

    if (!file) {
        alert("이미지를 선택해주세요.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    fetch("/stories/create/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert(data.message || "스토리 업로드에 실패했습니다.");
                return;
            }

            alert("스토리가 업로드되었습니다.");
            window.location.reload();
        });
});