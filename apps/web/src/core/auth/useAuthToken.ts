"use client"
import { useAuth } from "@clerk/nextjs"

export function useAuthToken(): () => Promise<string | null> {
  const { getToken } = useAuth()
  return async () => {
    try {
      const direct = await getToken()
      if (direct) return direct
      const tpl = process.env.NEXT_PUBLIC_CLERK_TOKEN_TEMPLATE || "default"
      return await getToken({ template: tpl })
    } catch {
      return null
    }
  }
}


