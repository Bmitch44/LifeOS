"use client"

import { useMutation } from "@tanstack/react-query"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

type ExchangePublicTokenArgs = { public_token: string }

export function useExchangePlaidPublicToken() {
  const getToken = useAuthToken()
  return useMutation<unknown, Error, ExchangePublicTokenArgs>({
    mutationFn: async ({ public_token }) => {
      const token = await getToken()
      return api.postJson(
        "/v1/plaid/auth/exchange-public-token",
        public_token,
        { headers: token ? { Authorization: `Bearer ${token}` } : undefined }
      )
    },
  })
}


