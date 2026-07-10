document.addEventListener("DOMContentLoaded", function () {

    const sendBtn = document.querySelector(".send");
    const input = document.querySelector(".input-area input");
    const chatBox = document.querySelector(".chat-box");

    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");

    // ===========================
    // Send Message Function
    // ===========================

    async function sendMessage() {

        const message = input.value.trim();

        if (message === "") {
            alert("Please enter your question.");
            return;
        }

        // User Message
        const userMsg = document.createElement("div");
        userMsg.className = "user-message";
        userMsg.innerHTML = message;

        chatBox.appendChild(userMsg);

        input.value = "";

        // Loading Message
        const loading = document.createElement("div");
        loading.className = "bot-message";
        loading.innerHTML = "🤖 CampusPilot is thinking...";

        chatBox.appendChild(loading);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {

            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const data = await response.json();

            loading.remove();

            const botMsg = document.createElement("div");
            botMsg.className = "bot-message";
            botMsg.innerHTML = "🤖 " + data.response;

            chatBox.appendChild(botMsg);

            chatBox.scrollTop = chatBox.scrollHeight;

        }
        catch (error) {

            loading.remove();

            const botMsg = document.createElement("div");
            botMsg.className = "bot-message";
            botMsg.innerHTML = "❌ Error connecting to IBM Granite AI.";

            chatBox.appendChild(botMsg);

        }

    }

    // Send Button
    sendBtn.addEventListener("click", sendMessage);

    // Press Enter to Send
    input.addEventListener("keypress", function (e) {

        if (e.key === "Enter") {
            sendMessage();
        }

    });

    // ===========================
    // Upload Button
    // ===========================

    uploadBtn.addEventListener("click", function () {

        fileInput.click();

    });

    fileInput.addEventListener("change", async function () {

        const file = fileInput.files[0];

        if (!file) return;

        const formData = new FormData();

        formData.append("file", file);

        try {

            const response = await fetch("/upload", {
                method: "POST",
                body: formData

            });

            const data = await response.json();

            const botMsg = document.createElement("div");
            botMsg.className = "bot-message";
          botMsg.innerHTML =
    "📄 " + data.message +
    "<br><br><b>📝 AI Summary</b><br><br>" +
    data.summary;

            chatBox.appendChild(botMsg);

            chatBox.scrollTop = chatBox.scrollHeight;

        }
        catch {

            const botMsg = document.createElement("div");
            botMsg.className = "bot-message";
            botMsg.innerHTML = "❌ File upload failed.";

            chatBox.appendChild(botMsg);

        }

    });

});