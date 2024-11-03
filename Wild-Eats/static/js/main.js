document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recipeForm');
    const ingredientInput = document.getElementById('ingredientInput');
    const addButton = document.getElementById('addIngredient');
    const ingredientsList = document.getElementById('ingredientsList');
    const generateButton = document.getElementById('generateButton');
    
    // Only proceed if we're on the input page with the form
    if (form && ingredientInput && addButton && ingredientsList && generateButton) {
        const ingredients = new Set();

        function addIngredient(ingredient) {
            if (ingredient && !ingredients.has(ingredient)) {
                ingredients.add(ingredient);
                
                const pill = document.createElement('div');
                pill.className = 'badge bg-secondary p-2 d-flex align-items-center';
                
                const text = document.createElement('span');
                text.textContent = ingredient;
                
                const removeBtn = document.createElement('button');
                removeBtn.className = 'btn-close ms-2';
                removeBtn.setAttribute('aria-label', 'Remove');
                
                removeBtn.addEventListener('click', () => {
                    ingredients.delete(ingredient);
                    pill.remove();
                    updateGenerateButton();
                });
                
                pill.appendChild(text);
                pill.appendChild(removeBtn);
                ingredientsList.appendChild(pill);
                
                // Add hidden input for form submission
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'ingredients[]';
                hiddenInput.value = ingredient;
                pill.appendChild(hiddenInput);
                
                updateGenerateButton();
            }
        }

        function updateGenerateButton() {
            generateButton.disabled = ingredients.size === 0;
        }

        addButton.addEventListener('click', () => {
            const ingredient = ingredientInput.value.trim();
            if (ingredient) {
                addIngredient(ingredient);
                ingredientInput.value = '';
            }
        });

        ingredientInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addButton.click();
            }
        });

        form.addEventListener('submit', (e) => {
            if (ingredients.size === 0) {
                e.preventDefault();
                alert('Please add at least one ingredient');
            }
        });
    }
});
