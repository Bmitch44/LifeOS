"use client"
import { FinancialAccountCard } from "./FinancialAccountCard"
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
        <Button onClick={() => syncFinancialAccounts()}>Sync Financial Accounts</Button>
      {data?.items?.map((financialAccount: FinancialAccount) => (
        <FinancialAccountCard financialAccount={financialAccount} />
      ))}
    </div>
  )
}