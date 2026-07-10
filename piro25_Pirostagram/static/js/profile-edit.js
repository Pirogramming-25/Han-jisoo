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

const profileEditOpenBtn = document.querySelector("#profileEditOpenBtn");
const profileEditModal = document.querySelector("#profileEditModal");
const profileEditOverlay = document.querySelector("#profileEditOverlay");
const profileEditCloseBtn = document.querySelector("#profileEditCloseBtn");
const profileEditForm = document.querySelector("#profileEditForm");

const profileImageInput = document.querySelector("#profileImageInput");
const profileEditPreviewImg = document.querySelector("#profileEditPreviewImg");
const profileBioInput = document.querySelector("#profileBioInput");

const myProfileImg = document.querySelector("#myProfileImg");
const myProfileBio = document.querySelector("#myProfileBio");

const originalPreviewSrc = profileEditPreviewImg.src;

profileEditOpenBtn.addEventListener("click", () => {
    profileEditModal.classList.add("active");

    profileEditPreviewImg.src = myProfileImg.src;
});

function closeProfileEditModal() {
    profileEditModal.classList.remove("active");

    profileImageInput.value = "";
    profileEditPreviewImg.src = myProfileImg.src;
}

profileEditOverlay.addEventListener("click", closeProfileEditModal);
profileEditCloseBtn.addEventListener("click", closeProfileEditModal);

profileImageInput.addEventListener("change", () => {
    const file = profileImageInput.files[0];

    if (!file) {
        return;
    }

    const imageUrl = URL.createObjectURL(file);

    // 여기서는 팝업 안 미리보기만 바뀜
    profileEditPreviewImg.src = imageUrl;
});

profileEditForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData();

    const image = profileImageInput.files[0];
    const bio = profileBioInput.value;

    if (image) {
        formData.append("image", image);
    }

    formData.append("bio", bio);

    fetch("/profile/update/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (!data.success) {
                alert("프로필 수정에 실패했습니다.");
                return;
            }

            const newImageUrl = data.profile_image_url + "?t=" + new Date().getTime();

            // 저장 버튼을 누른 뒤에만 실제 프로필 사진 변경
            myProfileImg.src = newImageUrl;
            profileEditPreviewImg.src = newImageUrl;

            if (data.bio) {
                myProfileBio.textContent = data.bio;
            } else {
                myProfileBio.textContent = "소개글이 없습니다.";
            }

            profileImageInput.value = "";
            closeProfileEditModal();
        });
});