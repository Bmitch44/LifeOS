"use client"

import { useMutation } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

type RegisterResponse = { user_secret: string; user_id: string }

export function useSnaptradeRegister() {
  const getToken = useAuthToken()
  return useMutation<RegisterResponse, Error, void>({
    mutationFn: async () => {
      const token = await getToken()
      return api.postJson<RegisterResponse>(
        "/v1/snaptrade/register",
        {},
        { headers: token ? { Authorization: `Bearer ${token}` } : undefined }
      )
    },
  })
}


