//Saves necessary elements to variables
const fileSelector = document.getElementById('image-select');
const output = document.getElementById('output');

//An array that tracks the upload row elements
var uploadRows = []
var alertedList = []

//The main grid
const uploadGrid = document.getElementById('upload-grid');

//Videos isn't read as an array,  so I've gotta turn it into an array manually
videos = videos.substring( 1, videos.length - 1 )
videos = videos.split(',')

i = 0
if (videos.length > 1 || (videos.length == 1 && videos[0] != "")){
videos.forEach(element => {
  element = element.trim()
  element = element.substring( 1, element.length - 1 )
  createUploadRow(element, i)
  i++
});
}

//Set up notifications
Notification.requestPermission().then(function (permission) {    console.log(permission);});
let permission = Notification.permission;

//Checks through each of the videos/streams to see if any fires are detected, and refreshes the images in the meantime.

function refreshImages(){

  i = 0
  videos.forEach(element => {
    element = element.trim()
    element = element.substring( 1, element.length - 1 )
    rowName = element.split('.')[0]

    if (new File("../static/"+rowName+"/test.jpg").exists){
      document.getElementById("testImg"+i).src = ""
      document.getElementById("testImg"+i).src = "../static/"+rowName+"/test.jpg?random="+new Date().getTime();
    }
    if (new File("../static/"+rowName+"/result.jpg").exists){
      document.getElementById("resultImg"+i).src = ""
      document.getElementById("resultImg"+i).src = "../static/"+rowName+"/result.jpg?random="+new Date().getTime();
    }
    
    console.log("alerted")
    console.log(videos)

    //if(!alertedList.includes(i)){
      url = "../static/"+rowName+"/result.txt"

      fetch(url)
        .then( r => r.text() )
        .then( t => checkResults(t, rowName, i))
      //}
    i++
  });

  setTimeout(refreshImages, 30000);
}

refreshImages();

function checkResults(result, rowName, index){

  if (result > 0){
    //Generate Date String
    const now1 = new Date();
    const now = now1.toLocaleString();
    console.log("b")
    if(permission === "granted") {   
      showNotification(now, rowName);
    } else if(permission === "default"){   
      requestAndShowPermission(now, rowName);
    } else {  
      alert("Fire detected at " + now);
    }

    alertedList.push(index)
    document.getElementById("upload_function_"+index).style.color("red")
  }
}

function requestAndShowPermission(now, rowName) {
  Notification.requestPermission(function (permission) {
     if (permission === "granted") {
           showNotification(now, rowName);
     }
     console.log("c")
  });
}

function showNotification(now, rowName) {
  console.log("d")
  if(document.visibilityState === "visible") {
    alert(rowName+"\n Fire detected at " + now);
  }   
  var title = "Fire Detected";   
  var body = "Fire detected at " + now;   
  var notification = new Notification(rowName, { body });   notification.onclick = () => { 
    notification.close();
    window.parent.focus();
  }
}

//This will catch when files are selected and save them into a list.
// File selector doesn't currently support multiple files, but I may need it in the future. 
/*fileSelector.addEventListener('change', (event) => {
  const fileList = event.target.files;
  console.log(fileList);
  readImage(fileList[0])
});*/

//The actual function for reading the image
function readImage(file) {
  // Check if the file is an image.
  if (file.type && !file.type.startsWith('image/')) {
    console.log('File is not an image.', file.type, file);
    return;
  }


  /*
  //Creates a file reader, and once the file reader has loaded, logs the file address
  const reader = new FileReader();
  reader.addEventListener('load', (event) => {
    console.log(event.target.result);
    //Replaces the output element's source with the uploaded file address to confirm the upload was successful
    output.src = event.target.result;
  });
  reader.readAsDataURL(file);*/
}


function createUploadRow(fileName, rowNum){
  rowName = fileName.split('.')[0]

  //console.log("row: " + rowName)
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
  test_img.setAttribute("id", "testImg"+rowNum);
  test_img.setAttribute("class", "smallImg");
  test_img.setAttribute("onerror", "this.onerror=null; this.src='../static/default.jpg'")
  test_img.setAttribute("src", "../static/"+rowName+"/test.jpg");
  upload_col_2.appendChild(test_img);

  upload_col_3 = document.createElement('div');
  upload_col_3.setAttribute("id", "upload_result_"+rowNum);
  upload_col_3.setAttribute("class", "col-3 upload_column");
  newRow.appendChild(upload_col_3);

  result_img = document.createElement('img');
  result_img.setAttribute("id", "resultImg"+rowNum);
  result_img.setAttribute("class", "smallImg");
  result_img.setAttribute("onerror", "this.onerror=null; this.src='../static/default.jpg'")
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
