export const fetchHello = async (): Promise<any> => {
  const res = await fetch('/api/hello')
  return await res.json()
}