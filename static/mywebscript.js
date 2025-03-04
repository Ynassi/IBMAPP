let RunSentimentAnalysis = () => {
    let textToAnalyze = document.getElementById("textToAnalyze").value;

    fetch("/sentiment_analyser", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: textToAnalyze })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errData => { throw new Error(errData.error || "Invalid response from server"); });
        }
        return response.json();
    })
    .then(data => {
        if (!data.label) {
            document.getElementById("system_response").innerHTML = "Invalid input! Try again.";
        } else {
            document.getElementById("system_response").innerHTML = `Sentiment: ${data.label} (Score: ${data.score})`;
        }
    })
    .catch(error => {
        document.getElementById("system_response").innerHTML = "Error: " + error.message;
        console.error("Error:", error);
    });
};
