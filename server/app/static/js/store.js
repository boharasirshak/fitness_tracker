class Store {
  constructor(key, init) {
    this.state = init;
    this.subscribers = [];
    this.localStorageKey = key;

    if (this.state !== undefined && Object.keys(this.state).length === 0) {
      this.load();
    } else {
      this.load()
      this.setState(init);
      this.save()
      this.notify()
    }
  }

  load() {
    const savedState = localStorage.getItem(this.localStorageKey);
    if (savedState) {
      this.state = JSON.parse(savedState);
      this.notify();
    }
    return this.state;
  }

  save() {
    localStorage.setItem(this.localStorageKey, JSON.stringify(this.state));
  }

  subscribe(listener) {
    this.subscribers.push(listener);
    listener(this.state);
  }

  change(newState) {
    this.state = newState;
  }

  notify() {
    this.subscribers.forEach((listener) => listener(this.state));
  }

  setState(newState) {
    if (newState) {
      this.state = { ...this.state, ...newState };
    } else {
      this.state = { ...this.state };
    }
    this.save();
    this.notify();
  }
}
