function getCookie(name) {
    const cookies = document.cookie
        ? document.cookie.split(";")
        : [];

    for (const cookieValue of cookies) {
        const cookie = cookieValue.trim();

        if (cookie.startsWith(`${name}=`)) {
            return decodeURIComponent(
                cookie.substring(name.length + 1)
            );
        }
    }

    return null;
}


function formatLabel(label) {
    const labels = {
        positive: "Positive",
        neutral: "Neutral",
        negative: "Negative",
    };

    return labels[label] ?? label;
}


function formatPercent(score) {
    return `${(score * 100).toFixed(2)}%`;
}


function escapeHtml(value) {
    const element = document.createElement("div");
    element.textContent = value;
    return element.innerHTML;
}


document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(
        "#sentiment-form"
    );

    if (!form) {
        return;
    }

    const input = document.querySelector(
        "#sentiment-input"
    );

    const button = document.querySelector(
        "#sentiment-button"
    );

    const count = document.querySelector(
        "#character-count"
    );

    const loadingMessage = document.querySelector(
        "#loading-message"
    );

    const errorMessage = document.querySelector(
        "#error-message"
    );

    const resultSection = document.querySelector(
        "#result-section"
    );

    const resultLabel = document.querySelector(
        "#result-label"
    );

    const resultScore = document.querySelector(
        "#result-score"
    );

    const allScores = document.querySelector(
        "#all-scores"
    );

    const historyList = document.querySelector(
        "#history-list"
    );

    const guestHistories = [];

    input.addEventListener("input", () => {
        count.textContent =
            `${input.value.length} / 1,000`;
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        errorMessage.hidden = true;
        resultSection.hidden = true;
        loadingMessage.hidden = false;

        button.disabled = true;
        input.disabled = true;

        try {
            const response = await fetch(
                sentimentRunUrl,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie(
                            "csrftoken"
                        ),
                    },
                    body: JSON.stringify({
                        text: input.value,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error ??
                    "요청 처리에 실패했습니다."
                );
            }

            resultLabel.textContent =
                formatLabel(data.label);

            resultScore.textContent =
                formatPercent(data.score);

            allScores.innerHTML =
                data.all_scores
                    .map((item) => {
                        return `
                            <p>
                                ${formatLabel(item.label)}:
                                ${formatPercent(item.score)}
                            </p>
                        `;
                    })
                    .join("");

            resultSection.hidden = false;

            addHistory(data);
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.hidden = false;
        } finally {
            loadingMessage.hidden = true;
            button.disabled = false;
            input.disabled = false;
        }
    });


    function addHistory(data) {
        const history = {
            input_text: data.input_text,
            label: data.label,
            score: data.score,
            created_at: data.created_at,
        };

        if (!isAuthenticated) {
            guestHistories.unshift(history);

            if (guestHistories.length > 5) {
                guestHistories.pop();
            }

            renderGuestHistories();
            return;
        }

        const emptyHistory = document.querySelector(
            "#empty-history"
        );

        if (emptyHistory) {
            emptyHistory.remove();
        }

        const item = createHistoryElement(history);

        historyList.prepend(item);

        const historyItems = historyList.querySelectorAll(
            ".history-item"
        );

        if (historyItems.length > 5) {
            historyItems[
                historyItems.length - 1
            ].remove();
        }
    }


    function renderGuestHistories() {
        historyList.innerHTML = "";

        for (const history of guestHistories) {
            historyList.appendChild(
                createHistoryElement(history)
            );
        }
    }


    function createHistoryElement(history) {
        const article =
            document.createElement("article");

        article.className = "history-item";

        const shortenedInput =
            history.input_text.length > 100
                ? `${history.input_text.slice(0, 100)}...`
                : history.input_text;

        article.innerHTML = `
            <p class="history-input">
                ${escapeHtml(shortenedInput)}
            </p>

            <p>
                ${formatLabel(history.label)}
                ·
                ${formatPercent(history.score)}
            </p>

            ${
                history.created_at
                    ? `<time>${history.created_at}</time>`
                    : ""
            }
        `;

        return article;
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(
        "#summarize-form"
    );

    if (!form) {
        return;
    }

    const input = document.querySelector(
        "#summarize-input"
    );

    const button = document.querySelector(
        "#summarize-button"
    );

    const count = document.querySelector(
        "#summarize-character-count"
    );

    const loading = document.querySelector(
        "#summarize-loading"
    );

    const errorMessage = document.querySelector(
        "#summarize-error"
    );

    const resultSection = document.querySelector(
        "#summarize-result"
    );

    const originalLength = document.querySelector(
        "#original-length"
    );

    const summaryLength = document.querySelector(
        "#summary-length"
    );

    const summaryRatio = document.querySelector(
        "#summary-ratio"
    );

    const summaryText = document.querySelector(
        "#summary-text"
    );

    const historyList = document.querySelector(
        "#summarize-history-list"
    );

    input.addEventListener("input", () => {
        count.textContent =
            `${input.value.length} / 5,000`;
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        errorMessage.hidden = true;
        resultSection.hidden = true;
        loading.hidden = false;

        button.disabled = true;
        input.disabled = true;

        try {
            const response = await fetch(
                summarizeRunUrl,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie(
                            "csrftoken"
                        ),
                    },
                    body: JSON.stringify({
                        text: input.value,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error ??
                    "요청 처리에 실패했습니다."
                );
            }

            originalLength.textContent =
                `${data.original_length}자`;

            summaryLength.textContent =
                `${data.summary_length}자`;

            summaryRatio.textContent =
                `${data.summary_ratio.toFixed(2)}%`;

            summaryText.textContent =
                data.summary;

            resultSection.hidden = false;

            addSummarizeHistory(data);
        } catch (error) {
            errorMessage.textContent =
                error.message;

            errorMessage.hidden = false;
        } finally {
            loading.hidden = true;
            button.disabled = false;
            input.disabled = false;
        }
    });


    function addSummarizeHistory(data) {
        const emptyHistory =
            document.querySelector(
                "#summarize-empty-history"
            );

        if (emptyHistory) {
            emptyHistory.remove();
        }

        const article =
            document.createElement("article");

        article.className = "history-item";

        const inputPreview =
            data.input_text.length > 100
                ? `${data.input_text.slice(0, 100)}...`
                : data.input_text;

        const summaryPreview =
            data.summary.length > 180
                ? `${data.summary.slice(0, 180)}...`
                : data.summary;

        article.innerHTML = `
            <p class="history-input">
                ${escapeHtml(inputPreview)}
            </p>

            <p>
                ${escapeHtml(summaryPreview)}
            </p>

            <time>
                ${escapeHtml(data.created_at)}
            </time>
        `;

        historyList.prepend(article);

        const items =
            historyList.querySelectorAll(
                ".history-item"
            );

        if (items.length > 5) {
            items[items.length - 1].remove();
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(
        "#moderate-form"
    );

    if (!form) {
        return;
    }

    const input = document.querySelector(
        "#moderate-input"
    );

    const button = document.querySelector(
        "#moderate-button"
    );

    const count = document.querySelector(
        "#moderate-character-count"
    );

    const loading = document.querySelector(
        "#moderate-loading"
    );

    const errorMessage = document.querySelector(
        "#moderate-error"
    );

    const resultSection = document.querySelector(
        "#moderate-result"
    );

    const highestLabel = document.querySelector(
        "#highest-label"
    );

    const highestScore = document.querySelector(
        "#highest-score"
    );

    const allScores = document.querySelector(
        "#moderate-all-scores"
    );

    const historyList = document.querySelector(
        "#moderate-history-list"
    );

    input.addEventListener("input", () => {
        count.textContent =
            `${input.value.length} / 1,000`;
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        errorMessage.hidden = true;
        resultSection.hidden = true;
        loading.hidden = false;

        button.disabled = true;
        input.disabled = true;

        try {
            const response = await fetch(
                moderateRunUrl,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie(
                            "csrftoken"
                        ),
                    },
                    body: JSON.stringify({
                        text: input.value,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error ??
                    "요청 처리에 실패했습니다."
                );
            }

            highestLabel.textContent =
                data.highest_label;

            highestScore.textContent =
                formatPercent(data.highest_score);

            allScores.innerHTML =
                data.all_scores
                    .map((item) => {
                        return `
                            <p>
                                ${escapeHtml(item.label)}:
                                ${formatPercent(item.score)}
                            </p>
                        `;
                    })
                    .join("");

            resultSection.hidden = false;

            addModerateHistory(data);
        } catch (error) {
            errorMessage.textContent =
                error.message;

            errorMessage.hidden = false;
        } finally {
            loading.hidden = true;
            button.disabled = false;
            input.disabled = false;
        }
    });


    function addModerateHistory(data) {
        const emptyHistory =
            document.querySelector(
                "#moderate-empty-history"
            );

        if (emptyHistory) {
            emptyHistory.remove();
        }

        const article =
            document.createElement("article");

        article.className = "history-item";

        const inputPreview =
            data.input_text.length > 100
                ? `${data.input_text.slice(0, 100)}...`
                : data.input_text;

        article.innerHTML = `
            <p class="history-input">
                ${escapeHtml(inputPreview)}
            </p>

            <p>
                ${escapeHtml(data.highest_label)}
                ·
                ${formatPercent(data.highest_score)}
            </p>

            <time>
                ${escapeHtml(data.created_at)}
            </time>
        `;

        historyList.prepend(article);

        const items =
            historyList.querySelectorAll(
                ".history-item"
            );

        if (items.length > 5) {
            items[items.length - 1].remove();
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(
        "#combo-form"
    );

    if (!form) {
        return;
    }

    const input = document.querySelector(
        "#combo-input"
    );

    const button = document.querySelector(
        "#combo-button"
    );

    const regenerateButton = document.querySelector(
        "#regenerate-button"
    );

    const count = document.querySelector(
        "#combo-character-count"
    );

    const loading = document.querySelector(
        "#combo-loading"
    );

    const errorMessage = document.querySelector(
        "#combo-error"
    );

    const resultSection = document.querySelector(
        "#combo-result"
    );

    const originalText = document.querySelector(
        "#combo-original-text"
    );

    const summary = document.querySelector(
        "#combo-summary"
    );

    const sentimentLabel = document.querySelector(
        "#combo-sentiment-label"
    );

    const sentimentScore = document.querySelector(
        "#combo-sentiment-score"
    );

    const toxicityLabel = document.querySelector(
        "#combo-toxicity-label"
    );

    const toxicityScore = document.querySelector(
        "#combo-toxicity-score"
    );

    const allScores = document.querySelector(
        "#combo-all-scores"
    );

    const overallResult = document.querySelector(
        "#combo-overall-result"
    );

    const historyList = document.querySelector(
        "#combo-history-list"
    );

    let savedOriginalText = "";

    input.addEventListener("input", () => {
        count.textContent =
            `${input.value.length} / 5,000`;
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        await executeCombo(
            input.value,
            false,
        );
    });

    regenerateButton.addEventListener(
        "click",
        async () => {
            if (!savedOriginalText) {
                return;
            }

            await executeCombo(
                savedOriginalText,
                true,
            );
        }
    );


    async function executeCombo(
        text,
        regenerate
    ) {
        errorMessage.hidden = true;
        loading.hidden = false;

        button.disabled = true;
        regenerateButton.disabled = true;
        input.disabled = true;

        try {
            const response = await fetch(
                comboRunUrl,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/json",
                        "X-CSRFToken": getCookie(
                            "csrftoken"
                        ),
                    },
                    body: JSON.stringify({
                        text,
                        regenerate,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.error ??
                    "요청 처리에 실패했습니다."
                );
            }

            savedOriginalText =
                data.input_text;

            originalText.textContent =
                data.input_text;

            summary.textContent =
                data.summary;

            sentimentLabel.textContent =
                formatLabel(
                    data.sentiment.label
                );

            sentimentScore.textContent =
                formatPercent(
                    data.sentiment.score
                );

            toxicityLabel.textContent =
                data.toxicity.highest_label;

            toxicityScore.textContent =
                formatPercent(
                    data.toxicity.highest_score
                );

            allScores.innerHTML =
                data.toxicity.all_scores
                    .map((item) => {
                        return `
                            <p>
                                ${escapeHtml(item.label)}:
                                ${formatPercent(item.score)}
                            </p>
                        `;
                    })
                    .join("");

            overallResult.textContent =
                data.overall_result;

            resultSection.hidden = false;

            addComboHistory(data);
        } catch (error) {
            errorMessage.textContent =
                error.message;

            errorMessage.hidden = false;
        } finally {
            loading.hidden = true;
            button.disabled = false;
            regenerateButton.disabled = false;
            input.disabled = false;
        }
    }


    function addComboHistory(data) {
        const emptyHistory =
            document.querySelector(
                "#combo-empty-history"
            );

        if (emptyHistory) {
            emptyHistory.remove();
        }

        const article =
            document.createElement("article");

        article.className = "history-item";

        const inputPreview =
            data.input_text.length > 100
                ? `${data.input_text.slice(0, 100)}...`
                : data.input_text;

        const summaryPreview =
            data.summary.length > 180
                ? `${data.summary.slice(0, 180)}...`
                : data.summary;

        article.innerHTML = `
            <p class="history-input">
                ${escapeHtml(inputPreview)}
            </p>

            <p>
                ${escapeHtml(summaryPreview)}
            </p>

            <p>
                ${escapeHtml(data.overall_result)}
            </p>

            <time>
                ${escapeHtml(data.created_at)}
            </time>
        `;

        historyList.prepend(article);

        const items =
            historyList.querySelectorAll(
                ".history-item"
            );

        if (items.length > 5) {
            items[items.length - 1].remove();
        }
    }
});