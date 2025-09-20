"use client"
import { FinancialAccountCard } from "@/src/features/finances/financial-accounts/components/FinancialAccountCard"
import { useAllFinancialAccounts, useSyncFinancialAccounts } from "@/src/features/finances/financial-accounts/hooks/useFinacialAccounts"
import { FinancialAccount } from "@/src/core/api/generated/types"
import { Button } from "@workspace/ui/components/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@workspace/ui/components/tabs"
import { Progress } from "@workspace/ui/components/progress"
import { useEffect, useRef, useState } from "react"

const integrations = [
  {
    label: "All",
    value: "all",
  },
  {
    label: "Plaid",
    value: "plaid",
  },
  {
    label: "Snaptrade",
    value: "snaptrade",
  },
]

export function FinancialAccountList() {
  const { data, isPending, error } = useAllFinancialAccounts()
  const { mutate: syncFinancialAccounts, isPending: isSyncing } = useSyncFinancialAccounts()
  const [progress, setProgress] = useState(0)
  const intervalRef = useRef<number | null>(null)

  useEffect(() => {
    if (isSyncing) {
      setProgress((p) => (p === 0 ? 5 : p))
      if (intervalRef.current) window.clearInterval(intervalRef.current)
      intervalRef.current = window.setInterval(() => {
        setProgress((p) => (p < 90 ? Math.min(90, p + (1 + Math.random() * 2)) : p))
      }, 400)
    } else {
      if (intervalRef.current) {
        window.clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }
    return () => {
      if (intervalRef.current) {
        window.clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }
  }, [isSyncing])
  if (isPending) return <div>Loading…</div>
  if (error) return <div>Failed to load financial accounts</div>

  return (
    <div>
        <div className="flex justify-between items-center">
          <h1 className="text-xl font-bold mb-4">Financial Accounts</h1>
        </div>
        <Tabs defaultValue="all">
          <div className="flex flex-row justify-between">
            <TabsList className="mb-4">
              <div className="flex flex-row gap-2">
                {integrations.map((integration) => (
                  <TabsTrigger key={integration.value} value={integration.value}>{integration.label}</TabsTrigger>
                ))}
              </div>
            </TabsList>
            {isSyncing || progress > 0 ? (
            <div className="flex flex-col gap-2">
              <p className="text-sm text-muted-foreground">Syncing financial accounts...</p>
              <div className="flex items-center gap-3 min-w-[200px]">
                <Progress value={progress} className="w-48" />
                <span className="text-sm text-muted-foreground w-10 text-right">{Math.floor(progress)}%</span>
              </div>
            </div>
            ) : (
              <Button
                onClick={() =>
                  syncFinancialAccounts(undefined, {
                    onSuccess: () => {
                      setProgress(100)
                      setTimeout(() => setProgress(0), 600)
                    },
                    onError: () => {
                      setProgress(0)
                    },
                  })
                }
                disabled={isPending}
              >
                Sync Financial Accounts
              </Button>
            )}
          </div>
          <TabsContent value="all">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4"> 
              {data?.items?.map((financialAccount: FinancialAccount) => (
                <FinancialAccountCard key={financialAccount.id} financialAccount={financialAccount} />
              ))}
            </div>
          </TabsContent>
          <TabsContent value="plaid">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4"> 
              {data?.items?.filter((financialAccount: FinancialAccount) => financialAccount.source === "plaid").map((financialAccount: FinancialAccount) => (
                <FinancialAccountCard key={financialAccount.id} financialAccount={financialAccount} />
              ))}
            </div>
          </TabsContent>
          <TabsContent value="snaptrade">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4"> 
              {data?.items?.filter((financialAccount: FinancialAccount) => financialAccount.source === "snaptrade").map((financialAccount: FinancialAccount) => (
                <FinancialAccountCard key={financialAccount.id} financialAccount={financialAccount} />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
  )
}