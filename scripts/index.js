//Saves necessary elements to variables
const fileSelector = document.getElementById('image-select');
const output = document.getElementById('output');

//Sets the output element to have an empty source by default.
output.src = '';


//This will catch when files are selected and save them into a list.
// File selector doesn't currently support multiple files, but I may need it in the future. 
fileSelector.addEventListener('change', (event) => {
  const fileList = event.target.files;
  console.log(fileList);
  readImage(fileList[0])
});

//The actual function for reading the image
function readImage(file) {
  // Check if the file is an image.
  if (file.type && !file.type.startsWith('image/')) {
    console.log('File is not an image.', file.type, file);
    return;
  }

  //Creates a file reader, and once the file reader has loaded, logs the file address
  const reader = new FileReader();
  reader.addEventListener('load', (event) => {
    console.log(event.target.result);
    //Replaces the output element's source with the uploaded file address to confirm the upload was successful
    output.src = event.target.result;
  });
  reader.readAsDataURL(file);
}
