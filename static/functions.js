
function removeBackground(butId) {
  row = parseInt(butId.replace("but", ""))

  fetch("/remove_background/" + row).then(response => {
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