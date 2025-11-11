// Main application logic

// Tab switching
document.querySelectorAll('.tabs .tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // atualizar tab buttons
    document.querySelectorAll('.tabs .tab').forEach(t => {
        t.classList.remove('active');
    });
    document.querySelector(`.tabs .tab[data-tab="${tabName}"]`).classList.add('active');

    // atualizar tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');

    // carrgar tab data
    loadTabData(tabName);
}

function loadTabData(tabName) {
    switch(tabName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'books':
            loadBooks();
            break;
        case 'members':
            loadMembers();
            break;
        case 'loans':
            loadLoans();
            break;
    }
}

// inicializar app
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});
