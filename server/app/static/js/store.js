class Store {
  constructor(key, init) {
    this.state = init;
    this.subscribers = [];
    this.localStorageKey = key;

    if (this.state && Object.keys(this.state).length === 0) {
      this.load();
    } else {
      let newState = init; 
      this.load()
      this.setState(newState);
    }
  }

  load() {
    const savedState = localStorage.getItem(this.localStorageKey);
    if (savedState) {
      this.state = JSON.parse(savedState);
      this.notify();
    }
  }

  save() {
    localStorage.setItem(this.localStorageKey, JSON.stringify(this.state));
  }

  subscribe(listener) {
    this.subscribers.push(listener);
    listener(this.state);
  }

  notify() {
    this.subscribers.forEach((listener) => listener(this.state));
  }

  setState(newState) {
    this.state = { ...this.state, ...newState };
    this.save();
    this.notify();
  }
}
