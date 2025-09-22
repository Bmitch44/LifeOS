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
    // Ensure token is created ahead of time to avoid popup blockers
    if (!createLinkToken.data && !createLinkToken.isPending) {
      try {
        await createLinkToken.mutateAsync()
      } catch (e) {
        throw e
      }
    }

    if (ready) {
      open()
    } else {
      // Fallback: open once Link is ready
      setShouldOpen(true)
    }
  }, [createLinkToken, ready, open])

  // Pre-initialize Link as soon as possible for lower latency
  useEffect(() => {
    if (!createLinkToken.data && !createLinkToken.isPending) {
      createLinkToken.mutate()
    }
  }, [createLinkToken])

  useEffect(() => {
    if (shouldOpen && ready) {
      open()
      setShouldOpen(false)
    }
  }, [shouldOpen, ready, open])

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


