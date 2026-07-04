const askButton = document.getElementById("askButton");
const chat = document.getElementById("chat");
const questionBox = document.getElementById("question");

let isLoading = false;

// ------------------------------
// Add Chat Message
// ------------------------------
function addMessage(text, cls){

    const div = document.createElement("div");

    div.classList.add("message");

    div.classList.add(cls);

    div.innerText = text;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;

    return div;

}

// ------------------------------
// Ask AI
// ------------------------------
async function askQuestion() {

    if (isLoading)
        return;

    const question = questionBox.value.trim();

    if (question === "")
        return;

    isLoading = true;

    askButton.disabled = true;
    askButton.innerText = "...";

    addMessage(question, "user");

    questionBox.value = "";

    const loadingMessage = addMessage(
        "Thinking...",
        "ai"
    );

    try {

        const tabs = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        const url = tabs[0].url;

        if (!url.includes("youtube.com/watch")) {

            loadingMessage.innerText =
                "Please open a YouTube video.";

            return;
        }

        const videoId =
            new URL(url).searchParams.get("v");

        const response = await fetch(
            "http://127.0.0.1:8000/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    video_id: videoId,
                    question: question
                })
            }
        );

        if (!response.ok) {

            loadingMessage.innerText =
                "Server Error.";

            return;
        }

        const data = await response.json();

        loadingMessage.innerText =
            data.answer;

    }
    catch (err) {

        console.error(err);

        loadingMessage.innerText =
            "Cannot connect to backend.";

    }
    finally {

        isLoading = false;

        askButton.disabled = false;

        askButton.innerText = "➤";
    }

}

// ------------------------------
// Button Click
// ------------------------------
askButton.addEventListener(
    "click",
    askQuestion
);

// ------------------------------
// Press Enter
// ------------------------------
questionBox.addEventListener(
    "keydown",
    function(event){

        if(event.key==="Enter" && !event.shiftKey){

            event.preventDefault();

            askQuestion();

        }

    }
);