
async function removeBackground(butId) {
  row = parseInt(butId.replace("but", ""))

  await fetch("/remove_background/" + row).then(response => {
    return response.json()
  }).then(data => {
    document.getElementById("edited_img" + row).src = "data:image/png;base64, " + data["content"]
    document.getElementById("a" + row).download = data["filename"]
    document.getElementById("a" + row).href = "data:image/png;base64, " + data["content"]
  })
}

function deleteRow(deleteNum, deletePath) {
  document.getElementById("tr" + deleteNum).remove()

  fetch("/delete_image", {
    method: "POST",
    body: JSON.stringify({
      path: deletePath
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8"
    }
  });
}


async function removeMultipleBackgrounds() {
  checked_checkboxes = document.querySelectorAll(".checkbox:checked");
  for (let i = 0; i < checked_checkboxes.length; i++) {
    row = parseInt(checked_checkboxes[i].id.replace("checkbox", ""));
    await removeBackground("but" + row);
    console.log("done image " + row);
  }
  alert("Finished removing background for all selected images");
}

async function downloadMultiple() {
  checked_checkboxes = document.querySelectorAll(".checkbox:checked");
  for (let i = 0; i < checked_checkboxes.length; i++) {
    row = parseInt(checked_checkboxes[i].id.replace("checkbox", ""));
    document.getElementById("a" + row).click();
  }
  alert("Finished downloading all selected images");
}

function setAllCheckboxes(value){
  checkboxes = document.querySelectorAll(".checkbox");
  console.log("Setting all checkboxes to " + value);
  for (let i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = value;
  }
}