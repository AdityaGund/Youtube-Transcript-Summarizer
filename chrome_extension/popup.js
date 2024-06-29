document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('summarizeButton').addEventListener('click', () => {
        console.log("clicked!!!");
        const youtubeUrl = document.getElementById('videoUrl').value;
        fetch(`http://localhost:5000/api/summarize?youtube_url=${youtubeUrl}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('summary').innerText = data.summary;
            })
            .catch(error => console.error('Error:', error));
    });
});
