export const api = {
  async getJson<T>(path: string, init?: RequestInit): Promise<T> {
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
    const res = await fetch(`${base}${path}`, {
      ...init,
      headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
      cache: "no-store",
    })
    if (!res.ok) throw await normalizeError(res)
    return res.json() as Promise<T>
  },
  async postJson<T = unknown>(path: string, body: unknown, init?: RequestInit): Promise<T> {
    return this.getJson<T>(path, { method: "POST", body: JSON.stringify(body), ...init })
  },
}

async function normalizeError(res: Response) {
  const data = await res.json().catch(() => ({}))
  return Object.assign(new Error((data as any)?.detail ?? res.statusText), {
    status: res.status,
    data,
  })
}


