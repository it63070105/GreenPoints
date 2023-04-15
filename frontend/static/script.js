new Vue({
  el: "#app",
  data: {
    selectedImage: "",
    loaderVisible: false,
    processBtnDisabled: false,
    processBtnText: "Process Images",
    result: [],
    remainingTime: 30,
    timerId: null,
  },
  methods: {
    clearOutputList() {
      const outputList = document.getElementById('output-list');
      outputList.innerHTML = ''; // clear the output list
    },
    displayImage(event) {
      const selectedFile = event.target.files[0];
      const reader = new FileReader();

      reader.onload = (event) => {
        const imageSrc = event.target.result;
        const imageElement = document.getElementById("selected-image");
        imageElement.setAttribute("src", imageSrc);
        imageElement.style.display = "block";
      };

      reader.readAsDataURL(selectedFile);
      this.clearOutputList(); // call the clearOutputList method here
    },
    async submitForm(event) {
      event.preventDefault();
      const form = event.target;
      const formData = new FormData(form);

      this.loaderVisible = true;
      this.processBtnDisabled = true;
      this.processBtnText = "Processing...";

      try {
        const response = await fetch(form.action, {
          method: form.method,
          body: formData,
        });
        const data = await response.json();
        this.result = data.map((item) => {
          return {
            ...item,
            output_image: "data:image/png;base64, " + item.output_image,
            qrcode: "data:qrcode/png;base64, " + item.qrcode,
          };
        });
      } catch (error) {
        console.log(error);
      }

      this.loaderVisible = false;
      this.processBtnDisabled = false;
      this.processBtnText = "Process Images";
    },
    closeModal() {
      clearInterval(this.timerId);
      document.getElementById('myModal').classList.remove('is-active');
    },
  },
  mounted() {

    this.timerId = setInterval(() => {
      document.getElementById('timeout').innerHTML = this.remainingTime;
      if (this.remainingTime <= 0) {
        clearInterval(this.timerId);
        this.closeModal();
      } else {
        this.remainingTime--;
      }
    }, 1000);
  },
  beforeDestroy() {
    clearInterval(this.timerId);
  },
});

