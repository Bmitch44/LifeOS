"use client"

import { useEffect, useMemo, useState } from "react"
import { Button } from "@workspace/ui/components/button"
import { usePlaid } from "@/src/core/integrations/plaid/hooks/usePlaid"
import { useSyncPlaidItems } from "@/src/core/integrations/plaid/hooks/usePlaidItems"
import { useSnaptrade } from "@/src/core/integrations/snaptrade/hooks/useSnaptrade"
import { useSyncSnaptradeConnections } from "@/src/core/integrations/snaptrade/hooks/useSnaptradeConnections"
import { SnapTradeReact } from "snaptrade-react"

export function IntegrationsSection() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-xl font-bold">Integrations</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <PlaidCard />
        <SnaptradeCard />
      </div>
    </div>
  )
}

function PlaidCard() {
  const plaid = usePlaid()
  const sync = useSyncPlaidItems()

  useEffect(() => {
    if (!sync.isPending && !sync.isSuccess && !sync.isError) sync.mutate()
  }, [sync])

  const isChecking = sync.isPending
  const isConnected = useMemo(() => {
    const msg = sync.data?.message
    return Boolean(msg && msg !== "No items to sync")
  }, [sync.data])

  return (
    <div className="border rounded-md p-4 flex items-center justify-between">
      <div>
        <div className="font-medium">Plaid</div>
        <div className="text-sm text-muted-foreground">
          {isChecking ? "Checking…" : isConnected ? "Connected" : "Not connected"}
        </div>
      </div>
      {!isConnected && (
        <Button onClick={plaid.connect} disabled={plaid.isCreating || plaid.isExchanging}>
          {plaid.isCreating || plaid.isExchanging ? "Connecting…" : "Connect"}
        </Button>
      )}
    </div>
  )
}

function SnaptradeCard() {
  const snaptrade = useSnaptrade()
  const sync = useSyncSnaptradeConnections()
  const [open, setOpen] = useState(false)
  const [loginLink, setLoginLink] = useState<string | null>(null)

  useEffect(() => {
    if (!sync.isPending && !sync.isSuccess && !sync.isError) sync.mutate()
  }, [sync])

  const isChecking = sync.isPending
  const isConnected = useMemo(() => {
    const msg = sync.data?.message
    return Boolean(msg && msg !== "No connections to sync")
  }, [sync.data])

  return (
    <div className="border rounded-md p-4 flex items-center justify-between">
      <div>
        <div className="font-medium">Snaptrade</div>
        <div className="text-sm text-muted-foreground">
          {isChecking ? "Checking…" : isConnected ? "Connected" : "Not connected"}
        </div>
      </div>
      {!isConnected && (
        <>
          <Button
            onClick={async () => {
              const link = await snaptrade.getRedirectLink()
              setLoginLink(link)
              setOpen(true)
            }}
            disabled={snaptrade.isConnecting}
          >
            {snaptrade.isConnecting ? "Connecting…" : "Connect"}
          </Button>
          <SnapTradeReact
            loginLink={loginLink ?? ""}
            isOpen={open}
            close={() => setOpen(false)}
            onSuccess={() => {
              setOpen(false)
              // refresh connections
              sync.mutate()
            }}
            onError={() => setOpen(false)}
            onExit={() => setOpen(false)}
          />
        </>
      )}
    </div>
  )
}


