const fileInput = document.querySelector("#post-image");
const previewImg = document.querySelector("#previewImg");
const uploadIcon = document.querySelector("#uploadIcon");
const uploadText = document.querySelector("#uploadText");

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    const imageUrl = URL.createObjectURL(file);

    previewImg.src = imageUrl;
    previewImg.style.display = "block";

    uploadIcon.style.display = "none";
    uploadText.style.display = "none";
});