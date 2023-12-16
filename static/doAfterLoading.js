Dropzone.options.myDropzone = {
    init: function () {
      this.on("queuecomplete", file => {
        location.reload();
      })
    }
  };


enableAlphaMatting(false)