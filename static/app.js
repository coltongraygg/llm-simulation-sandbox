// Driftwood LLM Simulation Lab - Frontend Application

class DriftwoodApp {
    constructor() {
        this.currentView = 'scenario';
        this.participants = [];
        this.currentScenarioId = null;
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupScenarioBuilder();
        this.setupConversationViewer();
        this.setupHistoryViewer();
        this.setupNotifications();
        this.showView('scenario');
    }

    setupNavigation() {
        const navButtons = document.querySelectorAll('.nav-btn');
        navButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const viewName = e.target.id.replace('nav-', '');
                this.showView(viewName);
            });
        });
    }

    showView(viewName) {
        // Hide all views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
        });

        // Remove active class from all nav buttons
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Show target view
        const targetView = document.getElementById(`view-${viewName}`);
        if (targetView) {
            targetView.classList.add('active');
            this.currentView = viewName;
        }

        // Activate corresponding nav button
        const navBtn = document.getElementById(`nav-${viewName}`);
        if (navBtn) {
            navBtn.classList.add('active');
        }

        // Load history data when switching to history view
        if (viewName === 'history') {
            this.loadHistory();
        }
    }

    // API helper methods
    async apiCall(endpoint, method = 'GET', data = null) {
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(endpoint, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }

    setupScenarioBuilder() {
        const addParticipantBtn = document.getElementById('add-participant');
        const scenarioForm = document.getElementById('scenario-form');

        addParticipantBtn.addEventListener('click', () => this.addParticipant());
        scenarioForm.addEventListener('submit', (e) => this.saveAndRunScenario(e));

        // Add initial participant
        this.addParticipant();
    }

    addParticipant() {
        const participantId = `participant-${Date.now()}`;
        const participant = {
            id: participantId,
            name: '',
            role: '',
            perspective: '',
            meta_tags: [],
            initial_message: ''
        };

        this.participants.push(participant);
        this.renderParticipant(participant);
    }

    renderParticipant(participant) {
        const container = document.getElementById('participants-container');
        const participantCard = document.createElement('div');
        participantCard.className = 'participant-card';
        participantCard.dataset.participantId = participant.id;

        participantCard.innerHTML = `
            <h4>
                Participant ${this.participants.length}
                <button type="button" class="remove-participant" onclick="window.driftwoodApp.removeParticipant('${participant.id}')">
                    Remove
                </button>
            </h4>
            
            <div class="form-group">
                <label>Name</label>
                <input type="text" name="participant-name" placeholder="e.g., Jordan" required
                       onchange="window.driftwoodApp.updateParticipant('${participant.id}', 'name', this.value)">
            </div>
            
            <div class="form-group">
                <label>Role</label>
                <input type="text" name="participant-role" placeholder="e.g., Upset with Alex" required
                       onchange="window.driftwoodApp.updateParticipant('${participant.id}', 'role', this.value)">
            </div>
            
            <div class="form-group">
                <label>Perspective</label>
                <input type="text" name="participant-perspective" placeholder="e.g., Feels unheard and emotionally distant" required
                       onchange="window.driftwoodApp.updateParticipant('${participant.id}', 'perspective', this.value)">
            </div>
            
            <div class="form-group">
                <label>Initial Message</label>
                <textarea name="participant-initial-message" rows="2" placeholder="What this participant says to start the conversation..." required
                          onchange="window.driftwoodApp.updateParticipant('${participant.id}', 'initial_message', this.value)"></textarea>
            </div>
            
            <div class="form-group">
                <label>Meta Tags (emotional state - max 3)</label>
                <input type="text" name="participant-meta-tag-1" placeholder="e.g., angry" 
                       onchange="window.driftwoodApp.updateMetaTag('${participant.id}', 0, this.value)">
                <input type="text" name="participant-meta-tag-2" placeholder="e.g., resentful" 
                       onchange="window.driftwoodApp.updateMetaTag('${participant.id}', 1, this.value)">
                <input type="text" name="participant-meta-tag-3" placeholder="e.g., powerless" 
                       onchange="window.driftwoodApp.updateMetaTag('${participant.id}', 2, this.value)">
            </div>
        `;

        container.appendChild(participantCard);
    }

    removeParticipant(participantId) {
        this.participants = this.participants.filter(p => p.id !== participantId);
        const card = document.querySelector(`[data-participant-id="${participantId}"]`);
        if (card) {
            card.remove();
        }
        
        // Update participant numbers
        this.updateParticipantNumbers();
    }

    updateParticipant(participantId, field, value) {
        const participant = this.participants.find(p => p.id === participantId);
        if (participant) {
            participant[field] = value;
        }
        // No longer need to update run button state
    }

    updateMetaTag(participantId, index, value) {
        const participant = this.participants.find(p => p.id === participantId);
        if (participant) {
            // Ensure meta_tags array has 3 slots
            while (participant.meta_tags.length < 3) {
                participant.meta_tags.push('');
            }
            
            // Update the specific index
            participant.meta_tags[index] = value.trim();
        }
    }

    updateParticipantNumbers() {
        const cards = document.querySelectorAll('.participant-card');
        cards.forEach((card, index) => {
            const header = card.querySelector('h4');
            const participantId = card.dataset.participantId;
            const removeButton = card.querySelector('.remove-participant');
            header.innerHTML = `
                Participant ${index + 1}
                <button type="button" class="remove-participant" onclick="window.driftwoodApp.removeParticipant('${participantId}')">
                    Remove
                </button>
            `;
        });
    }

    // No longer needed - removed run button state management
    // Form validation is now handled in saveAndRunScenario

    validateScenario() {
        const name = document.getElementById('scenario-name').value.trim();
        const systemPrompt = document.getElementById('system-prompt').value.trim();
        
        if (!name || !systemPrompt || this.participants.length === 0) {
            return false;
        }

        return this.participants.every(p => 
            p.name && p.role && p.perspective && p.initial_message && 
            p.meta_tags.some(tag => tag.trim() !== '')
        );
    }

    async saveAndRunScenario(event) {
        event.preventDefault();
        
        if (!this.validateScenario()) {
            this.showNotification('Please fill in all required fields', 'error');
            return;
        }

        const formData = new FormData(event.target);
        const scenarioData = {
            name: formData.get('name'),
            system_prompt: formData.get('system_prompt'),
            participants: this.participants.map(p => ({
                name: p.name,
                role: p.role,
                perspective: p.perspective,
                meta_tags: p.meta_tags.filter(tag => tag.trim() !== ''),
                initial_message: p.initial_message
            })),
            settings: {
                model: formData.get('model'),
                temperature: parseFloat(formData.get('temperature')),
                max_tokens: parseInt(formData.get('max_tokens'))
            }
        };

        try {
            this.showLoading(true, 'Creating scenario and running simulation...');
            
            // Step 1: Save scenario
            const scenarioResponse = await this.apiCall('/scenarios', 'POST', scenarioData);
            
            // Step 2: Run simulation immediately
            const runResponse = await this.apiCall(`/run?scenario_id=${scenarioResponse.id}`, 'POST');
            
            this.showNotification('Simulation completed successfully!', 'success');
            
            // Switch to conversation viewer
            await this.showConversation(runResponse);
            
        } catch (error) {
            this.showNotification(`Failed to run simulation: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    setupHistoryViewer() {
        const filterAllBtn = document.getElementById('filter-all');
        const filterStarredBtn = document.getElementById('filter-starred');
        const deleteAllBtn = document.getElementById('delete-all-unstarred');
        
        filterAllBtn.addEventListener('click', () => {
            this.setHistoryFilter('all');
        });
        
        filterStarredBtn.addEventListener('click', () => {
            this.setHistoryFilter('starred');
        });
        
        deleteAllBtn.addEventListener('click', () => {
            this.deleteAllUnstarred();
        });
        
        this.currentHistoryFilter = 'all';
        this.runsCache = null;
    }

    setupConversationViewer() {
        const closeBtn = document.getElementById('close-conversation');
        closeBtn.addEventListener('click', () => {
            this.showView('history');
        });
    }

    async showConversation(runData) {
        try {
            this.showLoading(true, 'Loading conversation...');

            // Get full run details if we only have basic data
            let fullRunData = runData;
            if (!runData.log) {
                fullRunData = await this.apiCall(`/runs/${runData.id}`);
            }

            // Get scenario details
            const scenario = await this.apiCall(`/scenarios`);
            const runScenario = scenario.find(s => s.id === fullRunData.scenario_id);

            if (!runScenario) {
                this.showNotification('Scenario not found', 'error');
                return;
            }

            // Populate the conversation viewer
            this.populateConversationContext(runScenario, fullRunData);
            this.populateConversationLog(fullRunData.log);

            // Switch to conversation view
            this.showView('conversation');

        } catch (error) {
            this.showNotification(`Failed to load conversation: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    populateConversationContext(scenario, runData) {
        // Update title
        document.getElementById('conversation-title').textContent = scenario.name;

        // System Prompt
        const systemPromptEl = document.getElementById('context-system-prompt');
        systemPromptEl.innerHTML = `<p>${scenario.system_prompt}</p>`;

        // Model Settings
        const settingsEl = document.getElementById('context-settings');
        settingsEl.innerHTML = `
            <div class="setting-item">
                <span class="setting-label">Model:</span>
                <span>${scenario.settings.model}</span>
            </div>
            <div class="setting-item">
                <span class="setting-label">Temperature:</span>
                <span>${scenario.settings.temperature}</span>
            </div>
            <div class="setting-item">
                <span class="setting-label">Max Tokens:</span>
                <span>${scenario.settings.max_tokens}</span>
            </div>
        `;

        // Participants
        const participantsEl = document.getElementById('context-participants');
        participantsEl.innerHTML = scenario.participants.map(participant => `
            <div class="participant-item">
                <div class="participant-name">${participant.name}</div>
                <div class="participant-role">${participant.role}</div>
                <div class="participant-perspective">${participant.perspective}</div>
                <div class="participant-tags">
                    ${participant.meta_tags.map(tag => `
                        <span class="participant-tag">${tag}</span>
                    `).join('')}
                </div>
            </div>
        `).join('');

        // Update conversation timestamp
        const timestampEl = document.getElementById('conversation-timestamp');
        const timestamp = new Date(runData.timestamp).toLocaleString();
        timestampEl.textContent = timestamp;
    }

    populateConversationLog(conversationLog) {
        const chatLogEl = document.getElementById('chat-log');
        const messageCountEl = document.getElementById('message-count');

        // Update message count
        messageCountEl.textContent = `${conversationLog.length} messages`;

        // Clear existing messages
        chatLogEl.innerHTML = '';

        // Add messages
        conversationLog.forEach((message, index) => {
            const messageEl = document.createElement('div');
            const isAI = message.speaker === 'AI';
            
            messageEl.className = `message ${isAI ? 'ai-message' : 'participant-message'}`;
            
            const timestamp = new Date(message.timestamp).toLocaleTimeString();
            
            messageEl.innerHTML = `
                <div class="message-header">
                    <span class="message-speaker ${isAI ? 'ai' : 'participant'}">
                        ${isAI ? '🤖 AI (Driftwood)' : '👤 ' + message.speaker}
                    </span>
                    <span class="message-timestamp">${timestamp}</span>
                </div>
                <div class="message-content">${this.formatMessageContent(message.content)}</div>
            `;

            chatLogEl.appendChild(messageEl);
        });

        // Scroll to bottom
        chatLogEl.scrollTop = chatLogEl.scrollHeight;
    }

    formatMessageContent(content) {
        // Basic formatting - convert line breaks to <br> and preserve whitespace
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold **text**
            .replace(/\*(.*?)\*/g, '<em>$1</em>'); // Italic *text*
    }

    setupNotifications() {
        const closeBtn = document.getElementById('notification-close');
        closeBtn.addEventListener('click', () => {
            this.hideNotification();
        });
    }

    // History Management Methods
    async loadHistory() {
        try {
            const loadingEl = document.getElementById('history-loading');
            const emptyEl = document.getElementById('history-empty');
            const listEl = document.getElementById('history-list');
            
            // Show loading state
            loadingEl.style.display = 'flex';
            emptyEl.classList.add('hidden');
            listEl.innerHTML = '';
            
            // Fetch runs from API
            const runs = await this.apiCall('/runs');
            this.runsCache = runs;
            
            // Hide loading state
            loadingEl.style.display = 'none';
            
            // Show empty state or populate list
            if (runs.length === 0) {
                emptyEl.classList.remove('hidden');
            } else {
                this.renderHistory(runs);
            }
            
        } catch (error) {
            document.getElementById('history-loading').style.display = 'none';
            this.showNotification(`Failed to load history: ${error.message}`, 'error');
        }
    }

    setHistoryFilter(filter) {
        this.currentHistoryFilter = filter;
        
        // Update filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        if (filter === 'all') {
            document.getElementById('filter-all').classList.add('active');
        } else if (filter === 'starred') {
            document.getElementById('filter-starred').classList.add('active');
        }
        
        // Re-render history with filter
        if (this.runsCache) {
            this.renderHistory(this.runsCache);
        }
    }

    renderHistory(runs) {
        const listEl = document.getElementById('history-list');
        
        // Filter runs based on current filter
        let filteredRuns = runs;
        if (this.currentHistoryFilter === 'starred') {
            filteredRuns = runs.filter(run => run.starred);
        }
        
        // Sort by timestamp (latest first)
        filteredRuns.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        // Render filtered runs
        if (filteredRuns.length === 0) {
            listEl.innerHTML = '<div class="history-empty"><p>No runs found for this filter.</p></div>';
            return;
        }
        
        listEl.innerHTML = filteredRuns.map(run => this.renderHistoryItem(run)).join('');
    }

    renderHistoryItem(run) {
        const timestamp = new Date(run.timestamp).toLocaleString();
        const relativeTime = this.getRelativeTime(run.timestamp);
        
        return `
            <div class="history-item ${run.starred ? 'starred' : ''}" data-run-id="${run.id}">
                <div class="history-item-header">
                    <h3 class="history-item-title">${run.scenario_name || 'Unnamed Scenario'}</h3>
                    <button class="history-item-star ${run.starred ? 'starred' : ''}" 
                            onclick="window.driftwoodApp.toggleStar('${run.id}', ${!run.starred})">
                        ⭐
                    </button>
                </div>
                
                <div class="history-item-meta">
                    <div class="history-item-meta-item">
                        <span>🕐</span>
                        <span title="${timestamp}">${relativeTime}</span>
                    </div>
                    <div class="history-item-meta-item">
                        <span>💬</span>
                        <span>${this.getMessageCount(run)} messages</span>
                    </div>
                </div>
                
                <div class="history-item-actions">
                    <span class="history-item-id">${run.id.substring(0, 8)}...</span>
                    <button class="btn-view" onclick="window.driftwoodApp.viewHistoryItem('${run.id}')">
                        View Conversation
                    </button>
                    <button class="btn-delete" onclick="window.driftwoodApp.deleteRun('${run.id}')">
                        Delete
                    </button>
                </div>
            </div>
        `;
    }

    async toggleStar(runId, starred) {
        try {
            const response = await this.apiCall(`/runs/${runId}/star`, 'PATCH', { starred });
            
            // Update the cache
            if (this.runsCache) {
                const run = this.runsCache.find(r => r.id === runId);
                if (run) {
                    run.starred = starred;
                }
            }
            
            // Re-render the history
            if (this.runsCache) {
                this.renderHistory(this.runsCache);
            }
            
            this.showNotification(starred ? 'Run starred!' : 'Star removed', 'success');
            
        } catch (error) {
            this.showNotification(`Failed to update star: ${error.message}`, 'error');
        }
    }

    async viewHistoryItem(runId) {
        try {
            // Find the run in cache or fetch it
            let run = this.runsCache ? this.runsCache.find(r => r.id === runId) : null;
            
            if (!run) {
                // Fetch specific run if not in cache
                run = await this.apiCall(`/runs/${runId}`);
            }
            
            // Show the conversation
            await this.showConversation(run);
            
        } catch (error) {
            this.showNotification(`Failed to load conversation: ${error.message}`, 'error');
        }
    }

    async deleteRun(runId) {
        if (!confirm('Are you sure you want to delete this simulation run?')) {
            return;
        }
        
        try {
            await this.apiCall(`/runs/${runId}`, 'DELETE');
            
            // Remove from cache
            if (this.runsCache) {
                this.runsCache = this.runsCache.filter(run => run.id !== runId);
            }
            
            // Re-render history
            if (this.runsCache) {
                this.renderHistory(this.runsCache);
            }
            
            this.showNotification('Run deleted successfully', 'success');
            
        } catch (error) {
            this.showNotification(`Failed to delete run: ${error.message}`, 'error');
        }
    }

    async deleteAllUnstarred() {
        const unstarredCount = this.runsCache ? this.runsCache.filter(run => !run.starred).length : 0;
        
        if (unstarredCount === 0) {
            this.showNotification('No unstarred runs to delete', 'info');
            return;
        }
        
        if (!confirm(`Are you sure you want to delete all ${unstarredCount} unstarred simulation runs? This action cannot be undone.`)) {
            return;
        }
        
        try {
            this.showLoading(true, 'Deleting unstarred runs...');
            
            const response = await this.apiCall('/runs', 'DELETE');
            
            // Update cache - keep only starred runs
            if (this.runsCache) {
                this.runsCache = this.runsCache.filter(run => run.starred);
            }
            
            // Re-render history
            if (this.runsCache) {
                this.renderHistory(this.runsCache);
            }
            
            this.showNotification(`Deleted ${response.deleted_count} unstarred runs`, 'success');
            
        } catch (error) {
            this.showNotification(`Failed to delete runs: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    getRelativeTime(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffInSeconds = Math.floor((now - time) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} days ago`;
        
        return time.toLocaleDateString();
    }

    getMessageCount(run) {
        // This is a placeholder - the run summary doesn't include log data
        // In a real implementation, you might want to add message count to the API response
        return '~'; // Placeholder
    }

    // Utility methods
    showNotification(message, type = 'info') {
        const notification = document.getElementById('notification');
        const messageEl = document.getElementById('notification-message');
        
        messageEl.textContent = message;
        notification.className = `notification ${type}`;
        notification.classList.remove('hidden');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.hideNotification();
        }, 5000);
        
        console.log(`${type.toUpperCase()}: ${message}`);
    }

    hideNotification() {
        const notification = document.getElementById('notification');
        notification.classList.add('hidden');
    }

    showLoading(show = true, message = 'Processing...') {
        const overlay = document.getElementById('loading-overlay');
        const messageEl = document.getElementById('loading-message');
        
        if (show) {
            messageEl.textContent = message;
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.driftwoodApp = new DriftwoodApp();
});