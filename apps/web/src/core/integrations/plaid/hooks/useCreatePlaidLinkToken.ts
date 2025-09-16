"use client"

import { useMutation } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

type CreateLinkTokenResponse = { link_token: string }

export function useCreatePlaidLinkToken() {
  const getToken = useAuthToken()
  return useMutation<CreateLinkTokenResponse, Error, void>({
    mutationFn: async () => {
      const token = await getToken()
      return api.postJson<CreateLinkTokenResponse>(
        "/v1/plaid/link-token",
        {},
        { headers: token ? { Authorization: `Bearer ${token}` } : undefined }
      )
    },
  })
}


