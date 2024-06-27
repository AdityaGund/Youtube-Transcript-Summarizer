
document.getElementById('summarizeButton').addEventListener('click',async()=>{
    const videoUrl=document.getElementById("vidoUrl").value;
    const response=await fetch(`http://localhost:5000/api/summarize?youtube_url=${videoUrl}`);
    const data=await response.json()
    document.getElementById('summary').innerText=data.summary;
});