function selectAmount(amount) {
    document.querySelectorAll('.container').forEach(card => {
        card.classList.remove('selected');
    });
    const clickedCard = event.currentTarget;
    if (clickedCard) {
        clickedCard.classList.add('selected');
    }
    const customAmountInput = document.getElementById('customAmount');
    if (customAmountInput) {
        customAmountInput.value = amount;
        updateImpactPreview(amount);
    }
}

function updateImpactPreview(amount) {
    const preview = document.getElementById('impactPreview');
    const impactText = document.getElementById('impactText');
    if (!preview || !impactText) return;

    if (amount < 50) {
        preview.classList.remove('visible');
        return;
    }

    let impact = '';
    const programs = [
        {
            name: "Seniors Living at Home",
            items: [
                { name: "Essential food commodities", cost: 1500, unit: "month" },
                { name: "Essential hygiene items", cost: 300, unit: "month" },
                { name: "Social outings and lunches", cost: 400, unit: "month" },
                { name: "Necessary healthcare support", cost: 2000, unit: "year" },
                { name: "Necessary clothing", cost: 4000, unit: "year" }
            ]
        },
        {
            name: "Seniors in Care Center",
            items: [
                { name: "Nutritious meals three times a day", cost: 5000, unit: "month" },
                { name: "Hygiene supplies", cost: 1500, unit: "month" },
                { name: "Essential healthcare support", cost: 2500, unit: "year" },
                { name: "Essential clothing", cost: 4000, unit: "year" }
            ]
        },
        {
            name: "Education Support",
            items: [
                { name: "School supplies", cost: 2000, unit: "year" },
                { name: "Private college", cost: 2000, unit: "year" },
                { name: "Essential hygiene items", cost: 200, unit: "month" },
                { name: "School fees", cost: 3000, unit: "year" },
                { name: "Uniforms", cost: 7500, unit: "year" }
            ]
        }
    ];

    let maxCount = 0;
    let bestItems = [];
    programs.forEach(program => {
        let totalCount = 0;
        let programItems = [];
        program.items.forEach(item => {
            const count = Math.floor(amount / item.cost);
            if (count > 0) {
                totalCount += count;
                programItems.push({
                    name: item.name,
                    count: count,
                    unit: item.unit
                });
            }
        });
        if (totalCount > maxCount && programItems.length > 0) {
            maxCount = totalCount;
            bestItems = programItems;
        }
    });

    if (bestItems.length > 0) {
        impact = `Your donation of ${amount} ETB will support:`;
        impact += `<ul class="impact-list">`;
        bestItems.forEach(item => {
            impact += `<li><i class="fas fa-check-circle"></i> ${item.name} for ${item.count} seniors for ${item.count} ${item.unit}${item.count > 1 ? 's' : ''}</li>`;
        });
        impact += `</ul>`;
    } else {
        impact = `Your donation of ${amount} ETB will help our organization provide essential services for seniors and education for children.`;
    }

    impactText.innerHTML = impact;
    preview.classList.add('visible');
}

document.addEventListener('DOMContentLoaded', () => {
    const donationForm = document.getElementById('donationForm');
    if (donationForm) {
        donationForm.addEventListener('submit', function (event) {
            const email = document.querySelector('input[name="email"]').value;
            const phone = document.querySelector('input[name="phone_number"]').value;
            const amount = document.querySelector('input[name="amount"]').value;

            if (!email.includes('@') || !email.includes('.')) {
                event.preventDefault();
                alert('Please enter a valid email address.');
                return;
            }

            if (phone && (!phone.startsWith('09') && !phone.startsWith('07') || phone.length !== 10)) {
                event.preventDefault();
                alert('Phone number must be 10 digits starting with 09 or 07.');
                return;
            }

            if (amount < 50) {
                event.preventDefault();
                alert('Minimum donation amount is 50 ETB.');
                return;
            }

            // Show loading spinner
            const loadingOverlay = document.getElementById('loadingOverlay');
            if (loadingOverlay) {
                loadingOverlay.classList.add('active');
            }
        });
    }

    // Attach input event to amount field if it exists
    const customAmountInput = document.getElementById('customAmount');
    if (customAmountInput) {
        customAmountInput.addEventListener('input', function () {
            updateImpactPreview(this.value);
        });
    }
});
