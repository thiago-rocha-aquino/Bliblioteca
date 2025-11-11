// Dashboard funcionalidades

async function loadDashboard() {
    try {
        const [stats, activity] = await Promise.all([
            api.getStats(),
            api.getRecentActivity()
        ]);

        updateStats(stats.data);
        updateRecentActivity(activity.data);
    } catch (error) {
        showToast('Erro ao carregar dashboard', 'error');
    }
}

function updateStats(stats) {
    document.getElementById('stat-total-books').textContent = stats.books.total;
    document.getElementById('stat-total-members').textContent = stats.members.active;
    document.getElementById('stat-active-loans').textContent = stats.loans.active;
    document.getElementById('stat-overdue-loans').textContent = stats.loans.overdue;
}

function updateRecentActivity(activity) {
    const container = document.getElementById('recent-loans');
    container.innerHTML = '';

    if (!activity.recent_loans || activity.recent_loans.length === 0) {
        container.innerHTML = '<p class="loading">Nenhuma atividade recente</p>';
        return;
    }

    activity.recent_loans.slice(0, 5).forEach(loan => {
        const div = document.createElement('div');
        div.className = 'activity-item';

        const status = loan.status === 'returned' ? 'Devolvido' :
                      loan.is_overdue ? 'Atrasado' : 'Ativo';
        const badgeType = loan.status === 'returned' ? 'success' :
                         loan.is_overdue ? 'danger' : 'warning';

        div.innerHTML = `
            <strong>${loan.book ? loan.book.title : 'Livro'}</strong> -
            ${loan.member ? loan.member.name : 'Membro'}
            <span class="badge badge-${badgeType}">${status}</span>
            <br>
            <small style="color: var(--text-light);">
                Empréstimo: ${formatDate(loan.loan_date)} |
                Devolução: ${formatDate(loan.due_date)}
            </small>
        `;

        container.appendChild(div);
    });
}
