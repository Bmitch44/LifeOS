"use client"

import { useCallback } from "react"
import { useSnaptradeCreatePortal } from "@/src/core/integrations/snaptrade/hooks/useSnaptradeCreatePortal"

export function useSnaptrade() {
  const createPortal = useSnaptradeCreatePortal()

  const getRedirectLink = useCallback(async () => {
    const redirectURI = await createPortal.mutateAsync()
    return redirectURI
  }, [createPortal])

  const connect = useCallback(async () => {
    const redirectURI = await getRedirectLink()
    if (typeof window !== "undefined") window.location.href = redirectURI
  }, [getRedirectLink])

  return {
    connect,
    getRedirectLink,
    isConnecting: createPortal.isPending,
    error: createPortal.error ?? null,
  }
}


