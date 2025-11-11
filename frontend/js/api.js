// API Base URL
const API_URL = 'http://localhost:3002/api';

// API Client
const api = {
    // requisição genérica
    async request(endpoint, options = {}) {
        const url = `${API_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            console.log(data);

            if (!response.ok) {
                throw new Error(data.message || 'Erro na requisição');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // livros
    async getBooks() {
        return this.request('/books');
    },

    async getBook(id) {
        return this.request(`/books/${id}`);
    },

    async createBook(data) {
        return this.request('/books', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async updateBook(id, data) {
        return this.request(`/books/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    async deleteBook(id) {
        return this.request(`/books/${id}`, {
            method: 'DELETE'
        });
    },

    async searchBooks(query) {
        return this.request(`/books/search?q=${encodeURIComponent(query)}`);
    },

    // Membros
    async getMembers() {
        return this.request('/members');
    },

    async getMember(id) {
        return this.request(`/members/${id}`);
    },

    async createMember(data) {
        return this.request('/members', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async updateMember(id, data) {
        return this.request(`/members/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    async deleteMember(id) {
        return this.request(`/members/${id}`, {
            method: 'DELETE'
        });
    },

    // Loans
    async getLoans() {
        return this.request('/loans');
    },

    async getLoan(id) {
        return this.request(`/loans/${id}`);
    },

    async createLoan(data) {
        return this.request('/loans', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async returnLoan(id) {
        return this.request(`/loans/${id}/return`, {
            method: 'POST'
        });
    },

    async getActiveLoans() {
        return this.request('/loans/active');
    },

    async getOverdueLoans() {
        return this.request('/loans/overdue');
    },

    // Dashboard
    async getStats() {
        return this.request('/dashboard/stats');
    },

    async getRecentActivity() {
        return this.request('/dashboard/recent-activity');
    }
};
