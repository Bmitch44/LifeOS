"use client"

import { useMutation } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

type CreatePortalResponse = string

export function useSnaptradeCreatePortal() {
  const getToken = useAuthToken()
  return useMutation<CreatePortalResponse, Error, void>({
    mutationFn: async () => {
      const token = await getToken()
      return api.getJson<CreatePortalResponse>(
        "/v1/snaptrade/auth/connection-portal",
        { headers: token ? { Authorization: `Bearer ${token}` } : undefined }
      )
    },
  })
}


