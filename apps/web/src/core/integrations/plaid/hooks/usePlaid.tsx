"use client"

import { useEffect, useState, useCallback } from "react"
import { usePlaidLink, type PlaidLinkOptions } from "react-plaid-link"
import { useCreatePlaidLinkToken } from "@/src/core/integrations/plaid/hooks/useCreatePlaidLinkToken"
import { useExchangePlaidPublicToken } from "@/src/core/integrations/plaid/hooks/useExchangePlaidPublicToken"

export function usePlaid() {
  const [publicToken, setPublicToken] = useState<string | null>(null)
  const [shouldOpen, setShouldOpen] = useState(false)

  const createLinkToken = useCreatePlaidLinkToken()
  const exchangePublicToken = useExchangePlaidPublicToken()

  const config: PlaidLinkOptions = {
    token: createLinkToken.data ?? null,
    onSuccess: (token) => {
      setPublicToken(token)
      exchangePublicToken.mutate({ public_token: token })
    },
    onExit: () => {},
    onEvent: () => {},
  }

  const { open, exit, ready } = usePlaidLink(config)

  const connect = useCallback(async () => {
    setShouldOpen(true)
    if (!createLinkToken.data && !createLinkToken.isPending) {
      try {
        await createLinkToken.mutateAsync()
      } catch (e) {
        setShouldOpen(false)
        throw e
      }
    }
  }, [createLinkToken])

  useEffect(() => {
    if (shouldOpen && ready && createLinkToken.data) {
      open()
      setShouldOpen(false)
    }
  }, [shouldOpen, ready, createLinkToken.data, open])

  return {
    connect,
    exit,
    ready,
    publicToken,
    linkToken: createLinkToken.data ?? null,
    isCreating: createLinkToken.isPending,
    isExchanging: exchangePublicToken.isPending,
    error: createLinkToken.error ?? exchangePublicToken.error ?? null,
  }
}


