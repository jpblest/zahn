const socket = io();

let mediaRecorder;
let audioChunks = [];

document.getElementById('startRecord').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    document.getElementById('startRecord').disabled = true;
    document.getElementById('stopRecord').disabled = false;
});

document.getElementById('stopRecord').addEventListener('click', () => {
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

        // Create a FormData object to send the file to the server
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');

        // Send the audio file to the server
        fetch('/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Display the transcription
            document.getElementById('transcription').innerText = data.text;

            // Optionally display the filename or provide a download link
            const downloadLink = document.getElementById('downloadLink');
            downloadLink.href = `/static/recordings/${data.filename}`;
            downloadLink.download = data.filename;
            downloadLink.style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
        });

        document.getElementById('startRecord').disabled = false;
        document.getElementById('stopRecord').disabled = true;
    };
});
