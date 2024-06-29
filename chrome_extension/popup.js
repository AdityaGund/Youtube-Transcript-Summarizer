document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('summarizeButton').addEventListener('click',async () => 
    {
        const languagecode=document.getElementById('languageselect').value;
        const youtubeUrl = document.getElementById('videoUrl').value;
        const apiurl=`http://localhost:5000/api/summarize?youtube_url=${youtubeUrl}&language_code=${languagecode}`
        try{
            console.log("inside try");
            const reponse=await fetch(apiurl)
            const data=await reponse.json();

            document.getElementById('summary').innerText=data.summary;
        }catch(error){
            console.log("direcly error");
            console.error("Error: ",error)
        }
    });
});
