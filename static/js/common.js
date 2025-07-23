// Common JavaScript functions for VR180 Quick Editor

// Global modal management
let currentModal = null;

/**
 * Creates a modal with a message
 * @param {string} msg - The message to display in the modal
 * @returns {HTMLElement} - The modal element
 */
function createModal(msg) {
    // Remove existing modal if present
    if (currentModal) {
        dismissModal();
    }

    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: all;
    `;

    // Create modal container
    const modal = document.createElement('div');
    modal.id = 'modal-container';
    modal.style.cssText = `
        background-color: black;
        color: white;
        border: 1px solid white;
        padding: 20px;
        min-width: 300px;
        max-width: 80%;
        text-align: center;
        font-family: 'Fira Code', monospace;
        pointer-events: all;
    `;

    // Create message element
    const messageEl = document.createElement('div');
    messageEl.id = 'modal-message';
    messageEl.textContent = msg;
    messageEl.style.cssText = `
        margin-bottom: 15px;
        line-height: 1.4;
    `;

    // Create button container (initially empty)
    const buttonContainer = document.createElement('div');
    buttonContainer.id = 'modal-buttons';
    buttonContainer.style.cssText = `
        margin-top: 15px;
    `;

    // Assemble modal
    modal.appendChild(messageEl);
    modal.appendChild(buttonContainer);
    overlay.appendChild(modal);

    // Prevent click-through by stopping event propagation
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            e.stopPropagation();
            e.preventDefault();
        }
    });

    modal.addEventListener('click', (e) => {
        e.stopPropagation();
        e.preventDefault();
    });

    // Add to document
    document.body.appendChild(overlay);
    currentModal = overlay;

    return overlay;
}

/**
 * Updates an existing modal with a new message and adds a button that refreshes the page
 * @param {string} msg - The new message to display
 */
function setRefreshModalPrompt(msg) {
    if (!currentModal) {
        createModal(msg);
    }

    // Update message
    const messageEl = currentModal.querySelector('#modal-message');
    if (messageEl) {
        messageEl.textContent = msg;
    }

    // Add refresh button
    const buttonContainer = currentModal.querySelector('#modal-buttons');
    if (buttonContainer) {
        // Clear existing buttons
        buttonContainer.innerHTML = '';

        // Create refresh button
        const refreshBtn = document.createElement('button');
        refreshBtn.textContent = 'OK';
        refreshBtn.style.cssText = `
            border: 1px solid white;
            border-radius: 2px;
            padding: 10px 20px;
            background-color: black;
            color: white;
            font-family: 'Fira Code', monospace;
            cursor: pointer;
            margin: 5px;
        `;

        // Add hover effects
        refreshBtn.addEventListener('mouseenter', () => {
            refreshBtn.style.backgroundColor = '#333';
        });

        refreshBtn.addEventListener('mouseleave', () => {
            refreshBtn.style.backgroundColor = 'black';
        });

        refreshBtn.addEventListener('mousedown', () => {
            refreshBtn.style.backgroundColor = '#999';
            refreshBtn.style.color = 'black';
        });

        refreshBtn.addEventListener('mouseup', () => {
            refreshBtn.style.backgroundColor = '#333';
            refreshBtn.style.color = 'white';
        });

        // Add click handler to refresh page instead of dismissing modal
        refreshBtn.addEventListener('click', () => {
            window.location.reload();
        });

        buttonContainer.appendChild(refreshBtn);
    }
}

/**
 * Dismisses the current modal
 */
function dismissModal() {
    if (currentModal) {
        document.body.removeChild(currentModal);
        currentModal = null;
    }
}

/**
 * Creates a custom modal with custom buttons
 * @param {string} msg - The message to display
 * @param {Array} buttons - Array of button objects {text, callback, style}
 * @returns {HTMLElement} - The modal element
 */
function createCustomModal(msg, buttons = []) {
    const modal = createModal(msg);
    const buttonContainer = modal.querySelector('#modal-buttons');

    if (buttons.length > 0 && buttonContainer) {
        buttonContainer.innerHTML = '';

        buttons.forEach(buttonConfig => {
            const btn = document.createElement('button');
            btn.textContent = buttonConfig.text || 'Button';
            btn.style.cssText = `
                border: 1px solid white;
                border-radius: 2px;
                padding: 10px 20px;
                background-color: black;
                color: white;
                font-family: 'Fira Code', monospace;
                cursor: pointer;
                margin: 5px;
                ${buttonConfig.style || ''}
            `;

            // Add hover effects
            btn.addEventListener('mouseenter', () => {
                btn.style.backgroundColor = '#333';
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.backgroundColor = 'black';
            });

            btn.addEventListener('mousedown', () => {
                btn.style.backgroundColor = '#999';
                btn.style.color = 'black';
            });

            btn.addEventListener('mouseup', () => {
                btn.style.backgroundColor = '#333';
                btn.style.color = 'white';
            });

            // Add click handler
            btn.addEventListener('click', () => {
                if (buttonConfig.callback) {
                    buttonConfig.callback();
                }
                if (buttonConfig.dismissOnClick !== false) {
                    dismissModal();
                }
            });

            buttonContainer.appendChild(btn);
        });
    }

    return modal;
}

// Export functions for global use
window.createModal = createModal;
window.setRefreshModalPrompt = setRefreshModalPrompt;
window.dismissModal = dismissModal;
window.createCustomModal = createCustomModal;
