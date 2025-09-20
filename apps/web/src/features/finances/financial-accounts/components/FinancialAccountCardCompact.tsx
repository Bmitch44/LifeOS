import { FinancialAccount } from "@/src/core/api/generated/types";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@workspace/ui/components/card";
import { Badge } from "@workspace/ui/components/badge";


export function FinancialAccountCardCompact({ financialAccount }: { financialAccount: FinancialAccount }) {
  const amount = financialAccount.current_balance ?? 0
  const currency = financialAccount.currency ?? "USD"
  const formattedAmount = new Intl.NumberFormat(undefined, { style: "currency", currency }).format(amount)
  return (
    <Card className="py-2 gap-0">
      <CardHeader className="py-2 px-3 gap-0">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium leading-none">{financialAccount.name}</CardTitle>
          <Badge variant="outline" className="text-[10px] px-1.5 py-0.5">
            {financialAccount.source} | {financialAccount.type}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="py-2 px-3 pt-0">
        <p className="text-sm tabular-nums">{formattedAmount}</p>
      </CardContent>
    </Card>
  );
}

  