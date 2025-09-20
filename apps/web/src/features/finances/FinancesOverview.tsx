"use client"

import { useAllFinancialAccounts } from "@/src/features/finances/financial-accounts/hooks/useFinacialAccounts"
import { FinancialAccountCardCompact } from "@/src/features/finances/financial-accounts/components/FinancialAccountCardCompact"
import { FinancialAccount } from "@/src/core/api/generated/types"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@workspace/ui/components/card"
import { Button } from "@workspace/ui/components/button"
import Link from "next/link"

export function FinancesOverview() {
  const { data: financialAccounts, isPending, error } = useAllFinancialAccounts()
  if (isPending) return <div>Loading…</div>
  if (error) return <div>Failed to load financial accounts</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">Finances Overview</h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="gap-2 lg:col-span-1 self-start">
          <CardHeader>
            <CardTitle>Total Balance</CardTitle>
            <CardDescription>The total balance of all financial accounts</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-semibold tabular-nums">
              {new Intl.NumberFormat(undefined, { style: "currency", currency: "USD" }).format(
                financialAccounts?.items?.reduce((acc, financialAccount) => acc + (financialAccount.current_balance ?? 0), 0) ?? 0
              )}
            </p>
          </CardContent>
        </Card>
        <Card className="gap-2 lg:col-span-2">
          <CardHeader>
            <div className="flex flex-row justify-between">
                <CardTitle>Financial Accounts</CardTitle>
                <Link href="/finances/accounts">
                    <Button>View All</Button>
                </Link>
            </div>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
            {financialAccounts?.items?.map((financialAccount: FinancialAccount) => (
              <FinancialAccountCardCompact key={financialAccount.id} financialAccount={financialAccount} />
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}