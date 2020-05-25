try {
  var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognition = new SpeechRecognition();
}
catch(e) {
  console.error(e);
  $('.no-browser-support').show();
  $('.app').hide();
}


var noteTextarea = $('#note-textarea');
var instructions = $('#recording-instructions');
var noteContent = '';

// Get all notes from previous sessions and display them.
///////////var notes = getAllNotes();
//renderNotes(notes);

/***************
*/
window.onload = function(){
    document.getElementsByClassName("tabs")[0].click();
};


/*-----------------------------
      Voice Recognition 
------------------------------*/

// If false, the recording will stop after a few seconds of silence.
// When true, the silence period is longer (about 15 seconds),
// allowing us to keep recording even when the user pauses. 
recognition.continuous = true;

// This block is called every time the Speech APi captures a line. 
recognition.onresult = function(event) {

  // event is a SpeechRecognitionEvent object.
  // It holds all the lines we have captured so far. 
  // We only need the current one.
  var current = event.resultIndex;

  // Get a transcript of what was said.
  var transcript = event.results[current][0].transcript;

  // Add the current transcript to the contents of our Note.
  // There is a weird bug on mobile, where everything is repeated twice.
  // There is no official solution so far so we have to handle an edge case.
  var mobileRepeatBug = (current == 1 && transcript == event.results[0][0].transcript);

  if(!mobileRepeatBug) {
    noteContent += transcript;
    noteTextarea.val(noteContent);
  }
};

recognition.onstart = function() { 
  instructions.text('Voice recognition activated. Try speaking into the microphone.');
}

recognition.onspeechend = function() {
  instructions.text('You were quiet for a while so voice recognition turned itself off.');
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    instructions.text('No speech was detected. Try again.');  
  };
}



/*-----------------------------
      App buttons and input 
------------------------------*/

$('#start-record-btn').on('click', function(e) {
  if (noteContent.length) {
    noteContent += ' ';
  }
  recognition.start();
});


$('#pause-record-btn').on('click', function(e) {
  recognition.stop();
  instructions.text('Voice recognition paused.');
});

// Sync the text inside the text area with the noteContent variable.
noteTextarea.on('input', function() {
  noteContent = $(this).val();
})

$('#save-note-btn').on('click', function(e) {
  recognition.stop();

  if(!noteContent.length) {
    instructions.text('Could not save empty note. Please add a message to your note.');
  }

  else if(document.getElementById("course").value=='') {
    instructions.text('Please enter course title');
  }

  else {
    // Save note to localStorage.
    // The key is the dateTime with seconds, the value is the content of the note.
    //saveNote(new Date().toLocaleString(), noteContent);
    saveNote(noteContent);

    // Reset variables and update UI.
    noteContent = '';
    //renderNotes(getAllNotes());
    noteTextarea.val('');
    instructions.text('Note saved successfully.');
    console.log("115: courseCode", localStorage.getItem("course"))
  }
      
})



/*-----------------------------
      Speech Synthesis 
------------------------------*/

function readOutLoud(message) {
	var speech = new SpeechSynthesisUtterance();

  // Set the text and voice attributes.
	speech.text = message;
	speech.volume = 1;
	speech.rate = 1;
	speech.pitch = 1;
  
	window.speechSynthesis.speak(speech);
}



function saveNote(content) {
  //localStorage.setItem('note-' + dateTime, content);
  courseTitle=document.getElementById("course").value;
  var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
      if(this.readyState == 4 && this.status == 200) {
        var resp = JSON.parse(xhr.responseText);
        if(resp.success) {
          console.log("successfull111")
        }
        else {
          console.log("ERRRORRR")
        }
      }
    }


  xhr.open("POST", "/put_message", true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.send(JSON.stringify({'message' : content,
                           'course' : courseTitle})); 
  }


function deleteNote( noteId) {
  var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
      if(this.readyState == 4 && this.status == 200) {
        var resp = JSON.parse(xhr.responseText);
        if(resp.success) {
          console.log("successfull111")
          all_messages()
        }
        else {
          console.log("ERRRORRR")
        }
      }
    }


  xhr.open("POST", "/delete_message", true);
  xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
  xhr.send(JSON.stringify({'id' : noteId})); 

}


////////////////////////////////////////////////////////////
///
///

//////////////////////////////////
function all_messages(){
  course = document.getElementById("courseSearch").value;
  fromDate = document.getElementById("fromDate").value;
  toDate = document.getElementById("toDate").value;
  word = document.getElementById("wordSearch").value;
  var xhr = new XMLHttpRequest();
  var content =[];
   xhr.onreadystatechange = function(){
      if(this.readyState == 4 && this.status == 200) {
        var resp = JSON.parse(xhr.responseText);
        if(resp.success) {
          var text = "";
          var size = resp.messages.length;
            for(var i = size - 1; 0 <= i; i--){
              text +=course+ ": " + resp.dates[i] + ": " + resp.messages[i] + "\n";
              content.push({
                date: resp.dates[i],
                message: resp.messages[i],
                course: resp.course[i],
                id: resp.id[i]
              })
              //console.log(resp.id[i]);
            }
          renderCourse(content);
        }
        //if not resp.success
        else {
          document.getElementById("search-div").innerHTML = resp.message;
        }
      }
    }
    xhr.open("GET", "/search_all", true);
    xhr.setRequestHeader('from', fromDate);
    xhr.setRequestHeader('to', toDate);
    xhr.setRequestHeader('course', course);
    xhr.setRequestHeader('word', word);
    xhr.send();

}

openTab = function(evt, tabName){
    var tabcontent = document.getElementsByClassName("container");
    for(var i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    var tabs = document.getElementsByClassName("tabs");
    for(var i = 0; i < tabs.length; i++) {
      tabs[i].className = tabs[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  }

function renderCourse(notes) {
  var html = '';
  if(notes.length) {
    notes.forEach(function(notes) {
      var note = notes.message;
      html+= `<p class="header">
          <span class="date">(${notes.course}) ${notes.date}</span>
          <button id="listen-to-note" title="read note" style="background-color: #1ABC9C;" onclick="readOutLoud('${note}')">Read note</button>
          <button id="delete-by-id" title="delete note" style="background-color: #1ABC9C;" onclick="deleteNote(${notes.id})">delete</button>
        </p>
        <p class="content"> ${notes.message}</p>`; 
    });
  }
  else {
    html = '<li><p class="content">You don\'t have any notes yet.</p></li>';
  }
  document.getElementById("search-div").innerHTML = html;
}