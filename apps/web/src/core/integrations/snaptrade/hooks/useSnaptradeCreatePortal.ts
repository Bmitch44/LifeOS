"use client"

import { useMutation } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

type CreatePortalResponse = { redirectURI: string }

export function useSnaptradeCreatePortal() {
  const getToken = useAuthToken()
  return useMutation<CreatePortalResponse, Error, { user_secret: string }>({
    mutationFn: async ({ user_secret }) => {
      const token = await getToken()
      return api.postJson<CreatePortalResponse>(
        "/v1/snaptrade/connection-portal",
        { user_secret },
        { headers: token ? { Authorization: `Bearer ${token}` } : undefined }
      )
    },
  })
}


