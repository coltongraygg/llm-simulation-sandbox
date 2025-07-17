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
        const runSimulationBtn = document.getElementById('run-simulation');

        addParticipantBtn.addEventListener('click', () => this.addParticipant());
        scenarioForm.addEventListener('submit', (e) => this.saveScenario(e));
        runSimulationBtn.addEventListener('click', () => this.runSimulation());

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
        this.updateRunButtonState();
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
            
            this.updateRunButtonState();
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

    updateRunButtonState() {
        const runBtn = document.getElementById('run-simulation');
        const isValid = this.validateScenario();
        runBtn.disabled = !isValid || !this.currentScenarioId;
    }

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

    async saveScenario(event) {
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
            this.showLoading(true);
            const response = await this.apiCall('/scenarios', 'POST', scenarioData);
            this.currentScenarioId = response.id;
            this.showNotification('Scenario saved successfully!', 'success');
            this.updateRunButtonState();
        } catch (error) {
            this.showNotification(`Failed to save scenario: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async runSimulation() {
        if (!this.currentScenarioId) {
            this.showNotification('Please save the scenario first', 'error');
            return;
        }

        try {
            this.showLoading(true);
            this.showNotification('Running simulation...', 'info');
            
            const response = await this.apiCall(`/run?scenario_id=${this.currentScenarioId}`, 'POST');
            this.showNotification('Simulation completed!', 'success');
            
            // Switch to conversation viewer
            this.showConversation(response);
        } catch (error) {
            this.showNotification(`Simulation failed: ${error.message}`, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    showConversation(runData) {
        // TODO: Implement in Phase 6
        console.log('Show conversation:', runData);
        this.showNotification('Conversation viewer will be implemented in Phase 6', 'info');
    }

    // Utility methods
    showNotification(message, type = 'info') {
        console.log(`${type.toUpperCase()}: ${message}`);
        // Will implement proper notification UI in later phases
    }

    showLoading(show = true) {
        console.log(`Loading: ${show}`);
        // Will implement proper loading UI in later phases
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.driftwoodApp = new DriftwoodApp();
});