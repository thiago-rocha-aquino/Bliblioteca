// Members 

async function loadMembers() {
    try {
        const response = await api.getMembers();
        displayMembers(response.data);
    } catch (error) {
        showToast('Erro ao carregar membros', 'error');
    }
}

function displayMembers(members) {
    const container = document.getElementById('members-list');

    if (!members || members.length === 0) {
        container.innerHTML = '<p class="loading">Nenhum membro cadastrado</p>';
        return;
    }

    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Nome</th>
                <th>Email</th>
                <th>Telefone</th>
                <th>Status</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');

    members.forEach(member => {
        const statusBadge = member.active ?
            createBadge('Ativo', 'success') :
            createBadge('Inativo', 'danger');

        const row = createTableRow([
            member.name,
            member.email,
            member.phone || '-',
            statusBadge
        ], [
            {
                text: 'Editar',
                className: 'btn-primary',
                onClick: () => editMember(member)
            },
            {
                text: 'Excluir',
                className: 'btn-danger',
                onClick: () => deleteMember(member.id)
            }
        ]);

        tbody.appendChild(row);
    });

    container.innerHTML = '';
    container.appendChild(table);
}

function openMemberForm(member = null) {
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <h2>${member ? 'Editar Membro' : 'Novo Membro'}</h2>
        <form id="member-form">
            <div class="form-group">
                <label>Nome *</label>
                <input type="text" name="name" value="${member ? member.name : ''}" required>
            </div>
            <div class="form-group">
                <label>Email *</label>
                <input type="email" name="email" value="${member ? member.email : ''}" required>
            </div>
            <div class="form-group">
                <label>Telefone</label>
                <input type="tel" name="phone" value="${member ? member.phone || '' : ''}" placeholder="(00) 00000-0000">
            </div>
            <div class="form-group">
                <label>Endereço</label>
                <textarea name="address">${member ? member.address || '' : ''}</textarea>
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" name="active" ${member && member.active !== false ? 'checked' : ''}>
                    Ativo
                </label>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
                <button type="submit" class="btn btn-primary">Salvar</button>
            </div>
        </form>
    `;

    document.getElementById('member-form').onsubmit = (e) => saveMember(e, member);
    openModal();
}

async function saveMember(e, existingMember) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    data.active = form.active.checked;

    try {
        if (existingMember) {
            await api.updateMember(existingMember.id, data);
            showToast('Membro atualizado com sucesso!');
        } else {
            await api.createMember(data);
            showToast('Membro cadastrado com sucesso!');
        }

        closeModal();
        loadMembers();
    } catch (error) {
        showToast(error.message || 'Erro ao salvar membro', 'error');
    }
}

function editMember(member) {
    openMemberForm(member);
}

async function deleteMember(id) {
    if (!confirm('Deseja realmente excluir este membro?')) return;

    try {
        await api.deleteMember(id);
        showToast('Membro removido com sucesso!');
        loadMembers();
    } catch (error) {
        showToast(error.message || 'Erro ao remover membro', 'error');
    }
}
