"use client"

import { useCallback } from "react"
import { useSnaptradeRegister } from "@/src/core/integrations/snaptrade/hooks/useSnaptradeRegister"
import { useSnaptradeCreatePortal } from "@/src/core/integrations/snaptrade/hooks/useSnaptradeCreatePortal"

export function useSnaptrade() {
  const register = useSnaptradeRegister()
  const createPortal = useSnaptradeCreatePortal()

  const getRedirectLink = useCallback(async () => {
    const { user_secret } = await register.mutateAsync()
    const { redirectURI } = await createPortal.mutateAsync({ user_secret })
    return redirectURI
  }, [register, createPortal])

  const connect = useCallback(async () => {
    const redirectURI = await getRedirectLink()
    if (typeof window !== "undefined") window.location.href = redirectURI
  }, [getRedirectLink])

  return {
    connect,
    getRedirectLink,
    isConnecting: register.isPending || createPortal.isPending,
    error: register.error ?? createPortal.error ?? null,
  }
}


