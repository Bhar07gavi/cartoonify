async function sendChat() {

    const input = document.getElementById("chatInput")
    const message = input.value

    if (!message) return

    const chatBox = document.getElementById("chatMessages")

    chatBox.innerHTML += `<p><b>You:</b> ${message}</p>`

    const res = await fetch("/api/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message
        })

    })

    const data = await res.json()

    chatBox.innerHTML += `<p><b>AI:</b> ${data.reply}</p>`

    input.value = ""

    chatBox.scrollTop = chatBox.scrollHeight

}