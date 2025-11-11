let currentBooks = [];

async function loadBooks() {
    try {
        const response = await api.getBooks();
        //console.log('Response completa:', response); // Debug
        //console.log('Response.data:', response.data); // Debug
        
        // A resposta pode estar em um nível diferente
        const books = response.data || response;
        currentBooks = books;
        displayBooks(currentBooks);
    } catch (error) {
        //console.error('Erro completo:', error); // Debug
        showToast('Erro ao carregar livros', 'error');
    }
}

function displayBooks(books) {
    const container = document.getElementById('books-list');

    if (!books || books.length === 0) {
        container.innerHTML = '<p class="loading">Nenhum livro cadastrado</p>';
        return;
    }

    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Título</th>
                <th>Autor</th>
                <th>ISBN</th>
                <th>Categoria</th>
                <th>Qtd</th>
                <th>Disponível</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');

    books.forEach(book => {
        const row = createTableRow([
            book.title,
            book.author,
            book.isbn,
            book.category || '-',
            book.quantity,
            book.available
        ], [
            {
                text: 'Editar',
                className: 'btn-primary',
                onClick: () => editBook(book)
            },
            {
                text: 'Excluir',
                className: 'btn-danger',
                onClick: () => deleteBook(book.id)
            }
        ]);

        tbody.appendChild(row);
    });

    container.innerHTML = '';
    container.appendChild(table);
}

function openBookForm(book = null) {
    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <h2>${book ? 'Editar Livro' : 'Novo Livro'}</h2>
        <form id="book-form">
            <div class="form-group">
                <label>Título *</label>
                <input type="text" name="title" value="${book ? book.title : ''}" required>
            </div>
            <div class="form-group">
                <label>Autor *</label>
                <input type="text" name="author" value="${book ? book.author : ''}" required>
            </div>
            <div class="form-group">
                <label>ISBN *</label>
                <input type="text" name="isbn" value="${book ? book.isbn : ''}" required>
            </div>
            <div class="form-group">
                <label>Editora</label>
                <input type="text" name="publisher" value="${book ? book.publisher || '' : ''}">
            </div>
            <div class="form-group">
                <label>Ano</label>
                <input type="number" name="year" value="${book ? book.year || '' : ''}">
            </div>
            <div class="form-group">
                <label>Categoria</label>
                <input type="text" name="category" value="${book ? book.category || '' : ''}">
            </div>
            <div class="form-group">
                <label>Quantidade *</label>
                <input type="number" name="quantity" value="${book ? book.quantity : 1}" required min="1">
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancelar</button>
                <button type="submit" class="btn btn-primary">Salvar</button>
            </div>
        </form>
    `;

    document.getElementById('book-form').onsubmit = (e) => saveBook(e, book);
    openModal();
}

async function saveBook(e, existingBook) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    // converter datas numéricas 
    if (data.year) data.year = parseInt(data.year);
    data.quantity = parseInt(data.quantity);

    try {
        if (existingBook) {
            await api.updateBook(existingBook.id, data);
            showToast('Livro atualizado com sucesso!');
        } else {
            await api.createBook(data);
            showToast('Livro cadastrado com sucesso!');
        }

        closeModal();
        loadBooks();
    } catch (error) {
        showToast(error.message || 'Erro ao salvar livro', 'error');
    }
}

function editBook(book) {
    openBookForm(book);
}

async function deleteBook(id) {
    if (!confirm('Deseja realmente excluir este livro?')) return;

    try {
        await api.deleteBook(id);
        showToast('Livro removido com sucesso!');
        loadBooks();
    } catch (error) {
        showToast(error.message || 'Erro ao remover livro', 'error');
    }
}

//  busca de livros
document.getElementById('book-search').addEventListener('input', async (e) => {
    const query = e.target.value.trim();

    if (query.length === 0) {
        displayBooks(currentBooks);
        return;
    }

    if (query.length < 2) return;

    try {
        const response = await api.searchBooks(query);
        displayBooks(response.data);
    } catch (error) {
        showToast('Erro na busca', 'error');
    }
});
