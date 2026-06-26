export const SessionCreate = (key: string, val: string) => {
  sessionStorage.setItem(key, val);
};

export const SessionRetrieve = (key: string): string => {
  const value = sessionStorage.getItem(key) ?? '';
  return value;
};

export const SessionClear = (key: string) => {
  sessionStorage.removeItem(key);
};
