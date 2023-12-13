//Saves necessary elements to variables
const fileSelector = document.getElementById('image-select');
const output = document.getElementById('output');

//An array that tracks the upload row elements
var uploadRows = []

//The main grid
const uploadGrid = document.getElementById('upload-grid');

console.log('Videos:')
//videos = videos.filter((item, i, ar) => ar.indexOf(item) === i)
console.log(videos)

//Videos isn't read as an array,  so I've gotta turn it into an array manually
videos = videos.substring( 1, videos.length - 1 )
videos = videos.split(',')

i = 0
videos.forEach(element => {
  element = element.trim()
  element = element.substring( 1, element.length - 1 )
  createUploadRow(element, i)
  i++
});


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

function createUploadRow(fileName, rowNum){
  rowName = fileName.split('.')[0]

  console.log("row: " + rowName)
  newRow = document.createElement('div');
  newRow.setAttribute("id", "upload_row_"+rowNum);
  newRow.setAttribute("class", "row upload_row");
  uploadGrid.appendChild(newRow);
  
  upload_col_1 = document.createElement('div');
  upload_col_1.setAttribute("id", "upload_function_"+rowNum);
  upload_col_1.setAttribute("class", "col-6 upload_column name_column");

  upload_col_1.innerHTML = "<h5>"+fileName+"</h5>"

  newRow.appendChild(upload_col_1); 
  
  upload_col_2 = document.createElement('div');
  upload_col_2.setAttribute("id", "upload_test_"+rowNum);
  upload_col_2.setAttribute("class", "col-3 upload_column");
  newRow.appendChild(upload_col_2);

  test_img = document.createElement('img');
  test_img.setAttribute("id", "testImg");
  test_img.setAttribute("class", "smallImg");
  test_img.setAttribute("src", "../static/"+rowName+"/test.jpg");
  upload_col_2.appendChild(test_img);

  upload_col_3 = document.createElement('div');
  upload_col_3.setAttribute("id", "upload_result_"+rowNum);
  upload_col_3.setAttribute("class", "col-3 upload_column");
  newRow.appendChild(upload_col_3);

  result_img = document.createElement('img');
  result_img.setAttribute("id", "resultImg");
  result_img.setAttribute("class", "smallImg");
  result_img.setAttribute("src", "../static/"+rowName+"/result.jpg");
  upload_col_3.appendChild(result_img);

  uploadRows.push(newRow)

  if (rowNum > 0){
    upload_col_1.classList.add("border_top");
    upload_col_2.classList.add("border_top");
    upload_col_3.classList.add("border_top");
  }
  
}

function toggleForm() {
  if (document.getElementById("emailForm").style.display == "block")
    document.getElementById("emailForm").style.display = "none";
  else
  document.getElementById("emailForm").style.display = "block";
}
