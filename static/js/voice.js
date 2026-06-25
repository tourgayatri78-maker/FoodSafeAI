function startVoiceInput() {

    if (!('webkitSpeechRecognition' in window)) {
        alert("Speech Recognition not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";
    recognition.start();

    recognition.onstart = function() {
        alert("Speak now...");
    };

    recognition.onresult = function(event) {

        let speech =
            event.results[0][0].transcript;

        alert("You said: " + speech);

        document.getElementById("food1").value = speech;
    };

    recognition.onerror = function(event) {
        alert("Error: " + event.error);
    };
}