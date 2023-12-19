async function removeBackground(butId) {
  row = parseInt(butId.replace("but", ""))
  deleteFilename = document.getElementById("filename" + row).textContent

  await fetch("/remove_background", {
    method: "POST",
    body: JSON.stringify({
      "filename": deleteFilename,
      "enable_alpha_matting": document.getElementById("enableAlphaMatting").checked,
      "alpha_matting_foreground_threshold": parseInt(document.getElementById("alphaMattingForegroundThreshold").value),
      "alpha_matting_background_threshold": parseInt(document.getElementById("alphaMattingBackgroundThreshold").value),
      "alpha_matting_erode": parseInt(document.getElementById("alphaMattingErode").value),
      "model": document.getElementById("selectModel").value
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  }).then(response => {
    return response.json()
  }).then(data => {
    document.getElementById("edited_img" + row).src = "data:image/png;base64, " + data["content"]
    document.getElementById("a" + row).download = data["filename"]
    document.getElementById("a" + row).href = "data:image/png;base64, " + data["content"]
  })
};

function deleteRow(deleteNum) {
  deleteFilename = document.getElementById("filename" + row).textContent
  document.getElementById("tr" + deleteNum).remove()

  fetch("/delete_image", {
    method: "POST",
    body: JSON.stringify({
      path: deleteFilename
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  });
}

async function deleteMultiple() {
  checked_checkboxes = document.querySelectorAll(".checkbox.row:checked");

  for (let i = 0; i < checked_checkboxes.length; i++) {
    row = parseInt(checked_checkboxes[i].id.replace("checkbox", ""));
    document.getElementById("delete" + row).click();
  }
}


async function removeMultipleBackgrounds() {
  checked_checkboxes = document.querySelectorAll(".checkbox.row:checked");

  for (let i = 0; i < checked_checkboxes.length; i++) {
    row = parseInt(checked_checkboxes[i].id.replace("checkbox", ""));
    await removeBackground("but" + row);
    console.log("done image " + row);
  }
  alert("Finished removing background for all selected images");
}

async function downloadMultiple() {
  checked_checkboxes = document.querySelectorAll(".checkbox.row:checked");
  for (let i = 0; i < checked_checkboxes.length; i++) {
    row = parseInt(checked_checkboxes[i].id.replace("checkbox", ""));
    document.getElementById("a" + row).click();
  }
  alert("Finished downloading all selected images");
}

function setAllRowCheckboxes(value) {
  checkboxes = document.querySelectorAll(".checkbox.row");
  console.log("Setting all checkboxes to " + value);
  for (let i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = value;
  }
  onCheckboxChange()
}

function onCheckboxChange() {
  checked_checkboxes = document.querySelectorAll(".checkbox.row:checked");
  document.getElementById("label_num_selected").textContent = checked_checkboxes.length + " Images selected"
}

function updateForegroundThreshold(val) {
  document.getElementById('alphaMattingForegroundThresholdValue').textContent = val;
}
function updateBackgroundThreshold(val) {
  document.getElementById('alphaMattingBackgroundThresholdValue').textContent = val;
}
function updateErode(val) {
  document.getElementById('alphaMattingErodeValue').textContent = val;
}

function enableAlphaMatting(val) {
  if (val) {
    document.getElementById('settingAlphaMattingForeground').classList.remove("hidden");
    document.getElementById('settingAlphaMattingBackground').classList.remove("hidden");
    document.getElementById('settingAlphaMattingErode').classList.remove("hidden");
  } else {
    document.getElementById('settingAlphaMattingForeground').classList.add("hidden");
    document.getElementById('settingAlphaMattingBackground').classList.add("hidden");
    document.getElementById('settingAlphaMattingErode').classList.add("hidden");
  }

}