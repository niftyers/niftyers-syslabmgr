import { defineStore } from 'pinia';
import { ref } from 'vue';

import { SessionCreate, SessionRetrieve, KEY_SIDEBAR } from '@/lib/common';

export const useSidebar = defineStore('storeDrawer', () => {
  const stored = SessionRetrieve(KEY_SIDEBAR);
  const State = ref(stored === null ? true : stored === 'true');
  const Rail = ref(true);

  function Get() {
    return State.value;
  }

  function Save(state: boolean) {
    State.value = state;
    SessionCreate(KEY_SIDEBAR, state.toString());
  }

  return { State, Rail, Save, Get };
});
