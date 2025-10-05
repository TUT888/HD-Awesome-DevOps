document.addEventListener('DOMContentLoaded', () => {
    // API endpoints - these will be replaced during deployment
    // const USERS_API_BASE_URL = '_USERS_API_URL_';
    // const NOTES_API_BASE_URL = '_NOTES_API_URL_';
    const USERS_API_BASE_URL = 'http://localhost:5000';
    const NOTES_API_BASE_URL = 'http://localhost:5001';

    // DOM Elements
    const messageBox = document.getElementById('message-box');
    const userForm = document.getElementById('user-form');
    const userListDiv = document.getElementById('user-list');
    const noteForm = document.getElementById('note-form');
    const noteListDiv = document.getElementById('note-list');
    const filterBtn = document.getElementById('filter-btn');
    const clearFilterBtn = document.getElementById('clear-filter-btn');
    const editModal = document.getElementById('edit-modal');
    const editNoteForm = document.getElementById('edit-note-form');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');

    let currentEditNoteId = null;
    let currentFilter = null;

    // --- Utility Functions ---
    function showMessage(message, type = 'info') {
        messageBox.textContent = message;
        messageBox.className = `message-box ${type}`;
        messageBox.style.display = 'block';
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 5000);
    }

    // --- User Service Interactions ---
    async function fetchUsers() {
        userListDiv.innerHTML = '<p>Loading users...</p>';
        try {
            const response = await fetch(`${USERS_API_BASE_URL}/users/`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            const users = await response.json();
            
            userListDiv.innerHTML = '';

            if (users.length === 0) {
                userListDiv.innerHTML = '<p>No users registered yet.</p>';
                return;
            }

            users.forEach(user => {
                const userCard = document.createElement('div');
                userCard.className = 'user-card';
                userCard.innerHTML = `
                    <h3>${user.username} (ID: ${user.id})</h3>
                    <p>Email: ${user.email}</p>
                    <p><small>Created: ${new Date(user.created_at).toLocaleString()}</small></p>
                `;
                userListDiv.appendChild(userCard);
            });
        } catch (error) {
            console.error('Error fetching users:', error);
            showMessage(`Failed to load users: ${error.message}`, 'error');
            userListDiv.innerHTML = '<p>Could not load users.</p>';
        }
    }

    userForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('user-username').value;
        const email = document.getElementById('user-email').value;

        try {
            const response = await fetch(`${USERS_API_BASE_URL}/users/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const newUser = await response.json();
            showMessage(`User "${newUser.username}" registered successfully! ID: ${newUser.id}`, 'success');
            userForm.reset();
            fetchUsers();
        } catch (error) {
            console.error('Error registering user:', error);
            showMessage(`Error: ${error.message}`, 'error');
        }
    });

    // --- Notes Service Interactions ---
    async function fetchNotes(userId = null) {
        noteListDiv.innerHTML = '<p>Loading notes...</p>';
        try {
            let url = `${NOTES_API_BASE_URL}/notes/`;
            if (userId) {
                url += `?user_id=${userId}`;
            } else {
                url += `?user_id=0`;
            }

            const response = await fetch(url);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            const notes = await response.json();
            
            noteListDiv.innerHTML = '';

            if (notes.length === 0) {
                noteListDiv.innerHTML = '<p>No notes found.</p>';
                return;
            }

            notes.forEach(note => {
                const noteCard = document.createElement('div');
                noteCard.className = 'note-card';
                noteCard.innerHTML = `
                    <h3>${note.title}</h3>
                    <p>User ID: ${note.user_id} | Note ID: ${note.id}</p>
                    <div class="content">${note.content}</div>
                    <p><small>Created: ${new Date(note.created_at).toLocaleString()}</small></p>
                    ${note.updated_at ? `<p><small>Updated: ${new Date(note.updated_at).toLocaleString()}</small></p>` : ''}
                    <div class="card-actions">
                        <button class="edit-btn" data-id="${note.id}">Edit</button>
                        <button class="delete-btn" data-id="${note.id}">Delete</button>
                    </div>
                `;
                noteListDiv.appendChild(noteCard);
            });
        } catch (error) {
            console.error('Error fetching notes:', error);
            showMessage(`Failed to load notes: ${error.message}`, 'error');
            noteListDiv.innerHTML = '<p>Could not load notes.</p>';
        }
    }

    noteForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const user_id = parseInt(document.getElementById('note-user-id').value);
        const title = document.getElementById('note-title').value;
        const content = document.getElementById('note-content').value;

        try {
            const response = await fetch(`${NOTES_API_BASE_URL}/notes/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id, title, content }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const newNote = await response.json();
            showMessage(`Note "${newNote.title}" created successfully!`, 'success');
            noteForm.reset();
            fetchNotes(currentFilter);
        } catch (error) {
            console.error('Error creating note:', error);
            showMessage(`Error: ${error.message}`, 'error');
        }
    });

    // Filter functionality
    filterBtn.addEventListener('click', () => {
        const userId = document.getElementById('filter-user-id').value;
        currentFilter = userId ? parseInt(userId) : null;
        fetchNotes(currentFilter);
    });

    clearFilterBtn.addEventListener('click', () => {
        document.getElementById('filter-user-id').value = '';
        currentFilter = null;
        fetchNotes();
    });

    // Edit and Delete handlers
    noteListDiv.addEventListener('click', async (event) => {
        // Delete Note
        if (event.target.classList.contains('delete-btn')) {
            const noteId = event.target.dataset.id;
            if (!confirm(`Delete note ID: ${noteId}?`)) return;

            try {
                const response = await fetch(`${NOTES_API_BASE_URL}/notes/${noteId}`, {
                    method: 'DELETE',
                });

                if (response.status === 204) {
                    showMessage(`Note deleted successfully`, 'success');
                    fetchNotes(currentFilter);
                } else {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Delete failed');
                }
            } catch (error) {
                console.error('Error deleting note:', error);
                showMessage(`Error: ${error.message}`, 'error');
            }
        }

        // Edit Note
        if (event.target.classList.contains('edit-btn')) {
            const noteId = event.target.dataset.id;
            
            try {
                const response = await fetch(`${NOTES_API_BASE_URL}/notes/${noteId}`);
                if (!response.ok) throw new Error('Failed to fetch note');
                
                const note = await response.json();
                currentEditNoteId = noteId;
                document.getElementById('edit-note-title').value = note.title;
                document.getElementById('edit-note-content').value = note.content;
                editModal.style.display = 'block';
            } catch (error) {
                console.error('Error loading note for edit:', error);
                showMessage(`Error: ${error.message}`, 'error');
            }
        }
    });

    // Edit form submission
    editNoteForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const title = document.getElementById('edit-note-title').value;
        const content = document.getElementById('edit-note-content').value;

        try {
            const response = await fetch(`${NOTES_API_BASE_URL}/notes/${currentEditNoteId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, content }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Update failed');
            }

            showMessage('Note updated successfully!', 'success');
            editModal.style.display = 'none';
            fetchNotes(currentFilter);
        } catch (error) {
            console.error('Error updating note:', error);
            showMessage(`Error: ${error.message}`, 'error');
        }
    });

    cancelEditBtn.addEventListener('click', () => {
        editModal.style.display = 'none';
    });

    // Initial load
    fetchUsers();
    fetchNotes();

    // Auto-refresh every 15 seconds
    setInterval(() => {
        fetchNotes(currentFilter);
    }, 15000);
});