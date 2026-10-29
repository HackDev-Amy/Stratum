import { create } from "zustand";

let id = 0;
export const useToasts = create((set) => ({
  items: [],
  push: (msg, type = "info") => {
    const tid = ++id;
    set((s) => ({ items: [...s.items, { id: tid, msg, type }] }));
    setTimeout(() => {
      set((s) => ({ items: s.items.filter((t) => t.id !== tid) }));
    }, 3500);
  },
  remove: (tid) => set((s) => ({ items: s.items.filter((t) => t.id !== tid) })),
}));

export const toast = (msg, type) => useToasts.getState().push(msg, type);