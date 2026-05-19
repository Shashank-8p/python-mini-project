function saveToStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function loadFromStorage(key, defaultValue = null) {
    const data = localStorage.getItem(key);

    if (!data) return defaultValue;

    try {
        return JSON.parse(data);
    } catch {
        return defaultValue;
    }
}

function removeFromStorage(key) {
    localStorage.removeItem(key);
}

const storageHelpers = {
    saveToStorage,
    loadFromStorage,
    removeFromStorage,
};

if (typeof window !== 'undefined') {
    window.appStorage = storageHelpers;
}

export { saveToStorage, loadFromStorage, removeFromStorage };
