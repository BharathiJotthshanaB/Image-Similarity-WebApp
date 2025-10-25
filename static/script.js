document.querySelectorAll('.drop-zone input').forEach(inputElement => {
  const dropZone = inputElement.closest('.drop-zone');
  const previewImg = dropZone.querySelector('img');

  inputElement.addEventListener('change', e => {
    if (inputElement.files.length) {
      const file = inputElement.files[0];
      previewImg.src = URL.createObjectURL(file);
      previewImg.style.display = 'block';
    }
  });
});

const slider = document.getElementById('slider');
if (slider) {
  slider.addEventListener('input', e => {
    document.getElementById('img-overlay').style.width = e.target.value + "%";
  });
}
