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

  async putJson<T = unknown>(path: string, body: unknown, init?: RequestInit): Promise<T> {
    return this.getJson<T>(path, { method: "PUT", body: JSON.stringify(body), ...init })
  },

  async deleteJson<T = unknown>(path: string, init?: RequestInit): Promise<T> {
    return this.getJson<T>(path, { method: "DELETE", ...init })
  },
}

function extractDetailMessage(data: unknown): string | undefined {
  if (data && typeof data === "object") {
    const record = data as Record<string, unknown>
    const detail = record.detail
    if (typeof detail === "string") return detail
  }
  return undefined
}

async function normalizeError(res: Response) {
  const data: unknown = await res.json().catch(() => ({} as unknown))
  const message = extractDetailMessage(data) ?? res.statusText
  return Object.assign(new Error(message), {
    status: res.status,
    data,
  })
}


