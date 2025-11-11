// Loans 

let currentFilter = 'all';

async function loadLoans() {
    await filterLoans(currentFilter);
}

async function filterLoans(filter) {
    currentFilter = filter;

    try {
        let response;
        switch(filter) {
            case 'active':
                response = await api.getActiveLoans();
                break;
            case 'overdue':
                response = await api.getOverdueLoans();
                break;
            default:
                response = await api.getLoans();
        }

        displayLoans(response.data);
    } catch (error) {
        showToast('Erro ao carregar empréstimos', 'error');
    }
}

function displayLoans(loans) {
    const container = document.getElementById('loans-list');

    if (!loans || loans.length === 0) {
        container.innerHTML = '<p class="loading">Nenhum empréstimo encontrado</p>';
        return;
    }

    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Livro</th>
                <th>Membro</th>
                <th>Empréstimo</th>
                <th>Devolução</th>
                <th>Status</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');

    loans.forEach(loan => {
        const status = loan.status === 'returned' ? 'Devolvido' :
                      loan.is_overdue ? 'Atrasado' : 'Ativo';
        const badgeType = loan.status === 'returned' ? 'success' :
                         loan.is_overdue ? 'danger' : 'warning';

        const statusBadge = createBadge(status, badgeType);

        const actions = loan.status === 'active' ? [
            {
                text: 'Devolver',
                className: 'btn-success',
                onClick: () => returnLoan(loan.id)
            }
        ] : [];

        const row = createTableRow([
            loan.book ? loan.book.title : '-',
            loan.member ? loan.member.name : '-',
            formatDate(loan.loan_date),
            formatDate(loan.due_date),
            statusBadge
        ], actions);

        tbody.appendChild(row);
    });

    container.innerHTML = '';
    container.appendChild(table);
}

async function openLoanForm() {
    try {
        const [booksRes, membersRes] = await Promise.all([
            api.getBooks(),
            api.getMembers()
        ]);

        const availableBooks = booksRes.data.filter(b => b.available > 0);
        const activeMembers = membersRes.data.filter(m => m.active);

        const modalBody = document.getElementById('modal-body');
        modalBody.innerHTML = `
            <h2>Novo Empréstimo</h2>
            <form id="loan-form">
                <div class="form-group">
                    <label>Livro *</label>
                    <select name="book_id" required>
                        <option value="">Selecione um livro</option>
                        ${availableBooks.map(book => `
                            <option value="${book.id}">
                                ${book.title} - ${book.author} (Disponível: ${book.available})
                            </option>
                        `).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>Membro *</label>
                    <select name="member_id" required>
                        <option value="">Selecione um membro</option>
                        ${activeMembers.map(member => `
                            <option value="${member.id}">${member.name} - ${member.email}</option>
                        `).join('')}
                    </select>
                </div>
                <div class="form-actions">
                    <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
                    <button type="submit" class="btn btn-primary">Registrar</button>
                </div>
            </form>
        `;

        document.getElementById('loan-form').onsubmit = saveLoan;
        openModal();
    } catch (error) {
        showToast('Erro ao abrir formulário', 'error');
    }
}

async function saveLoan(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        book_id: parseInt(formData.get('book_id')),
        member_id: parseInt(formData.get('member_id'))
    };

    try {
        await api.createLoan(data);
        showToast('Empréstimo registrado com sucesso!');
        closeModal();
        loadLoans();
        loadDashboard(); // atualizar estatísticas
    } catch (error) {
        showToast(error.message || 'Erro ao registrar empréstimo', 'error');
    }
}

async function returnLoan(id) {
    if (!confirm('Confirma a devolução deste livro?')) return;

    try {
        await api.returnLoan(id);
        showToast('Devolução registrada com sucesso!');
        loadLoans();
        loadDashboard(); // atualizar estatísticas
    } catch (error) {
        showToast(error.message || 'Erro ao registrar devolução', 'error');
    }
}
