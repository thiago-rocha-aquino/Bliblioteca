// funções utilitárias gerais

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}

function openModal() {
    document.getElementById('modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('modal-body').innerHTML = '';
}

// fecha o modal ao clicar fora dele
window.onclick = function(event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        closeModal();
    }
};

function createTableRow(cells, actions = []) {
    const tr = document.createElement('tr');

    cells.forEach(cell => {
        const td = document.createElement('td');
        if (typeof cell === 'string') {
            td.textContent = cell;
        } else if (cell instanceof Node) {
            // Se for um elemento DOM válido
            td.appendChild(cell);
        } else {
            // Converte qualquer outro tipo para string
            td.textContent = String(cell);
        }
        tr.appendChild(td);
    });

    // Célula de ações
    const actionsCell = document.createElement('td');
    actionsCell.style.display = 'flex';
    actionsCell.style.gap = '0.5rem';

    actions.forEach(action => {
        const btn = document.createElement('button');
        btn.className = `btn btn-sm ${action.className || ''}`;
        btn.textContent = action.text;
        btn.onclick = action.onClick;
        actionsCell.appendChild(btn);
    });

    tr.appendChild(actionsCell);

    return tr;
}

function createBadge(text, type = 'success') {
    const badge = document.createElement('span');
    badge.className = `badge badge-${type}`;
    badge.textContent = text;
    return badge;
}
