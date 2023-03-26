const apiUrl = "http://localhost:5000"; // ganti dengan URL aplikasi Flask Anda

function addCertificate() {
  // ambil data dari form
  const form = document.getElementById("certificate-form");
  const formData = new FormData(form);

  // konversi gambar menjadi base64
  const reader = new FileReader();
  const imageFile = formData.get("image");
  reader.readAsDataURL(imageFile);
  reader.onload = function () {
    // kirim data ke API Flask
    const certData = {
      name: formData.get("name"),
      date: formData.get("date"),
      image: reader.result.split(",")[1],
    };
    fetch(`${apiUrl}/add_cert`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(certData),
    })
      .then((response) => response.json())
      .then((data) => {
        // tampilkan pesan sukses dan proof of work
        const message = data.message;
        const proof = data.proof;
        alert(`${message}\nProof of work: ${proof}`);
      });
  };
}

function viewCertificates() {
  // ambil data dari API Flask
  fetch(`${apiUrl}/view_certificates`)
    .then((response) => response.json())
    .then((data) => {
      // tampilkan data pada halaman HTML
      const certificates = data;
      const container = document.getElementById("certificate-container");
      container.innerHTML = "";
      certificates.forEach((cert) => {
        const certHtml = `
          <div>
            <img src="${cert.image}">
            <h3>${cert.name}</h3>
            <p>${cert.date}</p>
            <p>Proof of work: ${cert.proof}</p>
          </div>
        `;
        container.innerHTML += certHtml;
      });
    });
}
