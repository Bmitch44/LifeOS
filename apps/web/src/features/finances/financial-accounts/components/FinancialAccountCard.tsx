import { FinancialAccount } from "@/src/core/api/generated/types";


export function FinancialAccountCard({ financialAccount }: { financialAccount: FinancialAccount }) {
  return (
    <div>
      <h1>{financialAccount.name}</h1>
      <p>{financialAccount.institution_name}</p>
      <p>{financialAccount.current_balance}</p>
      <p>{financialAccount.currency}</p>
      <p>{financialAccount.source}</p>
      <p>{financialAccount.source_account_id}</p>
      <p>{financialAccount.created_at}</p>
      <p>{financialAccount.updated_at}</p>
    </div>
  )
}