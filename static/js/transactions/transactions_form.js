document.addEventListener('DOMContentLoaded', function() {
  const categoriesByType = JSON.parse(document.getElementById('categories-by-type').textContent);
  const typeSelect = document.getElementById('type');
  const categorySelect = document.getElementById('category');
  const descField = document.getElementById('field-description');
  const amountField = document.getElementById('field-amount');
  const categoryField = document.getElementById('display-category');
  const accountField = document.getElementById('field-account');
  const toAccountField = document.getElementById('display-to-account');

  function updateCategories() {
    const selectedType = typeSelect.value;
    const categories = categoriesByType[selectedType] || [];
    categorySelect.innerHTML = '';
    // Add empty option
    const emptyOption = document.createElement('option');
    emptyOption.value = '';
    emptyOption.textContent = 'Select one';
    categorySelect.appendChild(emptyOption);
    categories.forEach(function(item) {
      var value = item[0];
      var label = item[1];
      var option = document.createElement('option');
      option.value = value;
      option.textContent = label;
      categorySelect.appendChild(option);
    });
  }

  function updateFields() {
    const selectedType = typeSelect.value;
    descField.style.display = 'none';
    amountField.style.display = 'none';
    categoryField.style.display = 'none';
    accountField.style.display = 'none';
    toAccountField.style.display = 'none';
    if (selectedType === 'income' || selectedType === 'expense') {
      descField.style.display = '';
      amountField.style.display = '';
      categoryField.style.display = '';
      categorySelect.required = true;
      accountField.style.display = '';
    } else if (selectedType === 'transfer') {
      descField.style.display = '';
      amountField.style.display = '';
      accountField.style.display = '';
      toAccountField.style.display = '';
      categoryField.style.display = 'none';
      categorySelect.required = false;
    }
  }

  typeSelect.addEventListener('change', function() {
    updateCategories();
    updateFields();
  });
  updateCategories();
  updateFields();
});
