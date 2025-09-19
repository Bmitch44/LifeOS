"use client"
import { FinancialAccountCard } from "@/src/features/finances/financial-accounts/components/FinancialAccountCard"
import { useAllFinancialAccounts, useSyncFinancialAccounts } from "@/src/features/finances/financial-accounts/hooks/useFinacialAccounts"
import { FinancialAccount } from "@/src/core/api/generated/types"
import { Button } from "@workspace/ui/components/button"

export function FinancialAccountList() {
  const { data, isPending, error } = useAllFinancialAccounts()
  const { mutate: syncFinancialAccounts } = useSyncFinancialAccounts()
  if (isPending) return <div>Loading…</div>
  if (error) return <div>Failed to load financial accounts</div>

  return (
    <div>
        <div className="flex justify-between items-center">
          <h1 className="text-xl font-bold">Financial Accounts</h1>
          <Button onClick={() => syncFinancialAccounts()}>Sync Financial Accounts</Button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4"> 
          {data?.items?.map((financialAccount: FinancialAccount) => (
              <FinancialAccountCard key={financialAccount.id} financialAccount={financialAccount} />
          ))}
        </div>
    </div>
  )
}