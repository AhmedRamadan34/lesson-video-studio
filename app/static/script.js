// ==========================
// Selected Files
// ==========================

let imageFiles = [];

let audioFiles = [];

const imageInput = document.getElementById("images");
const audioInput = document.getElementById("audios");

const imageDrop = document.getElementById("imageDrop");
const audioDrop = document.getElementById("audioDrop");

const lessonFiles = document.getElementById("lessonFiles");

const uploadForm = document.getElementById("uploadForm");

const progressBar = document.getElementById("progressBar");
const status = document.getElementById("status");

const preview = document.getElementById("preview");
const downloadBtn = document.getElementById("downloadBtn");

/* ===========================
   Drag & Drop
=========================== */

function setupDrop(dropZone, input){

    dropZone.addEventListener("click",()=>{

        input.click();

    });

    dropZone.addEventListener("dragover",(e)=>{

        e.preventDefault();

        dropZone.classList.add("dragover");

    });

    dropZone.addEventListener("dragleave",()=>{

        dropZone.classList.remove("dragover");

    });

    dropZone.addEventListener("drop",(e)=>{

        e.preventDefault();

        dropZone.classList.remove("dragover");

        for (const file of e.dataTransfer.files) {

            const list = input === imageInput
                ? imageFiles
                : audioFiles;

            const exists = list.some(
                f => f.name.toLowerCase() === file.name.toLowerCase()
            );

            if (!exists) {

                list.push(file);

            }

        }

        refreshUI();

    });

}

setupDrop(imageDrop,imageInput);
setupDrop(audioDrop,audioInput);


/* ===========================
   File Selection
=========================== */

imageInput.addEventListener("change", () => {

    [...imageInput.files].forEach(file => {

        const exists = imageFiles.some(
            f => f.name.toLowerCase() === file.name.toLowerCase()
        );

        if (!exists) {
            imageFiles.push(file);
        }

    });

    imageInput.value = "";

    refreshUI();

});


audioInput.addEventListener("change", () => {

    [...audioInput.files].forEach(file => {

        const exists = audioFiles.some(
            f => f.name.toLowerCase() === file.name.toLowerCase()
        );

        if (!exists) {
            audioFiles.push(file);
        }

    });

    audioInput.value = "";

    refreshUI();

});


/* ===========================
   Refresh UI
=========================== */

function refreshUI(){

    lessonFiles.innerHTML="";

    const images = imageFiles;
    const audios = audioFiles;

    const imageMap={};
    const audioMap={};

    images.forEach(file=>{

        imageMap[
            file.name.replace(/\.[^/.]+$/,"").toLowerCase()
        ]=file;

    });

    audios.forEach(file=>{

        audioMap[
            file.name.replace(/\.[^/.]+$/,"").toLowerCase()
        ]=file;

    });

    const names=new Set([

        ...Object.keys(imageMap),

        ...Object.keys(audioMap)

    ]);

    if(names.size===0){

        lessonFiles.innerHTML=`

        <div class="lesson-empty">

            No files selected yet.

        </div>

        `;

        return;

    }

    [...names]

        .sort()

        .forEach(name=>{

            const image=imageMap[name];

            const audio=audioMap[name];

            if(image && audio){

                lessonFiles.innerHTML+=`

                <div class="lesson-row ready">

                    <div>

                        🖼 ${image.name}

                    </div>

                    <div>

                        🎵 ${audio.name}

                    </div>

                    <div class="status-ready">

                        ✅ Ready

                    </div>

                    <div>

                        <button
                            type="button"
                            class="delete-btn"
                            onclick="removeLesson('${name}')">

                            🗑

                        </button>

                    </div>

                </div>

                `;

            }

            else if(image){

                lessonFiles.innerHTML+=`

                <div class="lesson-row error">

                    <div>

                        🖼 ${image.name}

                    </div>

                    <div>-</div>

                    <div class="status-error">

                        ❌ Missing Audio

                    </div>

                    <div>

                        <button
                            type="button"
                            class="delete-btn"
                            onclick="removeLesson('${name}')">

                            🗑

                        </button>

                    </div>

                </div>

                `;

            }

            else{

                lessonFiles.innerHTML+=`

                <div class="lesson-row error">

                    <div>-</div>

                    <div>

                        🎵 ${audio.name}

                    </div>

                    <div class="status-error">

                        ❌ Missing Image

                    </div>

                    <div>

                        <button
                            type="button"
                            class="delete-btn"
                            onclick="removeLesson('${name}')">

                            🗑

                        </button>

                    </div>

                </div>

                `;

            }

        });

}


/* ===========================
   Upload
=========================== */

uploadForm.addEventListener("submit",async(e)=>{

    e.preventDefault();

    const formData=new FormData();

    imageFiles.forEach(file=>{

        formData.append("images",file);

    });

    audioFiles.forEach(file=>{

        formData.append("audios",file);

    });

    progressBar.style.width="15%";

    status.innerHTML="Uploading files...";

    const response=await fetch("/upload",{

        method:"POST",

        body:formData

    });

    progressBar.style.width="70%";

    const result=await response.json();

    progressBar.style.width="100%";

    status.innerHTML=result.message;

    if(result.video){

        preview.style.display="block";

        preview.src=result.video+"?t="+Date.now();

        preview.load();

        downloadBtn.style.display="inline-block";

        downloadBtn.href=result.video;

        // Reset selected files

        imageFiles = [];

        audioFiles = [];

        refreshUI();

    }

});

function removeLesson(name){

    imageFiles = imageFiles.filter(file =>

        file.name
            .replace(/\.[^/.]+$/, "")
            .toLowerCase() !== name

    );

    audioFiles = audioFiles.filter(file =>

        file.name
            .replace(/\.[^/.]+$/, "")
            .toLowerCase() !== name

    );

    refreshUI();

}