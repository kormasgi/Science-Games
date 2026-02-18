const output = document.getElementById("output");
const startBtn = document.getElementById("startBtn");

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
  output.textContent = "Speech recognition not supported in this browser.";
} else {

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.continuous = false; // stops after one phrase
  recognition.interimResults = false;

  recognition.onstart = () => {
    output.textContent = "Listening...";
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    output.textContent = "You said: " + transcript;
  };

  recognition.onspeechend = () => {
    recognition.stop();
    output.textContent += " (Stopped listening)";
  };

  recognition.onerror = (event) => {
    console.error("Error:", event.error);
  };

  startBtn.onclick = () => {
    recognition.start();
  };
}
